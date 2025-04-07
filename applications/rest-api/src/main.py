import sqlalchemy
import uvicorn
from config import cfg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.genre.genre_gateway import GenreGateway
from rmatzke.components.youtube.youtube_video_gateway import YoutubeVideoGateway
from rmatzke.components.youtube.youtube_video_genre_gateway import YoutubeVideoGenreGateway
from rmatzke.components.youtube.youtube_video_service import YoutubeVideoService


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup database connection
db = sqlalchemy.create_engine(cfg["DATABASE_URI"])
db_template = DBTemplate(db)

# Setup gateways
genre_gateway = GenreGateway(db_template)
youtube_video_gateway = YoutubeVideoGateway(db_template)
youtube_video_genre_gateway = YoutubeVideoGenreGateway(db_template)

# Setup services
youtube_video_service = YoutubeVideoService(
    db=db_template,
    youtube_video_gateway=youtube_video_gateway,
    genre_gateway=genre_gateway,
    youtube_video_genre_gateway=youtube_video_genre_gateway
)


@app.get("/api/health")
def health():
    return { "status": "OK" }


@app.get("/api/genres")
def genres():
    return genre_gateway.list_all()


@app.get("/api/videos")
def videos(genre_id: int = 0):
    if genre_id > 0:
        return youtube_video_service.list_by_genre_id(genre_id)
    return youtube_video_service.list_all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
