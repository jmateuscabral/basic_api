from fastapi import Depends, FastAPI

from .dependencies import get_token_header
from .internal import admin
from .routers import user


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI(
    title='Basic API'
)

app.include_router(user.router)
app.include_router(admin.router)

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/", tags=['Root'])
async def root():
    return {"message": "Hello Bigger Applications!"}
