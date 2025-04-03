import json
import redis
import sqlalchemy
from config import cfg
from google import genai
from rmatzke.components.common.templates import DBTemplate
from rmatzke.components.genre.genre_gateway import GenreGateway
from rmatzke.components.youtube.youtube_video_gateway import YoutubeVideoGateway
from rmatzke.components.youtube.youtube_video_genre_gateway import YoutubeVideoGenreGateway


def main():
    # Setup database and Gemini connections
    db = sqlalchemy.create_engine(cfg["DATABASE_URI"])
    db_template = DBTemplate(db)
    rdb = redis.Redis(host=cfg["REDIS_HOST"], port=cfg["REDIS_PORT"], db=0)
    gemini_client = genai.Client(api_key=cfg["GEMINI_API_KEY"])

    # Setup database gateway
    genre_gateway = GenreGateway(db_template)
    youtube_video_gateway = YoutubeVideoGateway(db_template)
    youtube_video_genre_gateway = YoutubeVideoGenreGateway(db_template)

    # Get the list of genres
    genres = genre_gateway.list_all()
    genres_prompt_str = ", ".join([g.genre for g in genres])

    # Get the video data
    video_record = rdb.spop(cfg["REDIS_SET_KEY"])
    if not video_record:
        print("No videos available to analyze. Exiting.")
        exit()

    video_data = json.loads(video_record)
    video_title = video_data['snippet']['title']
    video_description = video_data['snippet']['description']

    # Ask Gemini to determine the genre
    prompt = f"""
            Based on the title and description, what genres is this movie likely to be?
            Please provide only a comma separate list of genres as your response.
            Please select only from the following genres: {genres_prompt_str}
            Please select a minimum of 1 and a maximum of 3 genres.
            Title: {video_title}
            Description: {video_description}
        """
    response = gemini_client.models.generate_content(
        model=cfg["GEMINI_MODEL"],
        contents=prompt
    )
    suggested_genres = [g.strip() for g in response.text.split(",")]

    # Insert the video record
    youtube_video_record = youtube_video_gateway.insert(
        youtube_video_id=video_data['id']['videoId'],
        youtube_channel_id=video_data['snippet']['channelId'],
        title=video_title,
        description=video_description,
        publish_date=video_data['snippet']['publishedAt'],
        thumbnail_url=video_data['snippet']['thumbnails']['medium']['url']
    )
    print(f'Inserted youtube_video record with id {youtube_video_record.id}')

    # Insert the video genre records
    for genre in suggested_genres:
        genre_id = [g.id for g in genres if g.genre == genre][0]
        youtube_video_genre_gateway.insert(genre_id, youtube_video_record.id)
        print(f'Inserted youtube_video_genre record with genre_id {genre_id} ({genre})')


if __name__ == "__main__":
    main()
