from fastapi import APIRouter, Depends, HTTPException, Security

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from typing import List, Annotated, Optional

from app.dependencies import get_session
from app.internal.authentication.auth import get_current_user

from app.internal.models.user import UserModel
from app.internal.models.group import GroupModel

from app.internal.schemas.user import UserListSchema
from app.internal.schemas.group import (
    GroupCreateSchema,
    GroupRetrieveSchema,
    GroupUpdateSchema,
    GroupListSchema,
)


router = APIRouter(prefix='/groups', tags=['Groups'])


@router.get(
    path='/',
    summary='All Groups',
    description='Return all groups or an empty list',
    response_model=List[GroupListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_groups(
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["group_list"]
        )] = Optional,
):

    async with db as session:

        try:
            query = select(GroupModel).order_by('name')
            result = await session.execute(query)
            groups: List[GroupModel] = list(result.scalars().unique())
            return groups

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.post(
    path='/',
    summary='Create Group',
    description='Add and return new group',
    response_model=GroupRetrieveSchema,
    status_code=status.HTTP_201_CREATED,
)
async def post_group(
        group_create: GroupCreateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["group_create"]
        )] = Optional,
):

    group: GroupModel = GroupModel(name=group_create.name)

    async with db as session:

        try:
            session.add(group)
            await session.commit()
            return group

        except IntegrityError:
            raise HTTPException(
                detail='Group already exists',
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get(
    path='/{group_id}',
    summary='Retrieve Group',
    description='Return a group by ID',
    response_model=GroupRetrieveSchema,
    status_code=status.HTTP_200_OK,
)
async def get_group(
        group_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["group_retrieve"]
        )] = Optional,
):

    async with db as session:

        try:
            query = select(GroupModel).filter(GroupModel.id == group_id)
            result = await session.execute(query)
            group: GroupModel = result.scalars().unique().one_or_none()

            if group:
                return group
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.get(
    path='/{group_id}/users',
    summary='Retrieve Group',
    description='Return a group by ID',
    response_model=List[UserListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users_by_group(
        group_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["group_users_by_group"]
        )] = Optional,
):

    async with db as session:

        try:
            group_query = select(GroupModel).filter(GroupModel.id == group_id)
            group_result = await session.execute(group_query)
            group: GroupModel = group_result.scalars().unique().one_or_none()

            if not group:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            query = select(UserModel).filter(UserModel.groups.contains(group))
            result = await session.execute(query)
            users: List[UserModel] = list(result.scalars().unique())

            if users is not None:
                return users
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.put(
    path='/{group_id}',
    summary='Update Group',
    description='Update and return a group by ID',
    response_model=GroupRetrieveSchema,
    status_code=status.HTTP_200_OK,
)
async def put_group(
        group_id: int,
        group_update: GroupUpdateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["group_update"]
        )] = Optional,
):

    async with db as session:

        try:
            query = select(GroupModel).filter(GroupModel.id == group_id)
            result = await session.execute(query)
            group: GroupModel = result.scalars().unique().one_or_none()

            if group:

                if group_update.name:
                    group.name = group_update.name

                await session.commit()
                return group

            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except IntegrityError:
            raise HTTPException(
                detail='Group already exists',
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


@router.delete(
    path='/{group_id}',
    summary='Delete Group',
    description='Delete a group by ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
        group_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: Annotated[UserModel, Security(
            get_current_user,
            scopes=["group_delete"]
        )] = Optional
):

    async with db as session:

        try:
            query = select(GroupModel).filter(GroupModel.id == group_id)
            result = await session.execute(query)
            group: GroupModel = result.scalars().unique().one_or_none()

            if group:
                await session.delete(group)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError as e:
            raise HTTPException(
                detail=f'{e}',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
