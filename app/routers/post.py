from fastapi import APIRouter, Depends, HTTPException, status,FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
import app.db.schemas as schemas
from datetime import datetime, timezone
import time
from app.db.models import User

# Get application settings from the configuration module
settings = get_settings()
templates=Jinja2Templates(directory='C:\\Users\\raghu\\Documents\\useful_social\\us\\app\\templates')

# Create an APIRouter instance
router = APIRouter()

__all__ = (
    'future_one_min'
)




# create a post
@router.post("/post/create")
async def create():
    return {"message": "Hello World"}



