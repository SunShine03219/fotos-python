# Templates Backend Projects

Base project templates for backend implementation


---

### Start virtual environment

```bash
pipenv shell
```

### Install dependencies

```bash
pipenv install
```

---

### Start Postgres and PGAdmin

```bash
sudo docker compose up -d
```

**_Only in first RUN_**: _If you haven't a .env file, you must create using below structure_

```
# Change for your user
PG_USER=admin
# Change for your password
PG_PASS=admin
# CONFIGURE BELOW USING YOUR INFORMATIONS CREATED ABOVE
DATABASE_URL=postgresql+asyncpg://admin:admin@localhost:5432/backend
# CONFIGURE BELOW USING YOUR TEST DATABASE INFORMATION
DATABASE_TEST_URL=postgresql+asyncpg://admin:admin@localhost:5432/tests

# Default Admin
NAME="Nome do user"
EMAIL="user@gmail.com"
PASSWORD="1234567"


# Change it for use your secrete key (token generation/validate)
SECRET_KEY=secret

# Change to false when test
PRODUCTION_MODE=True

# Chang it for use your API Cloud Credentials
# Can you generate your service account here: https://console.cloud.google.com/iam-admin/serviceaccounts?
# Give OWNER permissions for this account
# Open your service account and generate a JSON Key, take your credentials and change just bellow
TYPE=""
PROJECT_ID=""
PRIVATE_KEY_ID=""
PRIVATE_KEY=""
CLIENT_EMAIL=""
CLIENT_ID=""
AUTH_URI=""
TOKEN_URI=""
AUTH_PROVIDER_x509_CERT_URL=""
CLIENT_x509_CERT_URL=""

# Change it for use your bucket-name
BUCKET_NAME=""
```

## Start database migration (getting last version)

```bash
alembic upgrade head
```

If you update or create any new model, run it to reflect on database project

```bash
alembic revision --autogenerate -m "your message"
```

---
