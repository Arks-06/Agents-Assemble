# Agents-Assemble
## Description
Agents-Assemble is a full-stack, distributed AI engineering platform designed to orchestrate asynchronous AI research agents. It leverages **FastAPI** for a secure API layer, **PostgreSQL** for persistent state management, **Celery & Redis** for distributed background task queues, and **WebSockets** for real-time result broadcasting.

## Core Features
* **Multi-Tenant Architecture:** JWT-based authentication with role-based access control (RBAC) ensuring data isolation across user workspaces.
* **Asynchronous AI Agents:** Heavy LLM workloads are offloaded to Celery background workers, keeping the main API blazingly fast.
* **Real-Time WebSockets:** Redis Pub/Sub integration broadcasts live task completion updates directly to authenticated client sockets.
* **Smart Caching:** Database queries and AI responses are cached in Redis to minimize redundant API calls and save LLM credits.
* **Modern Tooling:** Built with Python 3.10+, SQLAlchemy 2.0, Alembic migrations, and the `uv` package manager.
* **Reactive Frontend:** A custom Streamlit-based workspace with integrated authentication, dynamic polling, and professional UI/UX animations.

## Project Structure
```markdown
Agents-Assemble/
├── backend/
│   ├── app/
│   │   ├── agents/       # Agno AI agent logic and prompts
│   │   ├── api/          # FastAPI routers and security dependencies
│   │   ├── core/         # Global config, Redis, and WebSocket managers
│   │   ├── db/           # SQLAlchemy session and Base setup
│   │   ├── models/       # Database schemas (Users, ResearchTasks)
│   │   ├── schemas/      # Pydantic validation models
│   │   ├── services/     # Redis caching and Pub/Sub broadcasters
│   │   └── workers/      # Celery app configuration and background tasks
│   ├── alembic/          # Database migration history
│   ├── main.py           # FastAPI application entry point
│   ├── pyproject.toml    # Project dependencies
│   └── uv.lock
├── docker-compose.yml    # Infrastructure container orchestration
├── frontend/
    ├── .gitignore
    ├── .python-version
    ├── README.md
    ├── pyproject.toml
    ├── src/
        ├── api_client.py
        ├── components/
            ├── auth.py
            ├── chat_ui.py
            ├── sidebar.py
        ├── config.py
        ├── main.py
        ├── utils/
            ├── helpers.py
            ├── styles.py
    ├── uv.lock
```

## Configuration
The application uses environment variables for configuration. A `.env` file should be created in the root of the project with the following variables:
* `DATABASE_URL`
* `REDIS_URL`
* `GROQ_API_KEY`
* `TAVILY_API_KEY`
* `CELERY_BROKER_URL`
* `CELERY_RESULT_BACKEND`

## Prerequisites
* Python 3.10 or higher
* `uv` package manager
* Docker (for database setup)

## Database Setup
To set up the database, navigate to the root of the project and run the following command:
```bash
docker compose up -d
```
This will start the PostgreSQL database in detached mode.

## Installation
To install the dependencies, navigate to the `backend` directory and run the following command:
```bash
cd backend
uv sync
```
This will install all dependencies specified in the `pyproject.toml` file.

## Run Database Migrations:
```bash
uv run alembic upgrade head
```

## Usage
To start the application, navigate to the `backend` directory and run the following command:
### Terminal 1: Start the FastAPI Server
```bash
uv run uvicorn app.main:app --reload --port 8000
```
This will start the FastAPI development server on port 8080.
### Terminal 2: Start the Celery Worker
```bash
uv run celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```
### Terminal 3: Start the Frontend
Navigate to the `frontend` directory:
```bash
cd frontend
uv sync
uv run streamlit run src/main.py
```

## License
The license for this project is not specified. Please contact the author for more information.