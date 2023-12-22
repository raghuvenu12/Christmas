from datetime import datetime, timezone
from fastapi import FastAPI
from app.routers import ( post,user)
from app.db.session import init_db
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static",StaticFiles(directory="./app/templates/"),name="static")

app.include_router(user.router)
# static =StaticFiles(directory="./app/templates/images")


@app.on_event("startup")
async def on_startup():
    await init_db()


