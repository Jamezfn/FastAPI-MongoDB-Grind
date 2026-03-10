from bcrypt import hashpw, checkpw, gensalt

class Hash:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes) -> bool:
        """Verify a plain password against a bcrypt hash."""
        return checkpw(password=plain_password.encode(), hashed_password=hashed_password)
    
    @staticmethod
    def hash_password(plain_password: str) -> bytes:
        """Generate a bcrypt hash for a plain password."""
        return hashpw(password=plain_password.encode(), salt=gensalt())