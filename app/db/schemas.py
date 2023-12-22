from pydantic import BaseModel, ConfigDict
import datetime

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    phone: str
    usr_type: str
    created_at: datetime.datetime

class Media(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type: str
    url: str
    thumbnail_url: str

class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: str
    user: User
    text: str
    latitude: float
    longitude: float
    #media: list(Media) = []
    created_at: datetime.datetime


