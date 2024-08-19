import secrets

class Settings:
    SECRET_KEY: str = secrets.token_hex(32)  # Generate a secure random key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Create an instance of the Settings class
settings = Settings()
