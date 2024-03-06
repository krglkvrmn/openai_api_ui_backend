from cryptography.fernet import Fernet

from app.core.settings import settings

cipher_suite = Fernet(settings.KEY_ENCODE_SECRET.get_secret_value())


def encrypt(value: str) -> bytes:
    return cipher_suite.encrypt(value.encode())


def decrypt(value: bytes) -> str:
    return cipher_suite.decrypt(value).decode()
