# Publication Search

A web application for searching and exploring academic publications retrieved from the [OpenAlex API](https://openalex.org/).

## Architecture

The application consists of:

- **Vue.js:** Frontend and user interface.
- **FastAPI:** Backend REST API.
- **Elasticsearch:** Search engine and runtime data storage.
- **MongoDB:** Storage of original publication records.

### Data flow

1. A Python script retrieves publications from OpenAlex and stores them in MongoDB.
2. A second Python script prepares and indexes the publications in Elasticsearch.
3. Vue.js sends search requests to FastAPI.
4. FastAPI queries Elasticsearch and returns results to the frontend.

MongoDB is only used for storing the initial data for indexing. All application searches and publication details are retrieved from Elasticsearch.

## Prerequisites

- Python
- Node.js and npm
- Docker Desktop with Docker Compose
- OpenAlex API key

## Installation and setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd publication-search
```

### 2. Configure environment variables

Create `backend/.env`:

```env
OPENALEX_API_KEY=your_api_key
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=publication_search
MONGODB_COLLECTION=publications
ELASTICSEARCH_URL=http://localhost:9200
```

### 3. Start databases

From the project root:

```bash
docker compose up -d
```

### 4. Set up the backend

This is done with a virtual environment to avoid python package conflicts

```bash
cd backend
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 5. Retrieve and index publications

```bash
python -m scripts.harvest
python -m scripts.index_publications
```

### 6. Start the backend

```bash
uvicorn app.main:app --reload
```

API documentation: http://localhost:8000/docs

### 7. Start the frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Application: http://localhost:5173

## Deployment

The application can be deployed on another machine by following the installation steps above.

Manual steps include configuring the OpenAlex API key, installing dependencies, running the harvesting and indexing scripts, and starting the frontend and backend.

MongoDB and Elasticsearch are managed through Docker Compose. The frontend and backend currently run separately and are not yet containerized.

## Assumptions and limitations

- Data is not updated automatically; harvesting and indexing must be run manually. Change streams in MongoDB combined with a worker could be added to synchronize the index as the database is updated.
- Elasticsearch security is disabled in the local development configuration for simplicity. Authentication, authorization and HTTPS should be configured before exposing the application publicly