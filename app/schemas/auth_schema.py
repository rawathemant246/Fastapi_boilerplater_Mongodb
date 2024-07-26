from uuid import UUID
from typing import Optional, Annotated
from pydantic import BaseModel, BeforeValidator
from bson import ObjectId
from app.core.mongo_object import PyObjectId

class TokenSchema(BaseModel):
    access_token : str
    refresh_token : str
    


class TokenPayload(BaseModel):
    sub : Annotated[PyObjectId, BeforeValidator(PyObjectId)]  = None
    exp : int = None

