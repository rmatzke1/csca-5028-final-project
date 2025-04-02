# CSCA 5028 - Final Project

For my final project, I have decided to create a movie recap application. This application contains:

- **Data Collector** - Pulls latest videos from a collection of YouTube movie recap channels.
- **Data Analyzer** - Analyzes the collected recap videos to determine the genre.
- **Web Application** - Frontend for displaying the movie recaps.

## Development

For running this project locally, I would recommend using PyCharm over VS Code for this project.
It is much easier to manage multiple virtual environments / projects in PyCharm.

If you are on Windows, I would suggest changing your default PyCharm terminal to Command Prompt instead of PowerShell.

### Prerequisites

- Python >= 3.10
- Docker
- PyCharm Community Edition

### Environment Variables

This project uses a single `.env` file shared across all subprojects.
In the `.local` directory, copy the `.env.example` file to a new file called `.env`.
Then, fill in all the required values in the file.

### Virtual Environments

Each subproject for this application will use a separate virtual environment.
To set up these virtual environments, follow the instructions in the README file for each subproject below.

- [applications/data-analyzer](./applications/data-analyzer/README.md)
- [applications/data-collector](./applications/data-collector/README.md)
- [applications/rest-api](./applications/rest-api/README.md)
- [components](./components/README.md)
- [databases/movie-recaps](./databases/movie-recaps/README.md)

Note that there is a requirements file in the root of the repository as well as in each subproject.
The one in the root is for project-wide dependencies. This would mostly be things like linting, formatting, etc.
If you want, you can setup another virtual environment in the root so that you can run validation from the root,
covering all the subprojects at once.

### Run Configurations

Several run configurations will be created to run the various subprojects. 
Note that before creating the run configurations, you may need to add the Python interpreter for each virtual
environment to the project. This can be done in File -> Settings -> Project -> Python Interpreter.

Once the virtual environment interpreters have been added, go to Run -> Edit Configurations to create each of
the following Python run configurations.

#### data-analyzer

| Property             | Value                                                                        |
|----------------------|------------------------------------------------------------------------------|
| Name                 | data-analyzer                                                                |
| Interpreter          | Select the virtual environment in the `applications/data-analyzer` directory |
| Script               | `/<path-to-project>/applications/data-analyzer/src/main.py`                  |
| Working directory    | `/<path-to-project>/applications/data-analyzer`                              |
| Path to ".env" files | `/<path-to-project>/.local/.env`                                             |

#### data-collector

| Property             | Value                                                                         |
|----------------------|-------------------------------------------------------------------------------|
| Name                 | data-collector                                                                |
| Interpreter          | Select the virtual environment in the `applications/data-collector` directory |
| Script               | `/<path-to-project>/applications/data-collector/src/main.py`                  |
| Working directory    | `/<path-to-project>/applications/data-collector`                              |
| Path to ".env" files | `/<path-to-project>/.local/.env`                                              |

#### rest-api

| Property             | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| Name                 | rest-api                                                                |
| Interpreter          | Select the virtual environment in the `applications/rest-api` directory |
| Script               | `/<path-to-project>/applications/rest-api/src/main.py`                  |
| Working directory    | `/<path-to-project>/applications/rest-api`                              |
| Path to ".env" files | `/<path-to-project>/.local/.env`                                        |

#### db-migration

| Property             | Value                                                                    |
|----------------------|--------------------------------------------------------------------------|
| Name                 | db-migration                                                             |
| Interpreter          | Select the virtual environment in the `databases/movie-recaps` directory |
| Script               | `/<path-to-project>/databases/movie-recaps/migrate.py`                   |
| Working directory    | `/<path-to-project>/databases/movie-recaps`                              |
| Path to ".env" files | `/<path-to-project>/.local/.env`                                         |

### Docker Container

Run this command to create a container for the application:
```
docker-compose -f .local/docker-compose.yml up -d
```

The first time you create this container, you will also need to run the **db-migration** run configuration.
This will execute the database migration scripts which will update your local database to the latest state.

Additional container management commands:
```
# Stop the container withour removing
docker-compose -f .local/docker-compose.yml stop

# Restart the stopped container
docker-compose -f .local/docker-compose.yml start

# Remove the container
docker-compose -f .local/docker-compose.yml down
```

If you have previously created a container and want to start from scratch, you should delete both the container
and the local `.docker-data` directory before building a new one. 

### Validation

#### Unit Tests

Unit tests will need to be executed from within each subproject directory. See the README for each subproject
for more information.

#### Database Queries

To connect to the PostgreSQL database running in your container, first open the movie-recap-database container 
in Docker Desktop, then navigate to the Exec tab, then enter the following commands:

```
psql -U db_user -d movie_recaps_dev
```

Now you can run psql commands or raw queries, for example:

```
\dt
select * from youtube_channel;
```

#### Datastore Queries

To connect to the Redis datastore running in your container, first open the movie-recap-datastore container 
in Docker Desktop, then navigate to the Exec tab. Below are some sample commands you can run:

```
redis-cli --scan                # List keys
redis-cli TYPE video_data       # Get type of video_data key
redis-cli SMEMBERS video_data   # Get values in video_data set
```


## Credits

- [initialcapacity/multiproject-python](https://github.com/initialcapacity/multiproject-python) - for providing
ideas on how to structure the project/repository, and for providing some boilerplate code.
- [Python Monorepo: An Example](https://www.tweag.io/blog/2023-04-04-python-monorepo-1/) - for providing ideas
on how to structure the project/repository.
