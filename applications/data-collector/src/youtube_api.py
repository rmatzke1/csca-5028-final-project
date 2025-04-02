import requests
from config import cfg
from datetime import datetime
from typing import List


def get_channel_id_by_handle(handle: str) -> str:
    response = requests.get(
        url="https://youtube.googleapis.com/youtube/v3/channels",
        params={
            "part": "snippet",
            "forHandle": handle,
            "maxResults": 1,
            "key": cfg["YOUTUBE_API_KEY"],
        },
    )
    # if response.status_code == 403:
    #     raise requests.exceptions.HTTPError("Rate limited!")
    return response.json()["items"][0]["id"]


def get_video_data(channel_id: str, published_before: datetime, published_after: datetime) -> List:
    response = requests.get(
        url="https://youtube.googleapis.com/youtube/v3/search",
        params={
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": 25,
            "order": "date",
            "key": cfg["YOUTUBE_API_KEY"],
            "published_before": published_before.isoformat() + "Z",
            "published_after": published_after.isoformat() + "Z",
        },
    )
    return response.json()["items"]
