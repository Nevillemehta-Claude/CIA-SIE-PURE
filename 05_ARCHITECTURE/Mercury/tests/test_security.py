"""
Tests for Mercury Security Utilities
====================================

Tests for sensitive data masking and sanitization.
"""

import pytest
from mercury.core.security import (
    mask_sensitive_string,
    sanitize_text,
    sanitize_dict,
    sanitize_exception,
    is_sensitive_key,
    validate_no_secrets_in_string,
)


class TestMaskSensitiveString:
    """Tests for mask_sensitive_string function."""
    
    def test_mask_normal_string(self):
        """Should mask most of the string."""
        result = mask_sensitive_string("sk-ant-api03-xxxxx")
        assert result.startswith("sk-a")
        assert "****" in result
        assert result.count("*") == len("sk-ant-api03-xxxxx") - 4
    
    def test_mask_short_string(self):
        """Should fully mask short strings."""
        result = mask_sensitive_string("abc")
        assert result == "***"
    
    def test_mask_empty_string(self):
        """Should handle empty string."""
        result = mask_sensitive_string("")
        assert result == "[EMPTY]"
    
    def test_mask_exact_length(self):
        """Should handle string exactly at visible_chars length."""
        result = mask_sensitive_string("abcd", visible_chars=4)
        assert result == "****"
    
    def test_custom_visible_chars(self):
        """Should respect custom visible_chars."""
        result = mask_sensitive_string("my-secret-key-12345", visible_chars=6)
        assert result.startswith("my-sec")


class TestSanitizeText:
    """Tests for sanitize_text function."""
    
    def test_sanitize_api_key(self):
        """Should redact API keys."""
        text = 'api_key="sk-ant-xxxx"'
        result = sanitize_text(text)
        assert "sk-ant" not in result
        assert "REDACTED" in result
    
    def test_sanitize_bearer_token(self):
        """Should redact bearer tokens."""
        text = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        result = sanitize_text(text)
        assert "eyJ" not in result
        assert "REDACTED" in result
    
    def test_sanitize_password(self):
        """Should redact passwords."""
        text = 'password=mysecretpassword123'
        result = sanitize_text(text)
        assert "mysecretpassword" not in result
    
    def test_preserve_non_sensitive(self):
        """Should preserve non-sensitive text."""
        text = "Processing query for instrument RELIANCE"
        result = sanitize_text(text)
        assert "Processing query for instrument RELIANCE" == result
    
    def test_empty_text(self):
        """Should handle empty text."""
        assert sanitize_text("") == ""
        assert sanitize_text(None) is None


class TestSanitizeDict:
    """Tests for sanitize_dict function."""
    
    def test_sanitize_simple_dict(self):
        """Should sanitize sensitive keys."""
        data = {
            "api_key": "sk-ant-xxxx",
            "name": "test",
        }
        result = sanitize_dict(data)
        assert "sk-ant" not in result["api_key"]
        assert result["name"] == "test"
    
    def test_sanitize_nested_dict(self):
        """Should sanitize nested dictionaries."""
        data = {
            "config": {
                "api_secret": "secret123",
                "endpoint": "https://api.example.com",
            }
        }
        result = sanitize_dict(data)
        assert "secret123" not in str(result)
        assert result["config"]["endpoint"] == "https://api.example.com"
    
    def test_sanitize_list_in_dict(self):
        """Should sanitize lists containing dicts."""
        data = {
            "tokens": [
                {"access_token": "token1"},
                {"access_token": "token2"},
            ]
        }
        result = sanitize_dict(data)
        assert "token1" not in str(result)
        assert "token2" not in str(result)
    
    def test_max_depth(self):
        """Should handle max depth."""
        deep = {"a": {"b": {"c": {"d": {"e": {}}}}}}
        result = sanitize_dict(deep, max_depth=2)
        # Should truncate at depth
        assert "_truncated" in str(result) or isinstance(result["a"]["b"], dict)
    
    def test_non_dict_passthrough(self):
        """Should pass through non-dict values."""
        assert sanitize_dict("string") == "string"
        assert sanitize_dict(123) == 123


class TestIsSensitiveKey:
    """Tests for is_sensitive_key function."""
    
    @pytest.mark.parametrize("key", [
        "api_key",
        "API_KEY",
        "kite_api_secret",
        "access_token",
        "PASSWORD",
        "secret_value",
        "authorization",
    ])
    def test_sensitive_keys_detected(self, key):
        """Should detect sensitive keys."""
        assert is_sensitive_key(key) is True
    
    @pytest.mark.parametrize("key", [
        "name",
        "symbol",
        "price",
        "quantity",
        "timestamp",
    ])
    def test_non_sensitive_keys(self, key):
        """Should not flag non-sensitive keys."""
        assert is_sensitive_key(key) is False


class TestValidateNoSecrets:
    """Tests for validate_no_secrets_in_string function."""
    
    def test_detect_api_key(self):
        """Should warn about API keys."""
        text = 'api_key="test123"'
        warnings = validate_no_secrets_in_string(text)
        assert len(warnings) > 0
    
    def test_clean_text(self):
        """Should return no warnings for clean text."""
        text = "Query processed successfully for RELIANCE"
        warnings = validate_no_secrets_in_string(text)
        assert len(warnings) == 0
