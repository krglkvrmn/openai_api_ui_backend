from cryptography.fernet import Fernet

from app.core.config import KEY_ENCODE_SECRET_KEY

cipher_suite = Fernet(KEY_ENCODE_SECRET_KEY)


def encrypt(value: str) -> bytes:
    return cipher_suite.encrypt(value.encode())


def decrypt(value: bytes) -> str:
    return cipher_suite.decrypt(value).decode()