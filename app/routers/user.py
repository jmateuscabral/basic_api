from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.dependencies import get_session

from app.models.user import UserModel

from app.schemas.user import (
    UserListSchema,
    UserCreateSchema,
    UserBaseSchema
)
from app.untils import generate_hashed_password

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
        password=generate_hashed_password(usuario.password),
        # date_birth=usuario.date_birth,
        # is_superuser=usuario.is_superuser,
        # is_active=usuario.is_active,
    )

    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        return novo_usuario
