"""
Tests for Mercury API Application
=================================

DIRECTIVE: System must be glitch-free and performant.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_returns_200(self):
        """Should return healthy status."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "mercury"
    
    def test_health_includes_version(self):
        """Should include version info."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        data = response.json()
        assert "version" in data
        assert "timestamp" in data


class TestStatusEndpoint:
    """Tests for status endpoint."""
    
    def test_status_returns_200(self):
        """Should return status info."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/status")
        
        assert response.status_code == 200
        data = response.json()
        assert "ready" in data
        assert "kite" in data
        assert "anthropic" in data
    
    def test_status_includes_api_details(self):
        """Should include API status details."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/status")
        
        data = response.json()
        
        assert "status" in data["kite"]
        assert "authenticated" in data["kite"]
        assert "status" in data["anthropic"]
        assert "authenticated" in data["anthropic"]


class TestChatEndpoint:
    """Tests for chat endpoint."""
    
    def test_chat_returns_response(self):
        """Should return chat response."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.post("/api/chat", json={
            "query": "Hello",
            "conversation_id": None,
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert "timestamp" in data
    
    def test_chat_maintains_conversation(self):
        """Should maintain conversation ID."""
        from mercury.api.app import app
        
        client = TestClient(app)
        
        # First message
        response1 = client.post("/api/chat", json={
            "query": "Hello",
        })
        conv_id = response1.json()["conversation_id"]
        
        # Second message with same conversation
        response2 = client.post("/api/chat", json={
            "query": "Follow up",
            "conversation_id": conv_id,
        })
        
        assert response2.json()["conversation_id"] == conv_id


class TestFrontendEndpoint:
    """Tests for frontend HTML endpoint."""
    
    def test_frontend_returns_html(self):
        """Should return HTML page."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_frontend_includes_mercury_branding(self):
        """Should include Mercury branding."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/")
        
        assert "Mercury" in response.text
        assert "☿" in response.text
    
    def test_frontend_includes_chat_interface(self):
        """Should include chat interface elements."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.get("/")
        
        assert "messages" in response.text
        assert "input" in response.text
        assert "sendMessage" in response.text


class TestClearConversation:
    """Tests for conversation clearing."""
    
    def test_clear_existing_conversation(self):
        """Should clear existing conversation."""
        from mercury.api.app import app
        
        client = TestClient(app)
        
        # Create conversation
        response = client.post("/api/chat", json={"query": "Hello"})
        conv_id = response.json()["conversation_id"]
        
        # Clear it
        response = client.delete(f"/api/chat/{conv_id}")
        
        assert response.status_code == 200
        assert response.json()["status"] == "cleared"
    
    def test_clear_nonexistent_conversation(self):
        """Should handle nonexistent conversation."""
        from mercury.api.app import app
        
        client = TestClient(app)
        response = client.delete("/api/chat/nonexistent_id")
        
        assert response.status_code == 200
        assert response.json()["status"] == "not_found"
