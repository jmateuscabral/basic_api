from fastapi import FastAPI

from app.routers import user
from app.configs import API_V1_URI


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(
    title='Basic API',
    version='0.0.1',
    description='Basic API struct',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},  # Ocultar Schemas da DOCs

)

app.include_router(user.router, prefix=API_V1_URI)
# app.include_router(admin.router, prefix=api_v1)

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


# @app.get("/", tags=['Root'])
# async def root():
#     return {"message": "Hello Bigger Applications!"}
