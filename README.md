# CSCA 5028 - Final Project

For my final project, I have decided to create a movie recap aggregator.
This project contains the following applications:

- **Data Collector** - Pulls latest videos from a collection of YouTube movie recap channels.
- **Data Analyzer** - Analyzes the collected videos data to determine the genre.
- **REST API** - Backend for serving data to the frontend via REST.
- **Web UI** - Frontend for displaying analyzed video data to end users.

Additionally, this project contains some reusable components, like database migration scripts and data access modules.

## Development

For running this project locally, I would recommend using PyCharm over VS Code. It is much easier to manage multiple 
virtual environments / projects in PyCharm, and the Run Configuration feature will be heavily used.

If you are on Windows, I would suggest changing your default PyCharm terminal to Command Prompt instead of PowerShell.

### Prerequisites

- Python >= 3.10
- Node.js >= 18.18
- Docker Desktop
- PyCharm Community Edition

### Environment Variables

In the `.local` directory, copy the `.env.example` file to a new file called `.env`.
Then, fill in all the required values in the file. 
Each application in this project (except the web-ui) uses this same `.env` file.

In the `applications/web-ui` directory, create a new file called `.env` and fill in with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Virtual Environments

Each subproject will use a separate virtual environment.
To set up these virtual environments, follow the instructions in the README file for each subproject below.

- [applications/data-analyzer](./applications/data-analyzer/README.md)
- [applications/data-collector](./applications/data-collector/README.md)
- [applications/rest-api](./applications/rest-api/README.md)
- [components](./components/README.md)
- [databases/movie-recaps](./databases/movie-recaps/README.md)

### Run Configurations

Several run configurations will be created to run the various applications locally. 
Note that before creating the run configurations, you may need to add the Python interpreter for each virtual
environment to the project. This can be done in File -> Settings -> Project -> Python Interpreter.

Once the virtual environment interpreters have been added, go to Run -> Edit Configurations to create each of
the following Python run configurations.

#### data-analyzer

| Property              | Value                                                                                                |
|-----------------------|------------------------------------------------------------------------------------------------------|
| Name                  | data-analyzer                                                                                        |
| Interpreter           | Select the Python executable in the `/<path-to-project>/applications/data-analyzer/.venv/` directory |
| Script                | `/<path-to-project>/applications/data-analyzer/src/main.py`                                          |
| Working directory     | `/<path-to-project>/applications/data-analyzer`                                                      |
| Environment variables | `PYTHONBUFFERED=1;`                                                                                  |
| Path to ".env" files  | `/<path-to-project>/.local/.env`                                                                     |

#### data-collector

| Property              | Value                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------|
| Name                  | data-collector                                                                                        |
| Interpreter           | Select the Python executable in the `/<path-to-project>/applications/data-collector/.venv/` directory |
| Script                | `/<path-to-project>/applications/data-collector/src/main.py`                                          |
| Working directory     | `/<path-to-project>/applications/data-collector`                                                      |
| Environment variables | `PYTHONBUFFERED=1;`                                                                                   |
| Path to ".env" files  | `/<path-to-project>/.local/.env`                                                                      |

#### rest-api

| Property              | Value                                                                                           |
|-----------------------|-------------------------------------------------------------------------------------------------|
| Name                  | rest-api                                                                                        |
| Interpreter           | Select the Python executable in the `/<path-to-project>/applications/rest-api/.venv/` directory |
| Script                | `/<path-to-project>/applications/rest-api/src/main.py`                                          |
| Working directory     | `/<path-to-project>/applications/rest-api`                                                      |
| Environment variables | `PYTHONBUFFERED=1;`                                                                             |
| Path to ".env" files  | `/<path-to-project>/.local/.env`                                                                |

#### db-migration

| Property               | Value                                                                                                   |
|------------------------|---------------------------------------------------------------------------------------------------------|
| Name                   | db-migration                                                                                            |
| Interpreter            | Select the Python executable in the `/<path-to-project>/databases/movie-recaps/.venv/` directory        |
| Script                 | `/<path-to-project>/databases/movie-recaps/migrate.py`                                                  |
| Working directory      | `/<path-to-project>/databases/movie-recaps`                                                             |
| Environment variables  | `PYTHONBUFFERED=1;DATABASE_URI=postgresql+psycopg2://db_user:password@localhost:5432/movie_recaps_dev;` |
| Path to ".env" files   |                                                                                                         |

#### db-migration [test]

| Property               | Value                                                                                                    |
|------------------------|----------------------------------------------------------------------------------------------------------|
| Name                   | db-migration                                                                                             |
| Interpreter            | Select the Python executable in the `/<path-to-project>/databases/movie-recaps/.venv/` directory         |
| Script                 | `/<path-to-project>/databases/movie-recaps/migrate.py`                                                   |
| Working directory      | `/<path-to-project>/databases/movie-recaps`                                                              |
| Environment variables  | `PYTHONBUFFERED=1;DATABASE_URI=postgresql+psycopg2://db_user:password@localhost:5432/movie_recaps_test;` |
| Path to ".env" files   |                                                                                                          |

## Execution

### Docker Container

Run this command to create a container for the application:
```
docker-compose -f .local/docker-compose.yml up -d
```

The first time you create this container, you will need to run the **db-migration** run configuration.
This will execute the database migration scripts which will update your local database to the latest state.
You should also run the **db-migration [test]** run configuration so that the test database is up to date.

If you have previously created a container and want to start from scratch, you should delete both the container
and the local `.docker-data` directory before building a new one.

### Local Execution

If you want to run any of the subprojects locally instead of in the docker container, you can follow the steps below.

The general process would be:
- Start the docker container and execute the **db-migration** run configuration, if you haven't already.
- Stop all containers except for the **database** and **datastore** containers.
- Execute the **data-collector** run configuration several times to collect data.
- Execute the **data-analyzer** run configuration several times to analyze the collected data.
- Start the REST API by executing the **rest-api** run configuration.
- Run the frontend web UI and navigate to http://localhost:3000 in a browser.

Note that there is no run configuration for the frontend web UI. Follow the web-ui
[README](./applications/web-ui/README.md) for setup instructions.
