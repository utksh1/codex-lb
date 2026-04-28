from __future__ import annotations

from pathlib import Path

from cryptography.fernet import Fernet

from app.core.config.settings import get_settings


def _validate_fernet_key(key: bytes) -> bytes:
    Fernet(key)
    return key


def _persist_key_file(key_file: Path, key: bytes) -> None:
    key_file.parent.mkdir(parents=True, exist_ok=True)
    if key_file.exists() and key_file.read_bytes() == key:
        return
    key_file.write_bytes(key)
    key_file.chmod(0o600)


def _key_bytes_from_setting(raw_key: str) -> bytes:
    return _validate_fernet_key(raw_key.encode("utf-8"))


def _get_or_create_key(key_file: Path, *, configured_key: str | None = None) -> bytes:
    if configured_key is not None:
        key = _key_bytes_from_setting(configured_key)
        _persist_key_file(key_file, key)
        return key
    key_file.parent.mkdir(parents=True, exist_ok=True)
    if key_file.exists():
        return _validate_fernet_key(key_file.read_bytes())
    key = Fernet.generate_key()
    _persist_key_file(key_file, key)
    return key


class TokenEncryptor:
    def __init__(self, key: bytes | None = None, key_file: Path | None = None) -> None:
        settings = get_settings()
        resolved_file = key_file or settings.encryption_key_file
        resolved_key = _validate_fernet_key(key) if key is not None else _get_or_create_key(
            resolved_file,
            configured_key=settings.encryption_key,
        )
        self._fernet = Fernet(resolved_key)

    def encrypt(self, token: str) -> bytes:
        return self._fernet.encrypt(token.encode())

    def decrypt(self, encrypted: bytes) -> str:
        return self._fernet.decrypt(encrypted).decode()


def get_or_create_key(key_file: Path | None = None) -> bytes:
    settings = get_settings()
    resolved_file = key_file or settings.encryption_key_file
    return _get_or_create_key(resolved_file, configured_key=settings.encryption_key)
