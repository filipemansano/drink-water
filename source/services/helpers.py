import hashlib

def chipper_password(password: str) -> str:
    password_bits  = password.encode('utf-8')
    secret_password = hashlib.sha256(password_bits)
    return secret_password.hexdigest()