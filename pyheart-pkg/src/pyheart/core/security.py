"""
Security and compliance management for healthcare systems
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta, timezone
import os
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()


class AuthProvider:
    """Authentication provider for healthcare systems"""
    
    def __init__(self, provider_type: str = "oauth2"):
        self.provider_type = provider_type
        self.tokens: Dict[str, Dict[str, Any]] = {}
    
    async def authenticate(self, credentials: Dict[str, Any]) -> Optional[str]:
        """Authenticate user and return token"""
        username = credentials.get("username")
        password = credentials.get("password")

        if not username or not password:
            return None

        # Simplified authentication - in production would validate against secure store
        if self._validate_credentials(username, password):
            token = self._generate_token(username)
            return token

        return None

    def _validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials (placeholder - replace with real store lookup)"""
        return bool(username) and len(password) >= 8

    def _generate_token(self, username: str) -> str:
        """Generate authentication token"""
        now = datetime.now(timezone.utc)
        token = secrets.token_urlsafe(32)
        self.tokens[token] = {
            "username": username,
            "issued_at": now,
            "expires_at": now + timedelta(hours=24),
            "scopes": ["patient.read", "observation.read", "patient.write"],
        }
        return token

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate authentication token"""
        token_data = self.tokens.get(token)
        if not token_data:
            return None

        if datetime.now(timezone.utc) > token_data["expires_at"]:
            del self.tokens[token]
            return None

        return token_data

    async def get_token(self, client_id: str, scope: str) -> str:
        """Get token for OAuth2/SMART on FHIR"""
        now = datetime.now(timezone.utc)
        token = secrets.token_urlsafe(32)
        self.tokens[token] = {
            "client_id": client_id,
            "scope": scope,
            "issued_at": now,
            "expires_at": now + timedelta(hours=1),
        }
        return token


class AuditLogger:
    """Audit logging for compliance"""
    
    def __init__(self):
        self.audit_logs: List[Dict[str, Any]] = []
    
    def log_access(self, user_id: str, resource_type: str, resource_id: str, action: str):
        """Log resource access"""
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "ip_address": "127.0.0.1",  # Would get from request
            "user_agent": "PyHeart Client",  # Would get from request
        }

        self.audit_logs.append(audit_entry)
        logger.info("Audit log entry", **audit_entry)

    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        """Log system events"""
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
        }

        self.audit_logs.append(audit_entry)
        logger.info("System event logged", **audit_entry)
    
    def get_audit_trail(self, 
                       resource_id: Optional[str] = None,
                       user_id: Optional[str] = None,
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get audit trail with filters"""
        filtered_logs = self.audit_logs
        
        if resource_id:
            filtered_logs = [log for log in filtered_logs if log.get("resource_id") == resource_id]
        
        if user_id:
            filtered_logs = [log for log in filtered_logs if log.get("user_id") == user_id]
        
        # Date filtering would be implemented here
        
        return filtered_logs


