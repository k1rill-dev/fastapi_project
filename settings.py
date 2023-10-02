from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:lolkek123@localhost:5432/postgres",
)
APP_PORT: int = env.int("APP_PORT", default=8000)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
SENTRY_URL: str = env.str("SENTRY_URL", default='lol')
