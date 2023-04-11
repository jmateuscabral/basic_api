from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.dependencies import get_session
from app.internal.models.user import UserModel
from app.internal.schemas.user import TokenData
from app.configs import Settings

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=F'{Settings.api_v1_uri}/users/sign-in')


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return password_context.verify(plain_password, hashed_password)


"""

Authentication

"""


async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)) -> UserModel:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token=token, key=Settings.jwt_secret_key, algorithms=[Settings.algorithm_jwt])

        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    async with db as session:

        # query = select(UserModel).filter(UserModel.id == int(token_data.username))
        query = select(UserModel).filter(UserModel.username == token_data.username)
        result = await session.execute(query)

        user: UserModel = result.scalars().one_or_none()

        if user is None:
            raise credentials_exception

        return user


async def authenticate(email: EmailStr, password: str, db: AsyncSession = Depends(get_session)) -> Optional[UserModel]:

    async with db as session:

        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, Settings.jwt_secret_key, algorithm=Settings.algorithm_jwt)
    return encoded_jwt
