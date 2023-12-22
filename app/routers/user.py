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

UPLOAD_DIR = "/Users/raghunandanvenugopal/Downloads/us-main/app/templates/static/images_uploaded/"

# Create the directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
templates = Jinja2Templates(
    directory="/Users/raghunandanvenugopal/Downloads/us-main/app/templates"
)
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/Users/raghunandanvenugopal/Desktop/demo/molten-complex-408603-13e3b41bd520.json"
Path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
storage_client = storage.Client(Path)
router = APIRouter()


@router.get("/",name='login')
async def login(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.post("/form")
async def login(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@router.post("/post/user")
async def get_user(
    request: Request,
    
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    gender:str=Form(...)
):
    print(gender)
    '''file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)'''

   
   
    random_number = random.randint(1000, 9999)
    img = await file.read()
    img = Image.open(BytesIO(img))
    img.thumbnail((200, 200))
    output = BytesIO()
    img.convert("RGB").save(output, format="JPEG")

    # Replace with your actual file name

    bucket = storage_client.bucket("christmas1234")

    # Create a Google Cloud Storage client

    # Define the destination blob name (file name in the bucket)
    last_record = await User.all().order_by('-id').first()
    destination_blob_name = f"profiles/{last_record.id+1}_thumb.jpg"

    # Upload the file to GCS
    blob = bucket.blob(destination_blob_name)
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
    ms=f"your otp is {random_number}"
    server.sendmail("raghu@launchxlabs.com",email,ms)
    server.quit()

    """ target_url = router.url_path_for(
            "create" ,
        ) 
    target_url+=f"/{phone}" """
    
    
    return templates.TemplateResponse("otp.html", {"request": request,"attempts":1})


@router.post("/post/verify_otp")
async def verify_otp(request:Request,otp:int=Form(...)):
    last_record = await User.all().order_by('-id').first()
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
    