from fastapi import FastAPI

from src.routes.notes import router as notes_router


app = FastAPI(title="Notes Management API", description="Project description")


api_version_prefix = "/api/v1"

app.include_router(
    notes_router, prefix=f"{api_version_prefix}/notes", tags=["notes"]
)
