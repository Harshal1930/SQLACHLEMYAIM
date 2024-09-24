from bcrypt import gensalt,hashpw,checkpw

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    """
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.
    """
    return checkpw(plain_password.encode(), hashed_password.encode())