import sqlalchemy
import uvicorn
from config import cfg
from fastapi import FastAPI
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.genre.genre_gateway import GenreGateway
from rmatzke.components.youtube.youtube_video_gateway import YoutubeVideoGateway


app = FastAPI()

db = sqlalchemy.create_engine(cfg["DATABASE_URI"])
db_template = DBTemplate(db)

genre_gateway = GenreGateway(db_template)
youtube_video_gateway = YoutubeVideoGateway(db_template)


@app.get("/api/videos")
def videos():
    return youtube_video_gateway.list_all()


@app.get("/api/genres")
def genres():
    return genre_gateway.list_all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
