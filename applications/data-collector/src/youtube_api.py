import requests
from config import cfg
from datetime import datetime
from typing import List, Union


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
    return response.json()["items"][0]["id"]


def get_video_data(channel_id: str, published_before: datetime, published_after: datetime) -> Union[List, None]:
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
        }
    )
    response_json = response.json()
    if "items" not in response_json:
        print(f"Unexpected response: {response_json}")
        return None

    return response_json["items"]
