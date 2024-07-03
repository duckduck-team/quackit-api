from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api import models
from api.users import security
from api.schemas import user_schemas
from api.postgresql.db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


async def get_user(
    db: Session,
    username: str,
) -> user_schemas.UserInDB:
    return db.query(models.User).filter(models.User.username == username).first()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> user_schemas.UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("username")
        password: str = payload.get("password")
        if username is None or password is None:
            raise credentials_exception
        
        token_data = user_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
