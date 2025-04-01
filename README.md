# CSCA 5028 - Final Project

For my final project, I have decided to create a movie recap application. This application contains:

- **Data Collector** - Pulls latest videos from a collection of YouTube movie recap channels.
- **Data Analyzer** - Analyzes the collected videos to determine things like genre, actors, etc.
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

- [databases/movie-recaps](./databases/movie-recaps/README.md)
- [components](./components/README.md)
- [applications/data-collector](./applications/data-collector/README.md)

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

#### db-migration

| Property             | Value                                                                    |
|----------------------|--------------------------------------------------------------------------|
| Name                 | db-migration                                                             |
| Interpreter          | Select the virtual environment in the `databases/movie-recaps` directory |
| Script               | `/<path-to-project>/databases/movie-recaps/migrate.py`                   |
| Working directory    | `/<path-to-project>/databases/movie-recaps`                              |
| Path to ".env" files | `/<path-to-project>/.local/.env`                                         |

#### data-collector

| Property             | Value                                                                         |
|----------------------|-------------------------------------------------------------------------------|
| Name                 | data-collector                                                                |
| Interpreter          | Select the virtual environment in the `applications/data-collector` directory |
| Script               | `/<path-to-project>/applications/data-collector/src/main.py`                  |
| Working directory    | `/<path-to-project>/applications/data-collector`                              |
| Path to ".env" files | `/<path-to-project>/.local/.env`                                              |

### Database

Run this command to create a local database using the docker compose file.

```
docker-compose -f .local/docker-compose.yml up -d
```

After the database is created, you will need to run the **db-migration** run configuration.
This will execute the database migration scripts which will update your local database to the latest state.

Note that if you have previously created a database and want to start from scratch, you should delete 
the `.docker-data` directory.

### Validation

The following commands can help with formatting, linting, tests, etc.

```
# Linting, formatting, etc.
black --check .
flake8 .
isort --check-only .
pyright .

# Unit tests
coverage run -m unittest discover
coverage report -m      # Print report
coverage html           # Generate HTML report
```