from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.routers import user
from app.configs import API_V1_URI


app = FastAPI(
    title='Basic API',
    version='0.0.1',
    description='Basic API struct',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},  # Ocultar Schemas da DOCs
)


@app.get('/', tags=['Root'], include_in_schema=False)
async def root():
    return RedirectResponse('/docs')


app.include_router(user.router, prefix=API_V1_URI)
# app.include_router(admin.router, prefix=api_v1)
