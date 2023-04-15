from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List, Annotated, Optional

from app.configs import Settings
from app.dependencies import get_session
from app.internal.models.user import GroupModel

from app.internal.models.user import UserModel
from app.internal.schemas.group import GroupListSchema

from app.internal.schemas.user import (
    UserListSchema,
    UserCreateSchema,
    UserBaseSchema, Token, UserUpdateSchema, UserRetrieveSchema, UserGroupsRetrieveSchema
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
        current_user: Annotated[UserModel, Security(get_current_user, scopes=[])] = Optional,
):

    async with db as session:
        try:
            query = select(UserModel).order_by('first_name')
            result = await session.execute(query)
            users: List[UserListSchema] = list(result.scalars().unique().all())
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
async def login(
        db: AsyncSession = Depends(get_session),
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()] = Optional,
):

    # asfdasdf

    async with db as session:
        try:
            # query = select(GroupModel).order_by('name')
            query = select(GroupModel).order_by('name')
            result = await session.execute(query)
            # groups: List[GroupRetrieveSchema] = list(result.scalars().all())
            # print(f'groups: {groups}')

        # Geralmente ocorre se o database estiver inacessível
        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    # asfdasdf

    async with db as session:
        try:
            user = await authenticate(EmailStr(form_data.username), form_data.password, session)
            form_data.scopes = ['all', 'users']
            user_scopes: list[str] = []

            # token_valido = True
            if user:
                # if not token_valido:
                access_token = create_access_token(
                    {'sub': user.username, 'scopes': user_scopes},
                    timedelta(minutes=Settings.access_token_expire_minutes)
                )

                print(f'user: {user}\n')

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

    async with db as session:

        try:

            query = select(UserModel).filter(UserModel.id == int(user_id))

            result = await session.execute(query)
            user: UserRetrieveSchema = result.scalars().unique().one_or_none()

            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Retrieve Grupos do Usuário
@router.get(
    '/{user_id}/groups/',
    summary='Retrieve a Users Groups',
    description='Returns all groups for the user ID',
    response_model=List[GroupListSchema]
)
async def get_user_groups(
        user_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)
):

    async with db as session:

        try:

            user_query = select(UserModel).filter(UserModel.id == user_id)
            user_result = await session.execute(user_query)
            user = user_result.scalars().unique().one_or_none()

            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            query = select(GroupModel).filter(GroupModel.users.contains(user)).order_by('name')
            result = await session.execute(query)
            groups: List[GroupListSchema] = list(result.scalars().unique())

            if groups is not None:
                return groups
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

    async with db as session:
        try:
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

                if user_put.is_superuser:
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

    if not current_user.is_superuser:
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
