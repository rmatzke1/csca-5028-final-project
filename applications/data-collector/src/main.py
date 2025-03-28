import os

import requests
from dotenv import load_dotenv

from rmatzke.components.videos import video_gateway

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def main():
    print("GET https://youtube.googleapis.com/youtube/v3/channels")
    print("--------------------------")
    response = requests.get(
        url="https://youtube.googleapis.com/youtube/v3/channels",
        params={"part": "snippet", "forHandle": CHANNEL_HANDLE, "maxResults": 1, "key": API_KEY},
    )
    print(response.status_code)
    print(response.text)

    print("GET https://youtube.googleapis.com/youtube/v3/search")
    print("--------------------------")
    response = requests.get(
        url="https://youtube.googleapis.com/youtube/v3/search",
        params={
            "part": "snippet",
            "channelId": CHANNEL_ID,
            "maxResults": 3,
            "order": "date",
            "key": API_KEY,
        },
    )
    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()
