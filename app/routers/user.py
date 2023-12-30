from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    FastAPI,
    Request,
    Form,
    Query,
    UploadFile,
    File,
)
from fastapi.templating import Jinja2Templates
import smtplib
import shutil
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from fastapi.responses import RedirectResponse
import re
import app.db.schemas as schemas
from datetime import datetime, timezone
import time
from app.db.models import User

import pytz
from app.routers import post, user

import random
from datetime import datetime, timedelta
from google.cloud import storage
import os
from PIL import Image
from io import BytesIO
from app.config import Settings

setting = get_settings()
print(setting.max_otp_attempts)

# Create a 'now' variable representing the current date and time


# Generate and print a random number between 100 and 9999

UPLOAD_DIR = "app/templates/static/images_uploaded/"

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
templates = Jinja2Templates(
    directory="app/templates"
)
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "app/credentials.json"
Path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
storage_client = storage.Client(Path)
router = APIRouter()


@router.get("/",name='login')
async def login(request: Request):
    try:
        return templates.TemplateResponse("base.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/form")
async def login(request: Request):
    try:
        return templates.TemplateResponse("form.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/post/user")
async def get_user(
    request: Request,
    
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    gender:str=Form(...)
):
    
    '''file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)'''

   
   
    try:
        random_number = random.randint(1000, 9999)
        img = await file.read()
        img = Image.open(BytesIO(img))
        #img.thumbnail((200, 200))
        output = BytesIO()
        img.convert("RGB").save(output, format="JPEG")

        # Replace with your actual file name

        bucket = storage_client.bucket("christmas1234")

        # Create a Google Cloud Storage client

        # Define the destination blob name (file name in the bucket)
        #last_record = await User.all().order_by('-id').first()
        destination_blob_name = f"profiles/photo_thumb.jpg"

        # Upload the file to GCS
        blob = bucket.blob(destination_blob_name)
        blob.cache_control = 'no-store, no-cache, must-revalidate'
        blob.upload_from_file(BytesIO(output.getvalue()), content_type="image/jpeg")
        image_url=blob.public_url
        new_data = User(
            name=name,
            email=email,
            
            image_url=image_url,
            Gender=gender,
            num_attempts=1,
            otp=random_number
        )
        await new_data.save()
        server=smtplib.SMTP("smtp.gmail.com",587)
        print(server)
        server.starttls()
        server.login("raghu@launchxlabs.com","edar boft prtz mbsy")
        ms=f"Your otp is {random_number}"
        server.sendmail("raghu@launchxlabs.com",email,ms)
        server.quit()

        """ target_url = router.url_path_for(
                "create" ,
            ) 
        target_url+=f"/{phone}" """
        
        
        return templates.TemplateResponse("otp.html", {"request": request,"attempts":1,"name":name})
    except Exception as e:
        # Log the exception or handle it as needed
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/post/verify_otp/{name}")
async def verify_otp(request:Request,name:str,otp:int=Form(...)):
    last_record = await User.filter(name=name).order_by('-id').first()
    if otp==last_record.otp:
        target_url = router.url_path_for(
            "last" ,
        ) 
         
        response = RedirectResponse(url=target_url, status_code=303)
        return response
    else:
        n = last_record.num_attempts
        n += 1
        if(n>3):
            target_url = "/form"
         
            response = RedirectResponse(url=target_url)
            return response


        last_record.num_attempts = n
        await last_record.save()
    return templates.TemplateResponse("otp.html", {"request": request,"attempts":last_record.num_attempts})
    

@router.get("/last")
async def last(request:Request):
    return templates.TemplateResponse("last.html", {"request": request})
