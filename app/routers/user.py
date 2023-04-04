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
    UserBaseSchema, Token, UserUpdateSchema
)
from app.untils import get_password_hash, authenticate, create_access_token

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# Todos usuários
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


# Login
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


# Create (novo usuário)
@router.post(
    '/sign-up',
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


# Retrieve (ver usuário)
@router.get(
    '/{user_id}',
    summary='User',
    description='Return a User by ID',
    response_model=UserBaseSchema
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(user_id))
        result = await session.execute(query)
        user: UserBaseSchema = result.scalars().one_or_none()
        if user:
            return user
        else:
            raise HTTPException(detail='User not found', status_code=status.HTTP_400_BAD_REQUEST)


# Update (atualizar dados de usuário)
@router.put(
    '/{user_id}',
    summary='Put User',
    description='Put and return a user by ID',
    response_model=UserBaseSchema,
)
async def put_user(user_id: int, user_put: UserUpdateSchema, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(user_id))
        result = await session.execute(query)
        user: UserUpdateSchema = result.scalars().one_or_none()

        if user:
            if user_put.first_name:
                user.first_name = user_put.first_name

            if user_put.last_name:
                user.last_name = user_put.last_name

            if user_put.username:
                user.username = EmailStr(user_put.username)

            if user_put.email:
                user.email = EmailStr(user_put.email)

            if user_put.password:
                user.password = get_password_hash(user_put.password)

            await session.commit()
            return user
        else:
            raise HTTPException(detail='User not found', status_code=status.HTTP_400_BAD_REQUEST)


# Delete (remover usuário)
@router.delete(
    '/{user_id}',
    summary='Delete User',
    description='Delete a User by ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(user_id))
        result = await session.execute(query)
        user: UserBaseSchema = result.scalars().one_or_none()
        if user:
            await session.delete(user)
            await session.commit()

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
