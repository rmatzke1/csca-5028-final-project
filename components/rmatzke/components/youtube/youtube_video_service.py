from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union
from sqlalchemy import Connection
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.genre.genre_gateway import GenreGateway
from rmatzke.components.youtube.youtube_video_gateway import YoutubeVideoGateway
from rmatzke.components.youtube.youtube_video_genre_gateway import YoutubeVideoGenreGateway


@dataclass
class Genre:
    id: int
    genre: str


@dataclass
class YoutubeVideo:
    id: int
    youtube_video_id: str
    youtube_channel_id: str
    title: str
    description: str
    publish_date: datetime
    thumbnail_url: str
    genres: List[Genre]


class YoutubeVideoService:
    def __init__(
            self,
            db: DBTemplate,
            youtube_video_gateway: YoutubeVideoGateway,
            genre_gateway: GenreGateway,
            youtube_video_genre_gateway: YoutubeVideoGenreGateway
    ):
        self.__db = db
        self.youtube_video_gateway = youtube_video_gateway
        self.genre_gateway = genre_gateway
        self.youtube_video_genre_gateway = youtube_video_genre_gateway

    def list_all(self) -> List[YoutubeVideo]:
        result = []
        with self.__db.begin() as conn:
            video_records = self.youtube_video_gateway.list_all(conn=conn)
            for video_record in video_records:
                video_genre_records = self.youtube_video_genre_gateway.list_by_youtube_video_id(
                    youtube_video_id=video_record.id,
                    conn=conn
                )
                genres = []
                for video_genre_record in video_genre_records:
                    genre_record = self.genre_gateway.get_by_id(
                        id=video_genre_record.genre_id,
                        conn=conn
                    )
                    genres.append(Genre(id=genre_record.id, genre=genre_record.genre))

                result.append(YoutubeVideo(
                    id = video_record.id,
                    youtube_video_id = video_record.youtube_video_id,
                    youtube_channel_id = video_record.youtube_channel_id,
                    title = video_record.title,
                    description = video_record.description,
                    publish_date= video_record.publish_date,
                    thumbnail_url= video_record.thumbnail_url,
                    genres = genres
                ))
        return result

    def list_by_genre_id(self, genre_id: int) -> List[YoutubeVideo]:
        result = []
        with self.__db.begin() as conn:
            genre_records_by_genre_id = self.youtube_video_genre_gateway.list_by_genre_id(
                genre_id=genre_id,
                conn=conn
            )

            for video_genre_record in genre_records_by_genre_id:
                video_id = video_genre_record.youtube_video_id
                video_record = self.youtube_video_gateway.get_by_id(video_id)
                video_genre_records = self.youtube_video_genre_gateway.list_by_youtube_video_id(
                    youtube_video_id=video_record.id,
                    conn=conn
                )

                genres = []
                for video_genre_record_for_video in video_genre_records:
                    genre_record = self.genre_gateway.get_by_id(
                        id=video_genre_record_for_video.genre_id,
                        conn=conn
                    )
                    genres.append(Genre(id=genre_record.id, genre=genre_record.genre))

                result.append(YoutubeVideo(
                    id = video_record.id,
                    youtube_video_id = video_record.youtube_video_id,
                    youtube_channel_id = video_record.youtube_channel_id,
                    title = video_record.title,
                    description = video_record.description,
                    publish_date= video_record.publish_date,
                    thumbnail_url= video_record.thumbnail_url,
                    genres = genres
                ))
        return result
