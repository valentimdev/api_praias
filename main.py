from fastapi import FastAPI
from core.config import settings
from api.v1 import routes_praia
from db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(routes_praia.router, prefix="/api/v1/praia", tags=["praias"])
