"""
Service Security for managing authentication and authorization.

---
description: Provides security features for services
endpoints: [service_security]
inputs: [credentials, permissions]
outputs: [auth_token]
dependencies: [jwt, logging]
auth: required
alwaysApply: true
---

- Authenticate service requests
- Authorize service access
- Encrypt sensitive data
- Manage security tokens
- Audit security events
"""

import logging
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from functools import wraps

logger = logging.getLogger(__name__)

class ServiceSecurity:
    """Manages service security."""

    def __init__(self, secret_key: str):
        """
        Initialize service security.

        Args:
            secret_key: Secret key for JWT signing
        """
        self.secret_key = secret_key
        self.token_blacklist: List[str] = []
        logger.info("Service security initialized")

    def generate_token(self, service_name: str, permissions: List[str]) -> str:
        """
        Generate a JWT token for a service.

        Args:
            service_name: Name of the service
            permissions: List of permissions

        Returns:
            str: JWT token
        """
        payload = {
            "service": service_name,
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        logger.info(f"Generated token for service: {service_name}")
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token.

        Args:
            token: JWT token to verify

        Returns:
            Optional[Dict[str, Any]]: Token payload if valid
        """
        if token in self.token_blacklist:
            logger.warning("Token is blacklisted")
            return None

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            logger.info(f"Verified token for service: {payload.get('service')}")
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            return None

    def blacklist_token(self, token: str) -> None:
        """
        Add a token to the blacklist.

        Args:
            token: Token to blacklist
        """
        self.token_blacklist.append(token)
        logger.info("Token added to blacklist")

    def check_permission(self, token: str, required_permission: str) -> bool:
        """
        Check if a token has a required permission.

        Args:
            token: JWT token
            required_permission: Required permission

        Returns:
            bool: True if token has permission
        """
        payload = self.verify_token(token)
        if not payload:
            return False

        permissions = payload.get("permissions", [])
        return required_permission in permissions

def require_auth(permission: Optional[str] = None):
    """
    Decorator to require authentication for a service method.

    Args:
        permission: Optional required permission

    Returns:
        Callable: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            token = kwargs.get("token")
            if not token:
                logger.error("No token provided")
                raise ValueError("Authentication required")

            if permission and not self.security.check_permission(token, permission):
                logger.error(f"Permission denied: {permission}")
                raise ValueError("Permission denied")

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def encrypt_data(data: str, key: str) -> str:
    """
    Encrypt sensitive data.

    Args:
        data: Data to encrypt
        key: Encryption key

    Returns:
        str: Encrypted data
    """
    try:
        return jwt.encode({"data": data}, key, algorithm="HS256")
    except Exception as e:
        logger.error(f"Encryption failed: {str(e)}")
        raise

def decrypt_data(encrypted_data: str, key: str) -> str:
    """
    Decrypt sensitive data.

    Args:
        encrypted_data: Data to decrypt
        key: Decryption key

    Returns:
        str: Decrypted data
    """
    try:
        payload = jwt.decode(encrypted_data, key, algorithms=["HS256"])
        return payload["data"]
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}")
        raise 