# AI chat application backend

This is a backend part of the application, also check out [frontend](https://github.com/krglkvrmn/openai_api_ui_frontend/tree/main)

## Tech stack

| Component                        | Technology                                                   |
| -------------------------------- | ------------------------------------------------------------ |
| Language                         | [Python 3.10+](https://www.python.org/)                      |
| Routing                          | [FastAPI](https://fastapi.tiangolo.com/)                     |
| Database                         | [PostgreSQL](https://www.postgresql.org/)                    |
| ORM                              | [SQLAlchemy](https://www.sqlalchemy.org/) + [asyncpg](https://magicstack.github.io/asyncpg/current/) |
| Authentication and authorization | Slightly patched [fastapi-users](https://fastapi-users.github.io/fastapi-users/latest/) |
| Data validation                  | [Pydantic](https://docs.pydantic.dev/latest/)                |
| Database migrations              | [Alembic](https://alembic.sqlalchemy.org/en/latest/)         |
| WSGI server                      | [Gunicorn](https://gunicorn.org/)                            |
| Reverse proxy server             | [NGINX](https://nginx.org/en/docs/?_ga=2.65749997.258183107.1714325166-1305194052.1709247764) |

## Usage 🛠️

Usage guide is primarily focused on running the app on **Linux** distributions. Slight adjustments might be needed for MacOS.

First, clone the repository to your local machine by running

```bash
git clone git@github.com:krglkvrmn/openai_api_ui_backend.git
# or
git clone https://github.com/krglkvrmn/openai_api_ui_backend.git
```

Go inside a repository directory

```bash
cd openai_api_ui_backend
```

### Configuration 🎛️

Application heavily relies on external configuration in the form of environment variables

#### Environment variables 📄

In order to simplify application management, almost all configurable parameters can be loaded from **env file**. You can configure env file by first copying and editing a template file

``` bash
cp .env.template .env.dev
```

Template file contains descriptions of all configurable parameters and credentials. You should replace all `<placeholders>` with actual parameter values. Optional parameters are marked with (*****), you can delete them from env file if you want so, these parameters have built-in defaults.

While it is definetely possible to store all parameters in env file, it is better to store sensitive information such as cryptography keys, API keys and passwords in separate files called **secrets**. These parameters are commented in env file.

#### Secrets 🔐

Secret file is just a plain text file containing sensitive information. These files should all be located in a separate directory.

**Configure all required secrets**. Some of those should be configured manually and there is also convenience script for creating and rotating cryptography keys `rotate_crypto_keys.sh`. *File names should be exactly the same*.

```bash
mkdir .secret
# OAuth config format - {"client_id": "<client_id>", "client_secret": "<client_secret>"}
echo "<google_oauth_config>" > .secret/google_oauth_config
echo "<github_oauth_config>" > .secret/github_oauth_config
echo "<postgres_password>" > .secret/postgres_password
echo "<sendgrid_api_key>" > .secret/sendgrid_api_key

chmod +x ./rotate_crypto_keys.sh
./rotate_crypto_keys.sh .secret
```

The application automatically loads secrets from secrets directory and thus it should have access to both secrets directory and env file, so we need to store these paths in environment variables.

```bash
# These variables are required to run everything related to the application
export SECRETS_DIR=".secrets"
export ENV_FILE=".env.dev"
```

### Development setup 🖥️

Development setup requires a few non-python dependencies including [redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/) and [postresql](https://www.postgresql.org/download/). These dependencies should be installed and running.

**Setup a virtual environment**. Note that the supported python versions are `python>=3.10`

```bash
python3 -m venv venv
source venv/bin/activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Set up PostgreSQL database**

```bash
# You may not need sudo -u postgres on MacOS
sudo -u postgres createdb <your_database_name>
sudo -u postgres psql mydatabase
```

**Create postgres user**

```sql
# Inside psql CLI
CREATE USER <your_user_name> WITH ENCRYPTED PASSWORD '<your_password>';
GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_user_name>;
ALTER DATABASE <your_database_name> OWNER TO <your_user_name>;
```

If you haven't done this earlier, **configure environment variables** and **create secrets files**. Fill out all variables in env file and create all required secrets files including one with postgres password.

```bash
# These variables are required to run anything related to an application
export ENV_FILE=<path_to_your_env_file>
export SECRETS_DIR=<path_to_your_secrets_dir>
```

**Apply database migrations**

```bash
alembic upgrade head
```

**Run dev server**

```bash
uvicorn app.main:app --reload
```

### Production setup 🚀

For this setup you need to install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)

Production setup is automated with docker-compose, all you need is to create a **production env file** for your application. This configuration may differ from dev setup

```bash
cp .env.template .env.prod
```

And also you need to create a separate **env file for launching docker-compose**. This file includes reference to file created on previous step `APP_ENV_FILE` and paths to all secret files.

```bash
cp .env.deploy.template .env.deploy.prod
```

**Launch docker-compose** and pass both created files as env-file arguments

```bash
docker compose --env-file .env.prod --env-file .env.deploy.prod build
docker compose --env-file .env.prod --env-file .env.deploy.prod up
```

❗️NGINX configuration and other deploy related code are not incuded in repository for sequrity reasons

## Endpoints

Interactive API docs provided by FastAPI are available at http://localhost:8000/docs#/ by default
