import os


cfg = {
    "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
    "DATABASE_URI": os.getenv("DATABASE_URI"),
    "DATETIME_FORMAT": os.getenv("DATETIME_FORMAT"),
    "COLLECTOR_DEFAULT_PUBLISHED_BEFORE": os.getenv("COLLECTOR_DEFAULT_PUBLISHED_BEFORE"),
    "COLLECTOR_RUN_DELTA": int(os.getenv("COLLECTOR_RUN_DELTA")),
    "REDIS_HOST": os.getenv("REDIS_HOST"),
    "REDIS_PORT": int(os.getenv("REDIS_PORT")),
    "REDIS_SET_KEY": os.getenv("REDIS_SET_KEY")
}
