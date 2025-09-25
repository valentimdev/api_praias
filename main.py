import os
from fastapi import FastAPI
from core.config import settings
from api.v1 import routes_praia
from api.v1 import routes_quiosque
from db.session import Base, engine
from seeds.praia import seed as praia_seed

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(routes_praia.router, prefix="/api/v1/praia", tags=["praias"])
app.include_router(routes_quiosque.router, prefix="/api/v1/quiosque", tags=["quiosques"])

seed_flag = os.getenv("SEED", "False").lower() in ("1", "true", "yes")
print(seed_flag)
if seed_flag:
    praia_seed()
