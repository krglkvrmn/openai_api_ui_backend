# AI chat application backend

## Usage

Usage guide is primarily focused on running the app on Linux distributions

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

### Configuration

Application heavily relies on external configuration in the form of environment variables

#### Environment variables

In order to simplify application management, almost all configurable parameters can be loaded from env file. You can configure such file by first copying and editing a template file

``` bash
cp .env.template .env.dev
```

Template file contains descriptions of all configurable parameters and credentials. You should replace all `<placeholders>` with actual parameters. Optional parameters are marked with (*), you can delete them from env file if you want so, these parameters have built-in defaults.

While it is definetely possible to store all parameters in env file, it is better to store sensitive information such as cryptography keys, API keys and passwords in separate files called **secrets**. These parameters are commented in env file.

#### Secrets

Secret file is just a plain text file containing some sensitive information. These files should all be located in a separate directory.

Configure all required secrets. Some of those should be configured manually and there is also convenience script for creating and rotating cryptography keys `rotate_crypto_keys.sh`. File names should be exactly the same

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
export SECRETS_DIR=".secrets"
export ENV_FILE=".env.dev"
```

### Development setup

#### Dependencies

Development setup requires a few non-python dependencies including [redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/) and [postresql](https://www.postgresql.org/download/). These dependencies should be installed and running.

Setup a virtual environment. Note that the supported python versions are `python>=3.10`

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Set up PostgreSQL database

```bash
sudo -u postgres createdb <your_database_name>
sudo -u postgres psql mydatabase
```

Create postgres user

```sql
CREATE USER <your_user_name> WITH ENCRYPTED PASSWORD '<your_password>';
GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_user_name>;
ALTER DATABASE <your_database_name> OWNER TO <your_user_name>;
```

If you haven't done this earlier, configure environment variables and create secrets files. Fill out all variables in env file and create a secrets files including one with postgres password.

```bash
# These variables are required to run anything related to an application
export ENV_FILE=<path_to_your_env_file>
export SECRETS_DIR=<path_to_your_secrets_dir>
```

Apply migrations

```bash
alembic upgrade head
```

Run dev server

```bash
uvicorn app.main:app --reload
```

### Production setup

Production setup is automated with docker-compose, all you need is to create a production env file for your application. This configuration may differ from dev setup

```bash
cp .env.template .env.prod
```

And also you need to create a separate env file for launching docker-compose. This file includes reference to file created on previous step `APP_ENV_FILE` and paths to all secret files.

```bash
cp .env.deploy.template .env.deploy.prod
```

Launch docker-compose with passing both created files as env-file arguments

```bash
docker compose --env-file .env.prod --env-file .env.deploy.prod build
docker compose --env-file .env.prod --env-file .env.deploy.prod up
```

## Endpoints

An interactive API docs provided by FastAPI are available at http://localhost:8000/docs#/ by default
