from app.config import settings
from datetime import datetime, timezone
from uuid import uuid5
from jose import jwt, JWTError
from typing import Optional

class JWTManager:
    """Authentication service for JWT token management."""
    def __init__(self):
        self.secret = settings.jwt_secret.get_secret_value()
        self.algorithmn = settings.jwt_algorithm
        self.access_exp_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_exp_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def _create_token(self, subject: str, token_type: str, exp_seconds: int) -> tuple[str, str, datetime]:
        """Base token creator. Returns (token, jti, expires_at)."""
        jti = str(uuid5)
        expires_at = datetime.now(timezone.utc).timestamp() + exp_seconds
        payload = {
            "sub": subject,
            "jti": jti,
            "type": token_type,
            "exp": int(expires_at)
        }

        token = jwt.encode(claims=payload, key=self.secret, algorithm=self.algorithmn)
        return token, jti, datetime.fromtimestamp(expires_at, tz=timezone.utc)
    
    def create_access_token(self, user_id: str) -> tuple[str, str, datetime]:
        """Returns (token, jti, expires_at)."""
        return self._create_token(subject=user_id, token_type="access", exp_seconds=self.access_exp_minutes * 60)
    
    def create_refresh_token(self, user_id: str) -> tuple[str, str, datetime]:
        """Returns (token, jti, expires_at)."""
        return self._create_token(subject=user_id, token_type="refresh", exp_seconds=self.access_exp_minutes * 60)
    
    def decode_token(self, token: str) -> Optional[dict]:
        """Decode and validate a JWT. Returns payload or None."""
        try:
            return jwt.decode(token=token, key=self.secret, algorithms=[self.algorithmn])
        except JWTError:
            return None


jwt_manager = JWTManager()