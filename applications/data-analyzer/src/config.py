import os


cfg = {
    "DATABASE_URI": os.getenv("DATABASE_URI"),
    "DATETIME_FORMAT": os.getenv("DATETIME_FORMAT"),
    "REDIS_HOST": os.getenv("REDIS_HOST"),
    "REDIS_PORT": int(os.getenv("REDIS_PORT"))
}
