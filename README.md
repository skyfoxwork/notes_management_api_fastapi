# "Notes Management API"

## Description
This is an API for managing notes built with FastAPI.
It allows you to create, update, delete, and retrieve notes, as well as analyze and summarize them using generative AI models.
The project uses SQLite and PostgreSQL databases to store data and provides Docker support for containerization.

### Directory Tree

```plaintext
.
├── Dockerfile
├── README.MD
├── alembic.ini
├── docker-compose.yml
├── pytest.ini
└── src
    ├── config
    │   ├── __init__.py
    │   ├── dependencies.py
    │   └── settings.py
    ├── database
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── README
    │   │   ├── env.py
    │   │   ├── script.py.mako
    │   │   └── versions
    │   │       ├── 2da0dc469be8_temp_migration.py
    │   │       ├── 32b1054a69e3_initial_migration.py
    │   │       └── 41cdafa531cf_temp_migration.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   ├── accounts.py
    │   │   ├── base.py
    │   │   └── notes.py
    │   ├── session_postgresql.py
    │   ├── session_sqlite.py
    │   └── validators
    │       ├── __init__.py
    │       └── accounts.py
    ├── exceptions
    │   ├── __init__.py
    │   └── security.py
    ├── main.py
    ├── routes
    │   ├── __init__.py
    │   ├── accounts.py
    │   ├── ai.py
    │   ├── analytics.py
    │   └── notes.py
    ├── schemas
    │   ├── __init__.py
    │   ├── accounts.py
    │   └── notes.py
    ├── security
    │   ├── __init__.py
    │   ├── http.py
    │   ├── interfaces.py
    │   ├── passwords.py
    │   ├── token_manager.py
    │   └── utils.py
    ├── services
    │   ├── __init__.py
    │   ├── accounts.py
    │   ├── ai.py
    │   └── analytics.py
    └── tests
        ├── __init__.py
        ├── conftest.py
        ├── test_accounts.py
        ├── test_ai.py
        ├── test_analytics.py
        └── test_notes.py

```

### Directory and File Descriptions

Below is a detailed description of each directory and its contents to help you navigate and understand the project's structure.

### **Root Directory**

- **`README.MD`**: Main project documentation.
- **`Dockerfile`**: Defines the Docker image configuration for the application, including base image, dependencies, and startup commands.
- **`docker-compose.yml`**: Configures the main application services using PostgreSQL, FastAPI,
- **`alembic.ini`**: Configuration file for Alembic, a database migration tool used with SQLAlchemy.
- **`Makefile`**: Automates common development tasks such as setting up the environment, running tests, managing database migrations, linting code, and building Docker images.
- **`requirements.txt`**: is a file that lists all the Python dependencies required for a project.
- **`.flake8`**: is a configuration file for the Flake8 tool
- **`.env.sample`**: file is a template that contains environment variable keys and sample values, which are used for configuring application settings (like database credentials, API keys, etc.). It's meant to be copied to .env and customized for your local environment.
- **`.gitignore`**: file specifies which files and directories Git should ignore when committing code to a repository.

### **Source Directory (`src/`)**

The core source code of the application, organized into various modules and components for maintainability and scalability.

#### **Configuration (`src/config/`)**

Handles application configurations and dependencies.

- **`__init__.py`**: Initializes the `config` module.
- **`dependencies.py`**: Defines dependencies for the application, often used with FastAPI for dependency injection.
- **`settings.py`**: Manages application settings, possibly using environment variables for configuration.

#### **Database (`src/database/`)**

Manages database interactions, migrations, and models.

- **`__init__.py`**: Initializes the `database` module.
- **`migrations/`**: Contains Alembic migration scripts to manage database schema changes.
  - **`README`**: Documentation related to database migrations.
  - **`env.py`**: Alembic environment configuration.
  - **`script.py.mako`**: Template for generating migration scripts.
  - **`versions/`**: Contains individual migration scripts.
    - **`2da0dc469be8_temp_migration.py`**: Temporary migration script.
    - **`32b1054a69e3_initial_migration.py`**: Initial migration script setting up the base schema.
    - **`41cdafa531cf_temp_migration.py`**: Another temporary migration script.
- **`models/`**: Defines the database models using SQLAlchemy.
  - **`__init__.py`**: Initializes the `models` module.
  - **`accounts.py`**: Defines the `Account` model and related database structures.
  - **`base.py`**: Base model definitions and common configurations.
  - **`notes.py`**: Defines the `Note` model and related database structures.
