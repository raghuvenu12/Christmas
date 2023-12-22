from tortoise import Tortoise
from app.db import orm_settings
from tortoise.contrib.pydantic import pydantic_model_creator


async def init_db():
    print(orm_settings.TORTOISE_ORM)
    await Tortoise.init(config=orm_settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()


