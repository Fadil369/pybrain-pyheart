"""Tests for security module — EncryptionManager, AuthProvider, AuditLogger."""

import os
import pytest
from unittest.mock import patch
from cryptography.exceptions import InvalidTag

from pyheart.core.security import EncryptionManager, AuthProvider, AuditLogger, SecurityManager


class TestEncryptionManager:
    """Tests for AES-256-GCM encryption / decryption."""

    def test_roundtrip_no_context(self):
        """Encrypt then decrypt without context returns original plaintext."""
        em = EncryptionManager()
        enc = em.encrypt_data("hello world")
        assert em.decrypt_data(enc) == "hello world"

    def test_roundtrip_with_context(self):
        """Encrypt then decrypt with a context string returns original plaintext."""
        em = EncryptionManager()
        enc = em.encrypt_data("sensitive value", "ssn")
        assert em.decrypt_data(enc) == "sensitive value"

    def test_roundtrip_empty_string(self):
        """Empty plaintext encrypts and decrypts correctly."""
        em = EncryptionManager()
        enc = em.encrypt_data("")
        assert em.decrypt_data(enc) == ""

    def test_ciphertext_differs_each_call(self):
        """Two encryptions of the same plaintext produce different ciphertexts (random nonce)."""
        em = EncryptionManager()
        enc1 = em.encrypt_data("data")
        enc2 = em.encrypt_data("data")
        assert enc1["encrypted_data"] != enc2["encrypted_data"]

    def test_caller_supplied_key_accepted(self):
        """Caller-supplied 32-byte key is used and allows cross-instance decryption."""
        key = os.urandom(32)
        em1 = EncryptionManager(key=key)
        em2 = EncryptionManager(key=key)
        enc = em1.encrypt_data("cross-instance", "ctx")
        assert em2.decrypt_data(enc) == "cross-instance"

    def test_caller_key_wrong_length_raises(self):
        """A key that is not 32 bytes raises ValueError."""
        with pytest.raises(ValueError, match="32 bytes"):
            EncryptionManager(key=b"short")

    def test_env_var_key_used(self):
        """PYHEART_ENCRYPTION_KEY env var is loaded and usable."""
        key = os.urandom(32)
        with patch.dict(os.environ, {"PYHEART_ENCRYPTION_KEY": key.hex()}):
            em = EncryptionManager()
            enc = em.encrypt_data("from env key")
        # Decrypt with explicit key (same bytes)
        em2 = EncryptionManager(key=key)
        assert em2.decrypt_data(enc) == "from env key"

    def test_env_var_wrong_length_raises(self):
        """An env var with wrong-length hex raises ValueError."""
        with patch.dict(os.environ, {"PYHEART_ENCRYPTION_KEY": "deadbeef"}):
            with pytest.raises(ValueError, match="64-char"):
                EncryptionManager()

    def test_decrypt_missing_encrypted_data_key(self):
        """Missing 'encrypted_data' key raises KeyError."""
        em = EncryptionManager()
        with pytest.raises(KeyError, match="encrypted_data"):
            em.decrypt_data({"context": "", "algorithm": "AES-256-GCM"})

    def test_decrypt_invalid_hex_raises(self):
        """Non-hex 'encrypted_data' raises ValueError."""
        em = EncryptionManager()
        with pytest.raises(ValueError, match="valid hex"):
            em.decrypt_data({"encrypted_data": "not-hex-!!"})

    def test_decrypt_payload_too_short_raises(self):
        """A payload shorter than 13 bytes raises ValueError."""
        em = EncryptionManager()
        with pytest.raises(ValueError, match="too short"):
            em.decrypt_data({"encrypted_data": "deadbeef01020304"})

    def test_decrypt_algorithm_mismatch_raises(self):
        """Mismatched 'algorithm' field raises ValueError."""
        em = EncryptionManager()
        enc = em.encrypt_data("test")
        enc["algorithm"] = "AES-128-GCM"
        with pytest.raises(ValueError, match="Algorithm mismatch"):
            em.decrypt_data(enc)

    def test_decrypt_tampered_ciphertext_raises(self):
        """Tampered ciphertext raises InvalidTag."""
        em = EncryptionManager()
        enc = em.encrypt_data("secret")
        # Flip last byte
        raw = bytearray(bytes.fromhex(enc["encrypted_data"]))
        raw[-1] ^= 0xFF
        enc["encrypted_data"] = raw.hex()
        with pytest.raises(InvalidTag):
            em.decrypt_data(enc)

    def test_encrypt_pii_encrypts_pii_fields(self):
        """PII fields are encrypted; non-PII fields remain unchanged."""
        em = EncryptionManager()
        patient = {"name": "Jane Doe", "email": "jane@example.com", "age": 35}
        encrypted = em.encrypt_pii(patient)
        assert isinstance(encrypted["name"], dict)
        assert isinstance(encrypted["email"], dict)
        assert encrypted["age"] == 35


