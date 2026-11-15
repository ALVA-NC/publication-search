
from fastapi import FastAPI

from app.api.routes import publications


app = FastAPI(
    title="Publication Search API",
    description="API for searching OpenAlex publications",
    version="1.0.0"
)

app.include_router(publications.router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