- **`session_postgresql.py`**: Manages PostgreSQL database sessions.
- **`session_sqlite.py`**: Manages SQLite database sessions for development or testing.

#### **Exceptions (`src/exceptions/`)**

Defines custom exception classes to handle various error scenarios within the application.

- **`__init__.py`**: Initializes the `exceptions` module.
- **`security.py`**: Exceptions related to security and authentication.

##### `src/main.py`

The main entry point of the application, typically initializing the FastAPI app, including middleware, routers, and other configurations.

#### **Routes (`src/routes/`)**

Defines the API endpoints and their respective handlers.

- **`__init__.py`**: Initializes the `routes` module.
- **`accounts.py`**: Routes related to user accounts (e.g., registration, login).
- **`notes.py`**: Routes related to note data (e.g., listing, details).
- **`ai.py`**: Routes related to ai (genai) summarizing.
- **`analytics.py`**: Routes related to data analytics.

#### **Schemas (`src/schemas/`)**

Defines the data schemas using Pydantic for request validation and response models.

- **`__init__.py`**: Initializes the `schemas` module.
- **`accounts.py`**: Schemas for account-related operations.
- **`notes.py`**: Schemas for note-related operations.

#### **Security (`src/security/`)**

Manages authentication, authorization, and security-related functionalities.

- **`__init__.py`**: Initializes the `security` module.
- **`http.py`**: Handles HTTP security configurations, possibly OAuth or JWT setups.
- **`interfaces.py`**: Defines interfaces for security components.
- **`passwords.py`**: Functions for hashing and verifying passwords.
- **`token_manager.py`**: Manages token creation, validation, and refreshing.
- **`utils.py`**: Utility functions related to security.

#### **Services (`src/services`)**

Business logic for routes.

- **`__init__.py`**: Initializes the `storages` module.
- **`accounts.py`**: Interaction with JWT (json web token).
- **`ai.py`**: Interaction with Gemini.
- **`analytics.py`**: Text analytics (NumPy/Pandas/NLTK).

#### **Testing (`src/tests/`)**

Contains all test cases to ensure the application's reliability and correctness.

- **`__init__.py`**: Initializes the `tests` module.
- **`conftest.py`**: Configuration file for pytest, defining fixtures and plugins.
- **`test_accounts.py`**: Integration tests for account-related operations.
- **`test_notess.py`**: Integration tests for note-related operations.
- **`test_ai.py`**: Integration tests for ai-related operations.
- **`test_analytics.py`**: Integration tests for analytics-related operations.
- **`utils.py`**: Test utility.
---

---
### **Make commands (Makefile):**
```shell
make run         # Starts the FastAPI server
make test        # Runs tests
make lint        # Checks the code with linters
make migrate     # Creates a new migration
make upgrade     # Applies migrations
make downgrade   # Rolls back the migration
make docker-up   # Builds and starts containers
make docker-down # Builds and starts containers

```
---
### **How to Run the Project**

Follow these steps to set up and run the project on your local machine.
You can run project with 2 ways (with Docker or with Postgres directly)

---
## **Run the Project with Docker**

Install Python3:

```shell
www.python.org/
```

Install Git:

```shell
git-scm.com/
```

## **1. Clone the Repository**

Start by cloning the project repository from GitHub:

```bash
git clone https://github.com/skyfoxwork/notes_management_api_fastapi.git
```
```shell
cd notes_management_api_fastapi
```

```shell
git checkout develop
```
---

## **2. Create and Activate a Virtual Environment**

It is recommended to use a virtual environment to isolate project dependencies:

Create virtual environment:

```shell
python3 -m venv venv
```

Activate virtual environment (venv).

MacOS, Linux:

```shell
source venv/bin/activate
```
   Windows:

```shell
venv\Scripts\activate
```

if you need to deactivate virtual environment use:

```shell
deactivate
```

---

## **3. Install Dependencies with Poetry**

```shell
pip install -r requirements.txt
```

---

## **4. Create a `.env` File**

Create a .env file in the root of the project and add the following environment variables:

Create .env file
```shell
cp .env.sample .env
```

