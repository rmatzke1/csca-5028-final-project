# GCP Setup

## APIs & Services

The following APIs & Services will need to be enabled:
- Artifact Registry API
- Cloud Run Admin APII
- Cloud Scheduler AP
- Cloud SQL Admin API
- Compute Engine API
- Google Cloud Memorystore for Redis API
- Memorystore API
- Priveleged Access Manager API
- Secret Manager API
- YouTube Data API v3

## Service Accounts

The following service accounts and associated roles will need to be created.
You will also need to create and export a JSON key for each service account.

**cloud-registry-dev**
- Artifact Registry Writer

**cloud-run-dev**
- Artifact Registry Reader
- Cloud Run Developer
- Cloud Run Invoker
- Cloud SQL Client
- Service Account User

**cloud-sql-dev**
- Cloud SQL Client

**cloud-sql-test**
- Cloud SQL Client

## Cloud SQL

### postgres-test

Create a Cloud SQL Postgres instance with the following:
- Cloud SQL Edition: Enterprise
- Database Version: PostgreSQL 16
- Instance ID: `postgres-test`

Once the instance is provisioned:
- Create database `movie_recaps_test`
- Create database user `integration_test_user`

Connect to the database and run the following command:
```
grant all privileges on database movie_recaps_test to integration_test_user;
```

### postgres-dev

Create a Cloud SQL Postgres instance with the following:
- Cloud SQL Edition: Enterprise
- Database Version: PostgreSQL 16
- Instance ID: `postgres-dev`

Once the instance is provisioned:
- Create database `movie_recaps_dev`
- Create database user `db_user`

Connect to the database and run the following command:
```
grant all privileges on database movie_recaps_dev to db_user;
```

## Memorystore

### datastore-dev

In Memorystore, create a Redis instance:
- Name: `datastore-dev`

## Secrets

In Secret Manager, create the following secrets:
- `DATABASE_URI_DEV`: `postgresql+psycopg2://db_user_dev:<password>/movie_recaps_dev?host=/cloudsql/<project id>:<region>:postgres-dev`
- `GEMINI_API_KEY`: `<GEMINI_API_KEY>`
- `YOUTUBE_API_KEY`: `<YOUTUBE_API_KEY>`

## Artifact Registry

### docker-dev

Create an Artifact Registry repository with the following:
- Name: `docker-dev`
- Format: Docker

## Cloud Run Jobs

In Cloud Run, create the following jobs:

### data-collector-dev

#### General Settings

- Container image URL: Select the `data-collector` image with `latest` tag from the `docker-dev` repository, then remove the tag from the URL
- Job name: `data-collector-dev`
- Number of tasks: 1

#### Security

- Service account: `cloud-run-dev`

#### Connections

- Add the `postgres-dev` Cloud SQL connection
- Connect to a VPC for outbound traffic
  - Send traffic directly to a VPC
    - Network: default
    - Subnet: default
  - Route only requests to private IPs to the VPC

#### Volumes

Add a volume for the `YOUTUBE_API_KEY` secret:
- Volume type: Secret
- Volume name: `youtube-api-key`
- Secret: `YOUTUBE_API_KEY`
- Path: `YOUTUBE_API_KEY`
- Version: latest

Add a volume for the `DATABASE_URI` secret:
- Volume type: Secret
- Volume name: `database-uri-dev`
- Secret: `DATABASE_URI_DEV`
- Path: `DATABASE_URI_DEV`
- Version: latest
  
#### Containers - Volume Mounts

Mount the `youtube-api-key` volume:
- Name: youtube-api-key (Secret)
- Mount path: `/secrets-a`

Mount the `database-uri-dev` volume:
- Name: database-uri-dev (Secret)
- Mount path: `/secrets-b`

#### Containers - Variables & Secrets

Environment variables:
- `DATETIME_FORMAT`: `%Y-%m-%d %H:%M:%S`
- `COLLECTOR_DEFAULT_PUBLISHED_BEFORE`: `2024-01-01 00:00:00`
- `COLLECTOR_RUN_DELTA`: `1`
- `REDIS_HOST`: Enter the IP of the `datastore-dev` Redis instance
- `REDIS_PORT`: `6379`
- `REDIS_SET_KEY`: `video_data`

