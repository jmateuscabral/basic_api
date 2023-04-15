from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from app.dependencies import get_session
from app.internal.models.user import GroupModel
# from app.internal.models.group import GroupModel

from app.internal.models.user import UserModel
from app.internal.schemas.group import GroupBaseSchema, GroupCreateSchema, GroupListSchema, GroupRetrieveSchema, \
    GroupUpdateSchema, GroupUsersRetrieveSchema

from app.internal.authentication.auth import get_current_user
from app.internal.schemas.user import UserListSchema

router = APIRouter(prefix='/groups', tags=['Groups'])


# Todos grupos
@router.get(
    '/',
    summary='All Groups',
    description='Return all groups or an empty list',
    response_model=List[GroupListSchema],
    status_code=status.HTTP_200_OK
)
async def get_groups(
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user),
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:
        try:
            query = select(GroupModel).order_by('name')
            result = await session.execute(query)
            # groups: List[GroupListSchema] = list(result.scalars().all())
            groups: List[GroupListSchema] = list(result.scalars().unique())
            return groups

        # Geralmente ocorre se o database estiver inacessível
        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Create (novo grupo)
@router.post(
    '/',
    summary='Create Group',
    description='Add and return new group',
    response_model=GroupRetrieveSchema,
    status_code=status.HTTP_201_CREATED
)
async def post_group(
        grupo: GroupCreateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user),
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    novo_grupo: GroupModel = GroupModel(
        name=grupo.name,
    )

    async with db as session:
        try:
            session.add(novo_grupo)
            await session.commit()
            return novo_grupo
        except IntegrityError:
            raise HTTPException(detail='Group already exists', status_code=status.HTTP_406_NOT_ACCEPTABLE)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Retrieve (ver usuário)
@router.get(
    '/{group_id}',
    summary='Retrieve Group',
    description='Return a group by ID',
    response_model=GroupRetrieveSchema
)
async def get_group(
        group_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user),
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:

        try:

            query = select(GroupModel).filter(GroupModel.id == int(group_id))

            result = await session.execute(query)
            group: GroupRetrieveSchema = result.scalars().unique().one_or_none()
            if group:
                return group
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Retrieve usuários de um grupo
@router.get(
    '/{group_id}/users/',
    summary='Retrieve Group',
    description='Return a group by ID',
    response_model=List[UserListSchema]
)
async def get_group_users(
        group_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user),
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:

        try:

            group_query = select(GroupModel).filter(GroupModel.id == group_id)
            group_result = await session.execute(group_query)
            group = group_result.scalars().unique().one_or_none()

            if group is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            query = select(UserModel).filter(UserModel.groups.contains(group))
            result = await session.execute(query)
            users: List[UserListSchema] = list(result.scalars().unique())

            if users is not None:
                return users
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Update (atualizar dados de usuário)
@router.put(
    '/{group_id}',
    summary='Update Group',
    description='Update and return a group by ID',
    response_model=GroupRetrieveSchema,
)
async def put_group(
        group_id: int,
        group_put: GroupUpdateSchema,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user),
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:
        try:
            query = select(GroupModel).filter(GroupModel.id == int(group_id))
            result = await session.execute(query)
            group: GroupUpdateSchema = result.scalars().unique().one_or_none()

            if group:
                if group_put.name:
                    group.name = group_put.name

                await session.commit()
                return group
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except IntegrityError:
            raise HTTPException(detail=f'User already exists', status_code=status.HTTP_406_NOT_ACCEPTABLE)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# Delete (remover usuário)
@router.delete(
    '/{group_id}',
    summary='Delete Group',
    description='Delete a group by ID',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
        group_id: int,
        db: AsyncSession = Depends(get_session),
        current_user: UserModel = Depends(get_current_user)
):

    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db as session:

        try:

            query = select(GroupModel).filter(GroupModel.id == int(group_id))
            result = await session.execute(query)
            group: GroupBaseSchema = result.scalars().unique().one_or_none()

            if group:
                await session.delete(group)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        except OSError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