```env
# PostgreSQL
POSTGRES_DB_NAME=<your_db_name>
POSTGRES_DB_PORT=5432
POSTGRES_USER=<your_db_user>
POSTGRES_PASSWORD=<your_db_password>
POSTGRES_HOST=<your_db_host>

# Gemini
GEMINI_API_KEY=<your_gemini_key>

# JWT
SECRET_KEY_ACCESS=838qKq7dGp34hWij3c8txA5ZD2qm9ybt
SECRET_KEY_REFRESH=cFzRk8kllHMW71wQKLXBqDzl24fkhisw
JWT_SIGNING_ALGORITHM=HS256

# Docker
PGDATA=/var/lib/postgresql/data
```

---

## **5. Run the Project with Docker Compose**

The project is **Dockerized** for easy setup. To start all the required services (**PostgreSQL, pgAdmin, FastAPI app, MailHog, MinIO, and Alembic migrator**), run:

(Linux, MacOS)
```bash
make docker-up
```
or
(Linux, MacOS, Windows)
```bash
docker-compose up --build
```
#### Stop project
```bash
make docker-down
```
or
(Linux, MacOS, Windows)
```bash
docker-compose down
```
---

## **6. Access the Services**

| Service          | URL                             |
|------------------|---------------------------------|
| **API**          | `http://localhost:8000/api/v1/` |
| **Swagger Docs** | `http://localhost:8000/docs`    |

---

## **7. Verify Setup**

After all services are running, you can test the API by accessing the **OpenAPI documentation**:

```plaintext
http://localhost:8000/docs
```


---
## **Run the Project with Postgres directly**

Install Python3:

```shell
www.python.org/
```

Install Git:

```shell
git-scm.com/
```

Install postgres
```shell
www.postgresql.org
```

Create database (postgres)

Enter to postgres

MacOS:
```shell
psql -U postgres
```

Linux MacOS:
```shell
sudo -u postgres psql
```

create database
```shell
CREATE DATABASE <your_db_name>;
```

if you need create user
```shell
CREATE USER <your_db_user> WITH PASSWORD <your_db_password>;

```

## **1. Clone the Repository**

Start by cloning the project repository from GitHub:

```bash
git clone https://github.com/skyfoxwork/notes_management_api_fastapi.git
```
```shell
cd notes_management_api_fastapi
```

```shell
git checkout develop
```
---

## **2. Create and Activate a Virtual Environment**

It is recommended to use a virtual environment to isolate project dependencies:

Create virtual environment:

```shell
python3 -m venv venv
```

Activate virtual environment (venv).

MacOS, Linux:

```shell
source venv/bin/activate
```
   Windows:

```shell
venv\Scripts\activate
```

if you need to deactivate virtual environment use:

```shell
deactivate
```

---

## **3. Install Dependencies with Poetry**
(Linux, MacOS)
```bash
make install
```
(Linux, MacOS, Windows)
```bash
pip install -r requirements.txt
```

---

## **4. Create a `.env` File**

Create a .env file in the root of the project and add the following environment variables:

Create .env file
```shell
cp .env.sample .env
```

```env
# PostgreSQL
POSTGRES_DB_NAME=<your_db_name>
POSTGRES_DB_PORT=5432
POSTGRES_USER=<your_db_user>
POSTGRES_PASSWORD=<your_db_password>
POSTGRES_HOST=<your_db_host>

# Gemini
GEMINI_API_KEY=<your_gemini_key>

# JWT
SECRET_KEY_ACCESS=838qKq7dGp34hWij3c8txA5ZD2qm9ybt
SECRET_KEY_REFRESH=cFzRk8kllHMW71wQKLXBqDzl24fkhisw
JWT_SIGNING_ALGORITHM=HS256

# Docker
PGDATA=/var/lib/postgresql/data
```

---

## **5. Run the Project with Postgres directly**
#### Make migrations
(Linux, MacOS)
```bash
make migrate
```
(Linux, MacOS, Windows)
```bash
alembic revision --autogenerate
```
#### Create tables in database
(Linux, MacOS)
```bash
make upgrade
```
(Linux, MacOS, Windows)
```bash
alembic upgrade head
```
#### Run project
(Linux, MacOS)
```bash
make run
```
(Linux, MacOS, Windows)
```bash
uvicorn src.main:app --reload
```
---

## **6. Access the Services**

| Service          | URL                             |
|------------------|---------------------------------|
| **API**          | `http://localhost:8000/api/v1/` |
| **Swagger Docs** | `http://localhost:8000/docs`    |

---

## **7. Verify Setup**

After all services are running, you can test the API by accessing the **OpenAPI documentation**:

```plaintext
http://localhost:8000/docs
```

# **Testing Project**

```shell
make test
```
```shell
python -m pytest
```
