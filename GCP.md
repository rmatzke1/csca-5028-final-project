# Google Cloud Project Setup

## APIs & Services

The following APIs & Services will need to be enabled:
- Artifact Registry API
- Cloud Run Admin API
- Cloud SQL Admin API
- Compute Engine API
- Google Cloud Memorystore for Redis API
- Memorystore API
- Priveleged Access Manager API
- Secret Manager API
- YouTube Data API v3

## Artifact Registry

### docker-dev

Create an Artifact Registry repository with the following:
- Name: docker-dev
- Format: Docker

## Cloud SQL

### postgres-test

Create a Cloud SQL Postgres instance with the following:
- Cloud SQL Edition: Enterprise
- Database Version: PostgreSQL 16
- Instance ID: postgres-test

Once the instance is provisioned:
- Create database **movie_recaps_test**
- Create database user **integration_test_user**

Connect to the database and run the following command:
```grant all privileges on database movie_recaps_test to integration_test_user;```

### postgres-dev

Create a Cloud SQL Postgres instance with the following:
- Cloud SQL Edition: Enterprise
- Database Version: PostgreSQL 16
- Instance ID: postgres-dev

Once the instance is provisioned:
- Create database **movie_recaps_dev**
- Create database user **db_user**

Connect to the database and run the following command:
```grant all privileges on database movie_recaps_dev to db_user;```

## Memorystore

### datastore-dev

Create a Redis Memorystore instance:
- Name: datastore-dev

## Secrets

- DATABASE_URI_DEV = `postgresql+psycopg2://db_user_dev:<password>/movie_recaps_dev?host=/cloudsql/<project id>:<region>:postgres-dev`
- GEMINI_API_KEY = <GEMINI_API_KEY>
- YOUTUBE_API_KEY = <YOUTUBE_API_KEY>

## Cloud Run Jobs

### data-collector-dev

#### General Settings

- Container image URL: Select the data-collector image with "latest" tag
- Job name: data-collector-dev
- Number of tasks: 1

#### Security

- Service account: cloud-run-dev

#### Connections

- Add the **postgres-dev** Cloud SQL connection
- Connect to a VPC for outbound traffic
  - Send traffic directly to a VPC
    - Network: default
    - Subnet: default
  - Route only requests to private IPs to the VPC

#### Volumes

Add a volume for the `YOUTUBE_API_KEY` secret:
- Volume type: Secret
- Volume name: youtube-api-key
- Secret: YOUTUBE_API_KEY
- Path 1: YOUTUBE_API_KEY
- Version 1: latest

Add a volume for the `DATABASE_URI` secret:
- Volume type: Secret
- Volume name: database-uri-dev
- Secret: DATABASE_URI_DEV
- Path 1: DATABASE_URI_DEV
- Version 1: latest
  
#### Containers - Volume Mounts

Mount the `youtube-api-key` volume:
- Name: youtube-api-key (Secret)
- Mount path: /secrets-a

Mount the `database-uri-dev` volume:
- Name: database-uri-dev (Secret)
- Mount path: /secrets-b

#### Containers - Variables & Secrets

Environment variables:
- `DATETIME_FORMAT`: `%Y-%m-%d %H:%M:%S`
- `COLLECTOR_DEFAULT_PUBLISHED_BEFORE`: `2024-01-01 00:00:00`
- `COLLECTOR_RUN_DELTA`: `1`
- `REDIS_HOST`: `<IP of the datastore-dev Redis instance>`
- `REDIS_PORT`: `6379`
- `REDIS_SET_KEY`: `video_data`

Secrets exposed as environment variables:
- Name: `YOUTUBE_API_KEY`, Secret: `YOUTUBE_API_KEY`, Version: latest
- Name: `DATABASE_URI`, Secret: `DATABASE_URI_DEV`, Version: latest

## Service Accounts

The following service accounts and associated roles will need to be created.
You will also need to create and export a JSON key for each service account.

**cloud-registry-dev**
- Artifact Registry Writer

**cloud-run-dev**
- Cloud Run Developer
- Cloud SQL Client

**cloud-sql-dev**
- Cloud SQL Client

**cloud-sql-test**
- Cloud SQL Client
