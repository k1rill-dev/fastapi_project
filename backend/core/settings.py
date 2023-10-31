from envparse import Env

env = Env()

env.read_envfile()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="loh",
)
DATABASE_URL_ALEMBIC = env.str(
    "DATABASE_URL_ALEMBIC",
    default="loh",
)
APP_PORT = env.int("APP_PORT")
SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
SECRET_KEY_REFRESH: str = env.str("SECRET_KEY_REFRESH", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=1)
REFRESH_TOKEN_EXPIRE_DAYS: int = env.int("REFRESH_TOKEN_EXPIRE_DAYS", default=228)
SENTRY_URL: str = env.str("SENTRY_URL")
