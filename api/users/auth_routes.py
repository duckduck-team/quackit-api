from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import models
from api.users import auth
from api.users import security
from api.schemas import user_schemas

from api.postgresql.db import get_db


SESSION = 0


router = APIRouter(
    prefix="/user",
    tags=["User Authentication"],
    dependencies=[Depends(get_db)]
)


@router.post(
    "/register",
    response_model=user_schemas.UserInDB,
    status_code=200,
    summary="""The endpoint `/register` registers a new user by storing their username, password in PostgreSQL database.""",
)
async def register(
    user: user_schemas.User,
    db: Session = router.dependencies[SESSION],
):
    db_user: user_schemas.UserInDB = await auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = models.User(username=user.username, password=user.password, email=user.email)

    db.add(db_user)
    db.commit()

    return db_user


@router.post(
    "/token",
    response_model=user_schemas.Token,
    status_code=200,
    summary="""The endpoint `/token` returns an access token for the authenticated user.""",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = router.dependencies[SESSION],
):
    user: user_schemas.UserInDB = await auth.get_user(db, username=form_data.username)
    if not user or form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"username": user.username, "password": user.password}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=user_schemas.UserInDB,
    status_code=200,
    summary="""The endpoint `/me` returns the current user.""",
)
async def current_user(
    current_user: user_schemas.UserInDB = Depends(auth.get_current_user),
):
    return current_user
