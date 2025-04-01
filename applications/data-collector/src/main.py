import api
import json
import redis
import sqlalchemy
from config import cfg
from datetime import datetime, timedelta
from rmatzke.components.collector.collector_run_gateway import CollectorRunGateway
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.youtube.youtube_channel_gateway import YoutubeChannelGateway


def main():
    # Setup database connections
    db = sqlalchemy.create_engine(cfg["DATABASE_URI"])
    db_template = DBTemplate(db)
    rdb = redis.Redis(host=cfg["REDIS_HOST"], port=cfg["REDIS_PORT"], db=0)

    collector_run_gateway = CollectorRunGateway(db_template)
    youtube_channel_gateway = YoutubeChannelGateway(db_template)

    # Get latest run and determine publish data parameters
    latest_run = collector_run_gateway.get_latest()
    if latest_run:
        published_before = latest_run.param_published_before + timedelta(days=cfg["COLLECTOR_RUN_DELTA"])
        published_after = latest_run.param_published_before
    else:
        published_before = datetime.strptime(cfg["COLLECTOR_DEFAULT_PUBLISHED_BEFORE"], cfg["DATETIME_FORMAT"])
        published_after = published_before - timedelta(days=cfg["COLLECTOR_RUN_DELTA"])

    run_start = datetime.now()
    total_video_count = 0

    # Loop through all channels to find videos and store video data
    youtube_channels = youtube_channel_gateway.list_all()
    for channel in youtube_channels:
        channel_id = api.get_channel_id_by_handle(channel.handle)

        video_data = api.get_video_data(channel_id, published_before, published_after)
        for item in video_data:
            rdb.sadd("json_set", json.dumps(item))
        total_video_count += len(video_data)
        print(f"Found {len(video_data)} videos for channel @{channel.handle} published between {published_after} and {published_before}.")

    run_end = datetime.now()
    collector_run_gateway.insert(run_start, run_end, published_before, published_after, total_video_count)
    print(f"Run started at {run_start}, ended at {run_end}, and found {total_video_count} total videos.")

    # Get data from Redis
    video_data_items = rdb.smembers("json_set")
    for i in video_data_items:
        print(json.loads(i))
        break


if __name__ == "__main__":
    main()