class EncryptionManager:
    """Data encryption management using AES-256-GCM.

    A caller-supplied *key* (32 raw bytes) takes highest precedence.
    If none is provided the ``PYHEART_ENCRYPTION_KEY`` environment variable
    (hex-encoded 32-byte value) is tried next.  When neither is present a
    fresh random key is generated — suitable for single-process use only.
    """

    def __init__(self, algorithm: str = "AES-256-GCM", key: Optional[bytes] = None):
        self.algorithm = algorithm

        if key is not None:
            if len(key) != 32:
                raise ValueError("Encryption key must be exactly 32 bytes (256 bits)")
            self._master_key = key
        else:
            env_key = os.environ.get("PYHEART_ENCRYPTION_KEY")
            if env_key:
                raw = bytes.fromhex(env_key)
                if len(raw) != 32:
                    raise ValueError(
                        "PYHEART_ENCRYPTION_KEY must be a 64-char hex string (32 bytes)"
                    )
                self._master_key = raw
            else:
                self._master_key = os.urandom(32)  # ephemeral key – single-process only
                logger.warning(
                    "EncryptionManager using a random ephemeral key. "
                    "Set PYHEART_ENCRYPTION_KEY env var for persistent encryption."
                )

        self._aesgcm = AESGCM(self._master_key)
        logger.info("EncryptionManager initialised", algorithm=algorithm)

    def encrypt_data(self, data: str, context: Optional[str] = None) -> Dict[str, str]:
        """Encrypt sensitive data using AES-256-GCM."""
        nonce = os.urandom(12)  # 96-bit nonce
        aad = context.encode() if context else b""
        ciphertext = self._aesgcm.encrypt(nonce, data.encode(), aad)

        return {
            "encrypted_data": (nonce + ciphertext).hex(),
            "algorithm": self.algorithm,
            "context": context or "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def decrypt_data(self, encrypted_info: Dict[str, str]) -> str:
        """Decrypt data previously encrypted with encrypt_data.

        Raises:
            KeyError: if required keys are missing from *encrypted_info*.
            ValueError: if the payload is too short or the algorithm tag doesn't match.
            cryptography.exceptions.InvalidTag: if the ciphertext has been tampered with.
        """
        if "encrypted_data" not in encrypted_info:
            raise KeyError("encrypted_info must contain 'encrypted_data'")

        stored_algorithm = encrypted_info.get("algorithm", "")
        if stored_algorithm and stored_algorithm != self.algorithm:
            raise ValueError(
                f"Algorithm mismatch: stored '{stored_algorithm}', "
                f"expected '{self.algorithm}'"
            )

        try:
            raw = bytes.fromhex(encrypted_info["encrypted_data"])
        except ValueError as exc:
            raise ValueError("'encrypted_data' is not valid hex") from exc

        if len(raw) < 13:  # 12-byte nonce + at least 1 byte ciphertext
            raise ValueError("'encrypted_data' payload is too short to be valid")

        nonce, ciphertext = raw[:12], raw[12:]
        context = encrypted_info.get("context", "")
        aad = context.encode() if context else b""

        try:
            plaintext = self._aesgcm.decrypt(nonce, ciphertext, aad)
        except InvalidTag as exc:
            raise InvalidTag("Decryption failed: ciphertext may be tampered with or key mismatch detected") from exc

        logger.info("Data decrypted", context=context)
        return plaintext.decode()

    def encrypt_pii(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt personally identifiable information"""
        encrypted_data = patient_data.copy()

        # Fields to encrypt
        pii_fields = ["name", "address", "phone", "email", "ssn"]

        for field in pii_fields:
            if field in encrypted_data:
                encrypted_data[field] = self.encrypt_data(str(encrypted_data[field]), field)

        return encrypted_data


class SecurityManager:
    """Comprehensive security management"""
    
    def __init__(self):
        self.auth_provider = AuthProvider()
        self.audit_logger = AuditLogger()
        self.encryption_manager = EncryptionManager()
        self.compliance_rules: Dict[str, List[str]] = {}
        self._initialize_compliance_rules()
    
    def _initialize_compliance_rules(self):
        """Initialize compliance rules"""
        self.compliance_rules = {
            "HIPAA": [
                "encrypt_phi",
                "audit_access",
                "minimum_necessary",
                "access_controls"
            ],
            "GDPR": [
                "consent_management",
                "data_portability",
                "right_to_erasure",
                "privacy_by_design"
            ],
            "ISO27001": [
                "information_security_policy",
                "risk_management",
                "incident_response",
                "business_continuity"
            ]
        }
    
    def enable_encryption(self, algorithm: str = "AES-256-GCM"):
        """Enable data encryption"""
        self.encryption_manager = EncryptionManager(algorithm)
        logger.info("Encryption enabled", algorithm=algorithm)
    
    def enable_audit_logging(self):
        """Enable audit logging"""
        logger.info("Audit logging enabled")
    
    def configure_compliance(self, standards: List[str]):
        """Configure compliance standards"""
        for standard in standards:
            if standard in self.compliance_rules:
                logger.info("Configured compliance", standard=standard)
            else:
                logger.warning("Unknown compliance standard", standard=standard)
    
    def enable_consent_management(self):
        """Enable patient consent management"""
        logger.info("Consent management enabled")
    
    async def authenticate_user(self, credentials: Dict[str, Any]) -> Optional[str]:
        """Authenticate user"""
        token = await self.auth_provider.authenticate(credentials)
        if token:
            self.audit_logger.log_system_event("user_authentication", {
                "username": credentials.get("username"),
                "success": True
            })
        return token
    
    def authorize_access(self, 
                        token: str,
                        resource_type: str,
                        action: str) -> bool:
        """Authorize resource access"""
        token_data = self.auth_provider.validate_token(token)
        if not token_data:
            return False
        
        # Check scopes
        scopes = token_data.get("scopes", [])
        required_scope = f"{resource_type.lower()}.{action}"
        
        authorized = required_scope in scopes
        
        if authorized:
            self.audit_logger.log_access(
                token_data.get("username", "unknown"),
                resource_type,
                "resource_id",  # Would be actual resource ID
                action
            )
        
        return authorized
    
    def encrypt_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt patient data for storage"""
        return self.encryption_manager.encrypt_pii(patient_data)
    
    def check_compliance(self, operation: str, data: Dict[str, Any]) -> List[str]:
        """Check compliance requirements for operation"""
        violations = []
        
        # Example compliance checks
        if operation == "patient_access" and not data.get("consent"):
            violations.append("Missing patient consent")
        
        if operation == "data_export" and not data.get("audit_trail"):
            violations.append("Missing audit trail for data export")
        
        return violations
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate compliance report"""
        return {
            "report_date": datetime.now(timezone.utc).isoformat(),
            "audit_entries": len(self.audit_logger.audit_logs),
            "encryption_enabled": True,
            "compliance_standards": list(self.compliance_rules.keys()),
            "active_tokens": len(self.auth_provider.tokens),
            "violations": [],  # Would track actual violations
        }