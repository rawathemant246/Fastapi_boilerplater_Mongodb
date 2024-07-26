from typing import Optional
from uuid import UUID
from bson import ObjectId
import pymongo.errors
from app.schemas.user_schema import UserAuth
from app.core.security import get_password, verify_password
from app.core.mongo_object import PyObjectId
from app.models.user_model import User
import pymongo

from app.schemas.user_schema import UserUpdate



class UserService:
    
    @staticmethod
    async def create_user(user:UserAuth):
        user_in = User(
            username= user.username,
            email=user.email,
            hashed_password= get_password(user.password)
        )
        
        await user_in.insert()
        
        return user_in
    
    
    @staticmethod
    async def authenticate(email:str, password:str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        
        return user
    
    
    @staticmethod
    async def get_user_by_email(email:str) -> Optional[User]:
        user = await User.find_one({"email": email})
        return user
    
    @staticmethod
    async def get_user_by_id(id:PyObjectId) -> Optional[User]:
        user = await User.find_one({"_id": id})
        return user
    
    @staticmethod
    async def update_user(id: PyObjectId, data: UserUpdate) -> User:
        user = await User.find_one(User.id == id)
        
        if not user:
            raise pymongo.errors.OperationFailure("User not found")
        
        await user.update({"$set": data.model_dump(exclude_unset=True)})
        
        return user