Secrets exposed as environment variables:
- Name: `YOUTUBE_API_KEY`, Secret: `YOUTUBE_API_KEY`, Version: latest
- Name: `DATABASE_URI`, Secret: `DATABASE_URI_DEV`, Version: latest

### data-analyzer-dev

#### General Settings

- Container image URL: Select the `data-analyzer` image with `latest` tag from the `docker-dev` repository, then remove the tag from the URL
- Job name: `data-analyzer-dev`
- Number of tasks: 5

#### Security

- Service account: `cloud-run-dev`

#### Connections

- Add the `postgres-dev` Cloud SQL connection
- Connect to a VPC for outbound traffic
  - Send traffic directly to a VPC
    - Network: default
    - Subnet: default
  - Route only requests to private IPs to the VPC

#### Volumes

Add a volume for the `GEMINI_API_KEY` secret:
- Volume type: Secret
- Volume name: `gemini-api-key`
- Secret: `GEMINI_API_KEY`
- Path: `GEMINI_API_KEY`
- Version: latest

Add a volume for the `DATABASE_URI` secret:
- Volume type: Secret
- Volume name: `database-uri-dev`
- Secret: `DATABASE_URI_DEV`
- Path: `DATABASE_URI_DEV`
- Version: latest

#### Containers - Volume Mounts

Mount the `gemini-api-key` volume:
- Name: gemini-api-key (Secret)
- Mount path: `/secrets-a`

Mount the `database-uri-dev` volume:
- Name: database-uri-dev (Secret)
- Mount path: `/secrets-b`

#### Containers - Variables & Secrets

Environment variables:
- `DATETIME_FORMAT`: `%Y-%m-%d %H:%M:%S`
- `REDIS_HOST`: Enter the IP of the `datastore-dev` Redis instance
- `REDIS_PORT`: `6379`
- `REDIS_SET_KEY`: `video_data`
- `GEMINI_MODEL`: `gemini-2.0-flash`

Secrets exposed as environment variables:
- Name: `GEMINI_API_KEY`, Secret: `GEMINI_API_KEY`, Version: latest
- Name: `DATABASE_URI`, Secret: `DATABASE_URI_DEV`, Version: latest

## Cloud Run Services

In Cloud Run, create the following services:

### rest-api

#### General Settings

- Container image URL: Select the latest `rest-api` image from the `docker-dev` repository
- Service name: `rest-api-dev`
- Uncheck "Use Cloud IAM to authenticate incoming requests"
- Manual Scaling, Number of instances: 1
- Ingress: All

Add a Cloud SQL connection for the `postgres-dev` database.

#### Container Settings

- Container port: 8000
- Startup probe: tcp 8000 every 240s
  - Initial delay: 0s
  - Timeout: 240s
  - Failure threshold: 1
- Liveness probe: http /api/health every 120s
  - Initial delay: 30s
  - Timeout: 3s
  - Failure threshold: 3

#### Container Settings - Security

- Service account: `cloud-run-dev`

#### Container Settings - Volumes

Add a volume for the `DATABASE_URI` secret:
- Volume type: Secret
- Volume name: `database-uri-dev`
- Secret: `DATABASE_URI_DEV`
- Path: `DATABASE_URI_DEV`
- Version: latest

#### Container Settings - Volume Mounts

Mount the `database-uri-dev` volume:
- Name: database-uri-dev (Secret)
- Mount path: `/secrets-a`

#### Container Settings - Variables & Secrets

Secrets exposed as environment variables:
- Name: `DATABASE_URI`, Secret: `DATABASE_URI_DEV`, Version: latest

### web-ui

#### General Settings

- Container image URL: Select the latest `web-ui` image from the `docker-dev` repository
- Service name: `web-ui-dev`
- Uncheck "Use Cloud IAM to authenticate incoming requests"
- Manual Scaling, Number of instances: 1
- Ingress: All

#### Container Settings

- Container port: 3000

#### Container Settings - Security

- Service account: `cloud-run-dev`
