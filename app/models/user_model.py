from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from app.core.mongo_object import PyObjectId


class User(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str]= None
    disabled: Optional[bool]= None
    
    
    model_config = {
        "json_encoders": {PyObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
    
    
   
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def __str__(self) -> str:
        return self.email
    
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email 
        return False
    
    def __hash__(self) -> int:
        return hash(self.email)
    
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email:str) -> "User":
        return await self.find_one(self.email==email)
    
    
    
    class Settings:
        name = "users"
    