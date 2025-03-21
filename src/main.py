from fastapi import FastAPI

from src.routes.notes import router as notes_router
from src.routes.ai import router as ai_router
from src.routes.analytics import router as analytics_router


app = FastAPI(title="Notes Management API", description="Project description")

api_version_prefix = "/api/v1"

app.include_router(
    notes_router, prefix=f"{api_version_prefix}/notes", tags=["notes"]
)
app.include_router(
    ai_router, prefix=f"{api_version_prefix}/summarize", tags=["summarize"]
)
app.include_router(
    analytics_router, prefix=f"{api_version_prefix}/analytics", tags=["analytics"]
)
