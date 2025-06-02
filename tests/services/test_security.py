"""
Tests for the service security.

---
description: Tests service authentication and authorization
endpoints: [test_security]
inputs: [test_credentials]
outputs: [test_results]
dependencies: [pytest]
auth: required
alwaysApply: true
---

- Test token generation
- Test token verification
- Test permission checks
- Test data encryption
- Test security decorators
"""

import pytest
import jwt
from datetime import datetime, timedelta
from labeeb.services.security import ServiceSecurity, require_auth, encrypt_data, decrypt_data

@pytest.fixture
def security():
    """Create a service security instance for testing."""
    return ServiceSecurity("test_secret_key")

def test_generate_token(security):
    """Test token generation."""
    token = security.generate_token("test_service", ["read", "write"])
    assert token is not None
    payload = security.verify_token(token)
    assert payload["service"] == "test_service"
    assert payload["permissions"] == ["read", "write"]

def test_verify_expired_token(security):
    """Test verification of expired token."""
    payload = {
        "service": "test_service",
        "permissions": ["read"],
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    token = jwt.encode(payload, security.secret_key, algorithm="HS256")
    assert security.verify_token(token) is None

def test_verify_invalid_token(security):
    """Test verification of invalid token."""
    assert security.verify_token("invalid_token") is None

def test_blacklist_token(security):
    """Test token blacklisting."""
    token = security.generate_token("test_service", ["read"])
    security.blacklist_token(token)
    assert security.verify_token(token) is None

def test_check_permission(security):
    """Test permission checking."""
    token = security.generate_token("test_service", ["read", "write"])
    assert security.check_permission(token, "read")
    assert security.check_permission(token, "write")
    assert not security.check_permission(token, "admin")

def test_encrypt_decrypt_data(security):
    """Test data encryption and decryption."""
    data = "sensitive_data"
    encrypted = encrypt_data(data, security.secret_key)
    decrypted = decrypt_data(encrypted, security.secret_key)
    assert decrypted == data

def test_encrypt_decrypt_invalid_data(security):
    """Test encryption/decryption with invalid data."""
    with pytest.raises(Exception):
        decrypt_data("invalid_data", security.secret_key)

class TestService:
    """Test service for testing security decorator."""
    def __init__(self, security):
        self.security = security

    @require_auth("read")
    def read_data(self, token: str):
        return "data"

    @require_auth("write")
    def write_data(self, token: str):
        return "success"

def test_require_auth_decorator(security):
    """Test authentication decorator."""
    service = TestService(security)
    token = security.generate_token("test_service", ["read"])

    # Test with valid token and permission
    assert service.read_data(token=token) == "data"

    # Test with missing token
    with pytest.raises(ValueError, match="Authentication required"):
        service.read_data()

    # Test with invalid permission
    with pytest.raises(ValueError, match="Permission denied"):
        service.write_data(token=token) 