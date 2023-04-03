from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.configs import ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import get_session

from app.models.user import UserModel

from app.schemas.user import (
    UserListSchema,
    UserCreateSchema,
    UserBaseSchema, Token
)
from app.untils import get_password_hash, authenticate, create_access_token

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get(
    '/',
    summary='All Users',
    description='Return all users or an empty list',
    response_model=List[UserListSchema],
    status_code=status.HTTP_200_OK
)
async def get_users(db: AsyncSession = Depends(get_session)):

    async with db:
        # result = await db.execute(query)
        try:
            query = select(UserModel)
            result = await db.execute(query)
            users: List[UserListSchema] = list(result.scalars().unique().all())
            return users
        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@router.post(
    '/',
    summary='New User',
    description='Add and return new user',
    response_model=UserBaseSchema,
    status_code=status.HTTP_201_CREATED
)
async def post_user(usuario: UserCreateSchema, db: AsyncSession = Depends(get_session)):

    novo_usuario: UserModel = UserModel(
        first_name=usuario.first_name,
        last_name=usuario.last_name,
        username=usuario.username,
        email=usuario.email,
        password=get_password_hash(usuario.password),
    )

    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        return novo_usuario


@router.post(
    '/login',
    summary='Login',
    description='Authenticate User With Email and Password',
    response_model=Token
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):

    user = await authenticate(EmailStr(form_data.username), form_data.password, db)

    if user:
        access_token = create_access_token({'sub': user.username}, timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
        return {'access_token': access_token, 'token_type': 'bearer'}

    raise HTTPException(detail='Incorrect username or password', status_code=status.HTTP_401_UNAUTHORIZED)
