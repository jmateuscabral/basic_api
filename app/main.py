from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.internal.routers import user
from app.configs import Settings


app = FastAPI(
    title=Settings.app_name,
    version=Settings.app_version,
    description=Settings.app_description,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},  # Ocultar Schemas da DOCs
)


@app.get('/', tags=['Root'], include_in_schema=False)
async def root():
    return RedirectResponse('/docs')


app.include_router(user.router, prefix=Settings.api_v1_uri)
