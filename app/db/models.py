from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db import models

# This is an abstract model. No table will be created for this model.
class User(Model):
    name = fields.CharField(max_length=256, null=False, )
    email = fields.CharField(max_length=256, null=False, )
    otp = fields.IntField(max_length=6, null=False, )
    num_attempts = fields.IntField(max_length=3, null=False, )
    Gender= fields.CharField(max_length=256, null=False, )
    image_url=fields.CharField(max_length=256, null=False, )
    
    created_at = fields.DatetimeField(auto_now=True, )
    class Meta:
        table = "user"

