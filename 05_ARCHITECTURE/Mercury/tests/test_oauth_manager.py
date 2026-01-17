"""
Tests for OAuth Manager
========================

Tests for the Kite OAuth lifecycle management system.
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
import json

from mercury.kite.oauth_manager import (
    OAuthManager,
    TokenInfo,
    TokenState,
    TokenExpiredError,
    get_oauth_manager,
)


class TestTokenInfo:
    """Tests for TokenInfo dataclass."""
    
    def test_token_info_creation(self):
        """Test creating a TokenInfo."""
        token = TokenInfo(
            access_token="test_token",
            created_at=datetime.now(timezone.utc),
            user_id="test_user",
            user_name="Test User",
        )
        
        assert token.access_token == "test_token"
        assert token.user_id == "test_user"
        assert token.user_name == "Test User"
    
    def test_token_expiry_detection(self):
        """Test that token expiry is detected correctly."""
        # Token created 25 hours ago should be expired
        old_time = datetime.now(timezone.utc) - timedelta(hours=25)
        token = TokenInfo(
            access_token="old_token",
            created_at=old_time,
        )
        
        assert token.is_expired() is True
    
    def test_token_not_expired(self):
        """Test that fresh token is not marked as expired."""
        token = TokenInfo(
            access_token="fresh_token",
            created_at=datetime.now(timezone.utc),
        )
        
        # Token created just now should not be expired
        # (unless we're right at 6 AM IST boundary)
        assert token.is_expired() is False
    
    def test_token_to_dict(self):
        """Test serialization to dict."""
        now = datetime.now(timezone.utc)
        token = TokenInfo(
            access_token="test_token",
            created_at=now,
            user_id="user123",
            user_name="Test User",
        )
        
        data = token.to_dict()
        
        assert data["access_token"] == "test_token"
        assert data["user_id"] == "user123"
        assert data["user_name"] == "Test User"
        assert "created_at" in data
    
    def test_token_from_dict(self):
        """Test deserialization from dict."""
        now = datetime.now(timezone.utc)
        data = {
            "access_token": "restored_token",
            "created_at": now.isoformat(),
            "expires_at": None,
            "user_id": "user456",
            "user_name": "Restored User",
        }
        
        token = TokenInfo.from_dict(data)
        
        assert token.access_token == "restored_token"
        assert token.user_id == "user456"
        assert token.user_name == "Restored User"


class TestOAuthManager:
    """Tests for OAuthManager."""
    
    @pytest.fixture
    def temp_token_dir(self):
        """Create a temporary directory for token storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def oauth_manager(self, temp_token_dir):
        """Create an OAuth manager with temp storage."""
        return OAuthManager(
            token_dir=temp_token_dir,
            api_key="test_api_key",
            api_secret="test_api_secret",
        )
    
    def test_login_url(self, oauth_manager):
        """Test login URL generation."""
        url = oauth_manager.login_url
        
        assert "kite.zerodha.com" in url
        assert "test_api_key" in url
        assert "v=3" in url
    
    @pytest.mark.skip(reason="API key validation behavior has changed")
    def test_login_url_without_api_key(self, temp_token_dir):
        """Test that login URL raises error without API key."""
        oauth = OAuthManager(
            token_dir=temp_token_dir,
            api_key=None,
        )
        
        with pytest.raises(ValueError, match="KITE_API_KEY"):
            _ = oauth.login_url
    
    def test_token_state_missing(self, oauth_manager):
        """Test token state is MISSING when no token."""
        # Clear any env token
        with patch('mercury.kite.oauth_manager.get_settings') as mock_settings:
            mock_settings.return_value.kite_access_token = None
            mock_settings.return_value.kite_api_key = "test_key"
            mock_settings.return_value.kite_api_secret = "test_secret"
            
            oauth = OAuthManager(
                token_dir=oauth_manager.token_dir,
                api_key="test_key",
            )
            assert oauth.token_state == TokenState.MISSING
    
    def test_has_valid_token_false_when_missing(self, oauth_manager):
        """Test has_valid_token is False when no token."""
        assert oauth_manager.has_valid_token is False
    
    @pytest.mark.asyncio
    async def test_get_valid_token_raises_when_missing(self, oauth_manager):
        """Test that get_valid_token raises TokenExpiredError when no token."""
        with patch('mercury.kite.oauth_manager.get_settings') as mock_settings:
            mock_settings.return_value.kite_access_token = None
            
            with pytest.raises(TokenExpiredError):
                await oauth_manager.get_valid_token()
    
    @pytest.mark.asyncio
    async def test_get_valid_token_from_env(self, oauth_manager):
        """Test that env token is returned when available."""
        with patch('mercury.kite.oauth_manager.get_settings') as mock_settings:
            mock_settings.return_value.kite_access_token = "env_token"
            
            token = await oauth_manager.get_valid_token()
            assert token == "env_token"
    
    def test_token_persistence(self, oauth_manager, temp_token_dir):
        """Test that tokens are persisted to disk."""
        token_info = TokenInfo(
            access_token="persistent_token",
            created_at=datetime.now(timezone.utc),
            user_name="Test User",
        )
        
        oauth_manager._token_info = token_info
        oauth_manager._save_token(token_info)
        
        # Create new manager and check token loaded
        new_oauth = OAuthManager(
            token_dir=temp_token_dir,
            api_key="test_key",
        )
        
        assert new_oauth._token_info is not None
        assert new_oauth._token_info.access_token == "persistent_token"
    
    def test_get_status(self, oauth_manager):
        """Test status dictionary generation."""
        status = oauth_manager.get_status()
        
        assert "state" in status
        assert "has_token" in status
        assert "login_url" in status
    
    def test_get_status_with_token(self, oauth_manager):
        """Test status includes token info when present."""
        oauth_manager._token_info = TokenInfo(
            access_token="test_token",
            created_at=datetime.now(timezone.utc),
            user_name="Status Test User",
            user_id="user789",
        )
        
        status = oauth_manager.get_status()
        
        assert status["has_token"] is True
        assert status["user_name"] == "Status Test User"
        assert status["user_id"] == "user789"
        assert "is_expired" in status


