import hashlib


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    hash_object = hashlib.sha256(password.encode())
    hash_digest = hash_object.hexdigest()
    return hash_digest
