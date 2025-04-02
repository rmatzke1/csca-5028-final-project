import json
import redis
import sqlalchemy
import youtube_api
from config import cfg
from datetime import datetime, timedelta
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.collector.collector_run_gateway import CollectorRunGateway
from rmatzke.components.youtube.youtube_channel_gateway import YoutubeChannelGateway


def main():
    # Setup database connections
    db = sqlalchemy.create_engine(cfg["DATABASE_URI"])
    db_template = DBTemplate(db)
    rdb = redis.Redis(host=cfg["REDIS_HOST"], port=cfg["REDIS_PORT"], db=0)

    # Setup database gateways
    collector_run_gateway = CollectorRunGateway(db_template)
    youtube_channel_gateway = YoutubeChannelGateway(db_template)

    # Retrieve and store the YouTube channel ID for any newly added channels
    new_youtube_channels = youtube_channel_gateway.list_without_channel_ids()
    for channel in new_youtube_channels:
        youtube_channel_id = youtube_api.get_channel_id_by_handle(channel.youtube_handle)
        youtube_channel_gateway.set_channel_id(channel.id, youtube_channel_id)
        print(f'Set youtube_channel.youtube_channel_id to {youtube_channel_id} for handle {channel.youtube_handle}')

    # Get latest run and determine publish date parameters
    latest_run = collector_run_gateway.get_latest()
    if latest_run:
        published_before = latest_run.param_published_before + timedelta(days=cfg["COLLECTOR_RUN_DELTA"])
        published_after = latest_run.param_published_before
    else:
        published_before = datetime.strptime(cfg["COLLECTOR_DEFAULT_PUBLISHED_BEFORE"], cfg["DATETIME_FORMAT"])
        published_after = published_before - timedelta(days=cfg["COLLECTOR_RUN_DELTA"])

    if published_after > datetime.now():
        print("All currently published video have already been collected. Exiting...")
        exit()

    run_start = datetime.now()
    total_video_count = 0

    # Loop through all channels to find videos and store video data
    youtube_channels = youtube_channel_gateway.list_with_channel_ids()
    for channel in youtube_channels:
        video_data = youtube_api.get_video_data(channel.youtube_channel_id, published_before, published_after)
        for item in video_data:
            rdb.sadd(cfg["REDIS_SET_KEY"], json.dumps(item))
        total_video_count += len(video_data)
        print(f"Found {len(video_data)} videos for channel @{channel.youtube_handle} published between {published_after} and {published_before}.")

    run_end = datetime.now()
    collector_run_gateway.insert(run_start, run_end, published_before, published_after, total_video_count)
    print(f"Run started at {run_start}, ended at {run_end}, and found {total_video_count} total videos.")


if __name__ == "__main__":
    main()