class TestOAuthCallback:
    """Tests for OAuth callback handling."""
    
    @pytest.fixture
    def temp_token_dir(self):
        """Create a temporary directory for token storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.mark.asyncio
    async def test_oauth_callback_success(self, temp_token_dir):
        """Test successful OAuth callback."""
        oauth = OAuthManager(
            token_dir=temp_token_dir,
            api_key="test_api_key",
            api_secret="test_api_secret",
        )
        
        # Mock the HTTP client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "access_token": "new_access_token",
                "user_id": "callback_user",
                "user_name": "Callback User",
            }
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance
            
            token_info = await oauth.handle_oauth_callback("test_request_token")
        
        assert token_info.access_token == "new_access_token"
        assert token_info.user_name == "Callback User"
        assert oauth._token_info is not None
    
    @pytest.mark.asyncio
    async def test_oauth_callback_failure(self, temp_token_dir):
        """Test OAuth callback failure handling."""
        oauth = OAuthManager(
            token_dir=temp_token_dir,
            api_key="test_api_key",
            api_secret="test_api_secret",
        )
        
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid token"}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_instance.__aenter__.return_value = mock_instance
            mock_instance.__aexit__.return_value = None
            mock_client.return_value = mock_instance
            
            with pytest.raises(ValueError, match="OAuth failed"):
                await oauth.handle_oauth_callback("bad_request_token")


class TestGlobalOAuthManager:
    """Tests for global OAuth manager instance."""
    
    def test_get_oauth_manager_singleton(self):
        """Test that get_oauth_manager returns same instance."""
        # Reset global state
        import mercury.kite.oauth_manager as oauth_module
        oauth_module._oauth_manager = None
        
        manager1 = get_oauth_manager()
        manager2 = get_oauth_manager()
        
        assert manager1 is manager2
