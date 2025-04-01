import json
import redis
import sqlalchemy
from config import cfg
from rmatzke.components.common.templates import DBTemplate


def main():
    # Setup database connections
    # db = sqlalchemy.create_engine(cfg["DATABASE_URI"])
    # db_template = DBTemplate(db)
    rdb = redis.Redis(host=cfg["REDIS_HOST"], port=cfg["REDIS_PORT"], db=0)

    video_data = rdb.smembers("json_set")
    for d in video_data:
        print(json.loads(d))


if __name__ == "__main__":
    main()