class TestAuthProvider:
    """Tests for token generation and validation."""

    @pytest.mark.asyncio
    async def test_authenticate_valid_credentials(self):
        """Valid credentials return a token."""
        ap = AuthProvider()
        token = await ap.authenticate({"username": "alice", "password": "password123"})
        assert token is not None

    @pytest.mark.asyncio
    async def test_authenticate_missing_fields_returns_none(self):
        """Missing username or password returns None."""
        ap = AuthProvider()
        assert await ap.authenticate({"username": "alice"}) is None
        assert await ap.authenticate({"password": "pass12345"}) is None

    def test_validate_token_valid(self):
        """A freshly generated token validates correctly."""
        import asyncio
        ap = AuthProvider()
        token = asyncio.run(ap.get_token("client1", "openid"))
        data = ap.validate_token(token)
        assert data is not None
        assert data["client_id"] == "client1"

    def test_validate_token_unknown_returns_none(self):
        """An unknown token returns None."""
        ap = AuthProvider()
        assert ap.validate_token("totally-fake-token") is None


class TestFHIRClientClose:
    """Tests for FHIRClient.close() cleanup behaviour."""

    def test_close_calls_async_client_aclose(self):
        """close() closes the async client via asyncio.run() when no loop is running."""
        from unittest.mock import AsyncMock, MagicMock
        from pyheart.core.client import FHIRClient

        client = FHIRClient("https://fhir.example.com")
        # Replace the async client with a mock
        mock_async_client = AsyncMock()
        mock_async_client.is_closed = False
        mock_async_client.aclose = AsyncMock()
        client._async_client = mock_async_client

        client._client = MagicMock()  # suppress real sync close

        client.close()

        mock_async_client.aclose.assert_called_once()


class TestPluginRegistryUnregister:
    """Tests for PluginRegistry.unregister_plugin() cleanup behaviour."""

    @pytest.mark.asyncio
    async def test_unregister_calls_cleanup_in_async_context(self):
        """cleanup() is scheduled as a task when called from within a running loop."""
        from pyheart.core.plugins import PluginRegistry, Plugin, PluginMetadata, PluginType

        class FakePlugin(Plugin):
            cleaned_up = False

            def get_metadata(self):
                return PluginMetadata(
                    name="Fake",
                    version="0.1",
                    plugin_type=PluginType.ADAPTER,
                    description="Test plugin",
                )

            async def initialize(self):
                return True

            async def cleanup(self):
                FakePlugin.cleaned_up = True
                return True

        registry = PluginRegistry()
        plugin = FakePlugin()
        registry.register_plugin("fake", plugin)

        result = registry.unregister_plugin("fake")
        assert result is True
        assert "fake" not in registry.plugins

        # Give the scheduled task a chance to run
        import asyncio
        await asyncio.sleep(0)
        assert FakePlugin.cleaned_up is True

    def test_unregister_calls_cleanup_in_sync_context(self):
        """cleanup() is executed synchronously via asyncio.run() when no loop is running."""
        from pyheart.core.plugins import PluginRegistry, Plugin, PluginMetadata, PluginType

        class FakePlugin(Plugin):
            cleaned_up = False

            def get_metadata(self):
                return PluginMetadata(
                    name="Fake",
                    version="0.1",
                    plugin_type=PluginType.ADAPTER,
                    description="Test plugin",
                )

            async def initialize(self):
                return True

            async def cleanup(self):
                FakePlugin.cleaned_up = True
                return True

        registry = PluginRegistry()
        plugin = FakePlugin()
        registry.register_plugin("fake", plugin)

        registry.unregister_plugin("fake")
        assert FakePlugin.cleaned_up is True
