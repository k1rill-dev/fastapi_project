from envparse import Env

env = Env()

env.read_envfile()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="loh",
)
APP_PORT = env.int("APP_PORT")
SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
SENTRY_URL: str = env.str("SENTRY_URL")
