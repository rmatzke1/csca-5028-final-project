import os


cfg = {
    "DATABASE_URI": os.getenv("DATABASE_URI"),
    "DATETIME_FORMAT": os.getenv("DATETIME_FORMAT"),
    "REDIS_HOST": os.getenv("REDIS_HOST"),
    "REDIS_PORT": int(os.getenv("REDIS_PORT")),
    "REDIS_SET_KEY": os.getenv("REDIS_SET_KEY"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    "GEMINI_MODEL": os.getenv("GEMINI_MODEL")
}
