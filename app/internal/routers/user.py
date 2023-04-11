from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.configs import Settings
from app.dependencies import get_session

from app.internal.models.user import UserModel

from app.internal.schemas.user import (
    UserListSchema,
    UserCreateSchema,
    UserBaseSchema, Token, UserUpdateSchema, UserRetrieveSchema
)
from app.internal.authentication.auth import get_password_hash, authenticate, create_access_token, get_current_user

router = APIRouter(prefix='/users', tags=['Users'])


# Todos usuários
@router.get(
    '/',
    summary='All Users',
    description='Return all users or an empty list',
    response_model=List[UserListSchema],
    status_code=status.HTTP_200_OK
)
async def get_users(
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)
):

    """
    - Usuários is_superuser == True podem visualizar a lista de usuários
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:
        try:
            query = select(UserModel).order_by('first_name')
            result = await session.execute(query)
            users: List[UserListSchema] = list(result.scalars().all())
            return users

        # Geralmente ocorre se o database estiver inacessível
        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Login
@router.post(
    '/sign-in',
    summary='Login',
    description='Authenticate user with email and password',
    response_model=Token
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):

    async with db as session:
        try:
            user = await authenticate(EmailStr(form_data.username), form_data.password, session)
            # token_valido = True
            if user:
                # if not token_valido:
                access_token = create_access_token(
                    {'sub': user.username},
                    timedelta(minutes=Settings.access_token_expire_minutes)
                )

                return {'access_token': access_token, 'token_type': 'bearer'}

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

        raise HTTPException(detail='Incorrect username or password', status_code=status.HTTP_401_UNAUTHORIZED)


# Create (novo usuário)
@router.post(
    '/sign-up',
    summary='Create User',
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
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            raise HTTPException(detail='Username or Email already exists', status_code=status.HTTP_406_NOT_ACCEPTABLE)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Retrieve (ver usuário)
@router.get(
    '/{user_id}',
    summary='Retrieve User',
    description='Return a user by ID',
    response_model=UserRetrieveSchema
)
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)
):

    """
    - Usuários is_superuser == True podem visualizar qualquer usuário
    - Usuários comuns podem visualizar apenas seu próprio usuário
    """

    if not current_user.is_superuser:

        if user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:

        try:

            query = select(UserModel).filter(UserModel.id == int(user_id))

            result = await session.execute(query)
            user: UserRetrieveSchema = result.scalars().one_or_none()
            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Update (atualizar dados de usuário)
@router.put(
    '/{user_id}',
    summary='Update User',
    description='Update and return a user by ID',
    response_model=UserRetrieveSchema,
)
async def put_user(
        user_id: int,
        user_put: UserUpdateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)
):

    """
    - Usuários is_superuser == True podem alterar qualquer usuário
    - Usuários comuns podem alterar apenas seu próprio usuário
    - Usuários comuns não podem alterar o status is_superuser
    """

    if not current_user.is_superuser:

        if user_id != current_user.id:
            raise HTTPException(
                # detail='Unable to change another user', status_code=status.HTTP_401_UNAUTHORIZED
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if user_put.is_superuser is not None:
            raise HTTPException(
                detail='Only admins can change superuser value', status_code=status.HTTP_401_UNAUTHORIZED
            )

    async with db as session:
        try:
            query = select(UserModel).filter(UserModel.id == int(user_id))
            result = await session.execute(query)
            user: UserUpdateSchema = result.scalars().one_or_none()

            if user:
                if user_put.first_name is not None:
                    user.first_name = user_put.first_name

                if user_put.last_name is not None:
                    user.last_name = user_put.last_name

                if user_put.username is not None:
                    user.username = EmailStr(user_put.username)

                if user_put.email is not None:
                    user.email = EmailStr(user_put.email)

                if user_put.password is not None:
                    user.password = get_password_hash(user_put.password)

                if user_put.is_superuser is not None:
                    user.is_superuser = user_put.is_superuser

                await session.commit()
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except IntegrityError:
            raise HTTPException(detail=f'User already exists', status_code=status.HTTP_406_NOT_ACCEPTABLE)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Delete (remover usuário)
@router.delete(
    '/{user_id}',
    summary='Delete User',
    description='Delete a user by ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)
):

    """
    - Usuários is_superuser == True podem deletar qualquer usuário
    - Usuários comuns podem deletar apenas seu próprio usuário
    """

    if not current_user.is_superuser:

        if user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:

        try:

            query = select(UserModel).filter(UserModel.id == int(user_id))
            result = await session.execute(query)
            user: UserBaseSchema = result.scalars().one_or_none()

            if user:
                await session.delete(user)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
