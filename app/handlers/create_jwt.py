import jwt
import datetime
from app.config.config import Config
cfg = Config()

# Helper function to create JWT tokens
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)
    return encoded_jwt
