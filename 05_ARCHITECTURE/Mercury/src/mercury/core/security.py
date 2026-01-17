"""
Mercury Security Utilities
==========================

Security utilities for sensitive data handling.

MISSION-CRITICAL STANDARD: S-001 through S-005
- Never log sensitive data
- Mask credentials in error messages
- Validate at boundaries
"""

import re
from typing import Any

# Patterns that indicate sensitive data - NEVER log these
# NOTE: The replacer function uses the entire match for replacement, so pattern
# should match the full sensitive segment including the value to be redacted.
# IMPORTANT: Order matters! More specific patterns should come first.
SENSITIVE_PATTERNS = [
    # Bearer token pattern - MUST be first to catch "Authorization: Bearer token" in one match
    # This pattern matches the entire "Authorization: Bearer <token>" or just "Bearer <token>"
    (re.compile(r'(?:Authorization:\s*)?Bearer\s+\S+', re.IGNORECASE), 'bearer_token'),
    # Standard key=value patterns
    (re.compile(r'api_key["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)', re.IGNORECASE), 'api_key'),
    (re.compile(r'api_secret["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)', re.IGNORECASE), 'api_secret'),
    (re.compile(r'access_token["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)', re.IGNORECASE), 'access_token'),
    (re.compile(r'password["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)', re.IGNORECASE), 'password'),
    (re.compile(r'secret["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)', re.IGNORECASE), 'secret'),
    (re.compile(r'token["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)', re.IGNORECASE), 'token'),
    (re.compile(r'authorization["\']?\s*[:=]\s*["\']?[^"\'\s]+', re.IGNORECASE), 'authorization'),
]

# Keys that should never appear in logs
SENSITIVE_KEYS = {
    'api_key', 'api_secret', 'access_token', 'password', 'secret',
    'token', 'authorization', 'kite_api_key', 'kite_api_secret',
    'kite_access_token', 'anthropic_api_key', 'bearer', 'credential',
}


def mask_sensitive_string(value: str, visible_chars: int = 4) -> str:
    """
    Mask a sensitive string, showing only first few characters.
    
    Args:
        value: The sensitive string to mask
        visible_chars: Number of characters to show at start
        
    Returns:
        Masked string like "sk-a****"
    """
    if not value:
        return "[EMPTY]"
    
    if len(value) <= visible_chars:
        return "*" * len(value)
    
    return value[:visible_chars] + "*" * (len(value) - visible_chars)


def sanitize_text(text: str) -> str:
    """
    Remove sensitive data from a text string.
    
    Use this before logging any text that might contain credentials.
    
    Args:
        text: Text that may contain sensitive data
        
    Returns:
        Sanitized text with sensitive data masked
    """
    if not text:
        return text
    
    result = text
    for pattern, name in SENSITIVE_PATTERNS:
        def replacer(match):
            return f"{name}=[REDACTED]"
        result = pattern.sub(replacer, result)
    
    return result


def sanitize_dict(data: dict, depth: int = 0, max_depth: int = 10) -> dict:
    """
    Recursively sanitize a dictionary, masking sensitive values.
    
    Args:
        data: Dictionary that may contain sensitive data
        depth: Current recursion depth
        max_depth: Maximum recursion depth
        
    Returns:
        Sanitized dictionary with sensitive values masked
    """
    if depth > max_depth:
        return {"_truncated": "max depth exceeded"}
    
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        key_lower = key.lower()
        
        # Check if key indicates sensitive data
        is_sensitive = any(
            sensitive in key_lower 
            for sensitive in SENSITIVE_KEYS
        )
        
        if is_sensitive:
            if isinstance(value, str):
                result[key] = mask_sensitive_string(value)
            else:
                result[key] = "[REDACTED]"
        elif isinstance(value, dict):
            result[key] = sanitize_dict(value, depth + 1, max_depth)
        elif isinstance(value, list):
            result[key] = [
                sanitize_dict(item, depth + 1, max_depth) 
                if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, str):
            result[key] = sanitize_text(value)
        else:
            result[key] = value
    
    return result


def sanitize_exception(exc: Exception) -> str:
    """
    Sanitize an exception message for safe logging.
    
    Args:
        exc: Exception to sanitize
        
    Returns:
        Sanitized exception string
    """
    return sanitize_text(str(exc))


def is_sensitive_key(key: str) -> bool:
    """
    Check if a key name indicates sensitive data.
    
    Args:
        key: Key name to check
        
    Returns:
        True if key appears to hold sensitive data
    """
    return any(
        sensitive in key.lower()
        for sensitive in SENSITIVE_KEYS
    )


def validate_no_secrets_in_string(text: str) -> list[str]:
    """
    Validate that a string doesn't contain obvious secrets.
    
    Useful for checking log messages before they're written.
    
    Args:
        text: Text to validate
        
    Returns:
        List of warnings about potential secrets found
    """
    warnings = []
    
    for pattern, name in SENSITIVE_PATTERNS:
        if pattern.search(text):
            warnings.append(f"Potential {name} found in text")
    
    return warnings
