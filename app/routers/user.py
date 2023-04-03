from fastapi import APIRouter, Depends
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.dependencies import get_session

from app.models.user import UserModel

from app.schemas.user import UserListSchema

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', response_model=List[UserListSchema], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session)):

    async with db:
        query = select(UserModel)
        # result = await db.execute(query)
        result = await db.execute(query)
        users: List[UserListSchema] = result.scalars().unique().all()
        return users


@router.post('/', response_model=UserListSchema, status_code=status.HTTP_201_CREATED)
async def post_user(usuario: UserListSchema, db: AsyncSession = Depends(get_session)):

    novo_usuario: UserModel = UserModel(
        username=usuario.username,
        first_name=usuario.first_name,
        last_name=usuario.last_name,
        email=usuario.email,
        password=usuario.password,
        date_birth=usuario.date_birth,
        is_superuser=usuario.is_superuser,
        is_active=usuario.is_active,
    )

    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        return novo_usuario
