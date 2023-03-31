from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.dependencies import get_session

from app.models.user import UserModel

from app.schemas.user import UserSchema

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', response_model=List[UserSchema], status_code=status.HTTP_200_OK)
async def get_users():
    return [
        {'nome': 'Rick', 'email': 'teste@asfd.com', 'nascimento': '2001'},
        {"nome": 'Morty', 'email': 'eeeee@ffff.com', 'nascimento': '2004'}
    ]


@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post_user(usuario: UserSchema, db: AsyncSession = Depends(get_session)):

    novo_usuario: UserModel = UserModel(
        nome=usuario.nome,
        email=usuario.email,
        nascimento=usuario.nascimento,
    )

    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        return novo_usuario


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}
