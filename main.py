
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, Base, get_db
from security import hash_password, verify_password
from auth import create_access_token,get_current_user,create_refresh_token

app = FastAPI(
    title="JWT Authentication API"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "JWT Authentication API is running"
    }


@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post(
    "/auth/login",
    response_model=schemas.TokenWithRefresh
)
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    # Check if user exists
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    access_token = create_access_token(existing_user.id)
    refresh_token = create_refresh_token(existing_user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(
    current_user: models.User = Depends(get_current_user)
):
    return current_user