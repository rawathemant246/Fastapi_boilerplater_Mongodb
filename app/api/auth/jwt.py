from fastapi import APIRouter, Depends, HTTPException, status, Body 
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.services.user_service import UserService
from app.core.security import create_access_token,create_refresh_token
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserOut
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.core.config import settings
from app.schemas.auth_schema import TokenPayload
from pydantic import ValidationError
from jose import jwt 
from jwt.exceptions import PyJWTError



auth_router = APIRouter()


@auth_router.post("/login", summary="create access token and refresh token for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm= Depends()) -> Any:
    user = await UserService.authenticate(email= form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Incorrect email or password"
        )
    
    
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }
    
    

@auth_router.post('/test-token', summary="Test if the access token is valid", response_model=UserOut)
async def test_token(refresh_token:str = Body(...)):
    try: 
        payload = jwt.decode(
            refresh_token, 
            settings.JWT_REFRESH_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        token_data = TokenPayload(**payload)
    
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate refresh token",
            headers= {"WWW-Authenticate":"Bearer"}
        )
        
    
    user = await UserService.get_user_by_id(token_data.sub)
    
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    
    return {
        
        "access_token" : create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }
    
    
    
    





