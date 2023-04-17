from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from datetime import timedelta

from typing import List, Annotated, Optional
from pydantic import EmailStr

from app.dependencies import get_session
from app.configs import Settings

from app.internal.authentication.auth import (
    authenticate,
    create_access_token,
    get_password_hash,
    get_current_user,
)

from app.internal.models.group import GroupModel
from app.internal.models.user import UserModel

from app.internal.schemas.group import GroupListSchema
from app.internal.schemas.user import (
    UserCreateSchema,
    UserRetrieveSchema,
    UserUpdateSchema,
    UserListSchema,
    Token,
)

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    path='/',
    summary='All Users',
    description='Return all users or an empty list',
    response_model=List[UserListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users(
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["user_list"]
        )] = Optional,
):

    async with db as session:

        try:
            query = select(UserModel).order_by('first_name')
            result = await session.execute(query)
            users: List[UserModel] = list(result.scalars().unique())
            return users

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.post(
    path='/sign-in',
    summary='Login',
    description='Authenticate user with email and password',
    response_model=Token
)
async def login(
        db: AsyncSession = Depends(get_session),
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()] = Optional,
):

    async with db as session:

        try:
            user = await authenticate(EmailStr(form_data.username), form_data.password, session)

            query_groups = select(GroupModel).filter(GroupModel.users.contains(user)).order_by('name')
            result_groups = await session.execute(query_groups)
            groups: List[GroupModel] = list(result_groups.scalars().unique())
            print(f'groups: {groups}')

            user_scopes: list[str] = [

                'user_list',
                'user_groups_by_user',
                'user_retrieve',
                'user_update',
                'user_delete',

                'group_list',
                'group_users_by_group',
                'group_create',
                'group_retrieve',
                'group_update',
                'group_delete',

            ]

            if user:

                access_token = create_access_token(
                    {'sub': user.username, 'scopes': user_scopes},
                    timedelta(minutes=Settings.access_token_expire_minutes)
                )

                return {'access_token': access_token, 'token_type': 'bearer'}

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

        raise HTTPException(detail='Incorrect username or password', status_code=status.HTTP_401_UNAUTHORIZED)


@router.post(
    path='/sign-up',
    summary='Create User',
    description='Add and return new user',
    response_model=UserRetrieveSchema,
    status_code=status.HTTP_201_CREATED,
)
async def post_user(
        user_create: UserCreateSchema,
        db: AsyncSession = Depends(get_session)
):

    user: UserModel = UserModel(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        username=user_create.username,
        email=user_create.email,
        password=get_password_hash(user_create.password),
    )

    async with db as session:

        try:
            session.add(user)
            await session.commit()
            return user

        except IntegrityError:
            raise HTTPException(
                detail='Username or Email already exists',
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get(
    path='/{user_id}',
    summary='Retrieve User',
    description='Return a user by ID',
    response_model=UserRetrieveSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["user_retrieve"]
        )] = Optional,
):

    async with db as session:

        try:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get(
    path='/{user_id}/groups',
    summary='Retrieve User Groups',
    description='Returns all groups for the user ID',
    response_model=List[GroupListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_groups_by_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["user_groups_by_user"]
        )] = Optional,
):

    async with db as session:

        try:
            user_query = select(UserModel).filter(UserModel.id == user_id)
            user_result = await session.execute(user_query)
            user: UserModel = user_result.scalars().unique().one_or_none()

            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            query = select(GroupModel).filter(GroupModel.users.contains(user)).order_by('name')
            result = await session.execute(query)
            groups: List[GroupModel] = list(result.scalars().unique())

            if groups is not None:
                return groups
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.put(
    path='/{user_id}',
    summary='Update User',
    description='Update and return a user by ID',
    response_model=UserRetrieveSchema,
    status_code=status.HTTP_200_OK,
)
async def put_user(
        user_id: int,
        user_put: UserUpdateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["user_update"]
        )] = Optional,
):

    async with db as session:
        try:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

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
            raise HTTPException(
                detail=f'User already exists',
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.delete(
    path='/{user_id}',
    summary='Delete User',
    description='Delete a user by ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["user_delete"]
        )] = Optional,
):

    async with db as session:

        try:
            query = select(UserModel).filter(UserModel.id == user_id)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if user:
                await session.delete(user)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
