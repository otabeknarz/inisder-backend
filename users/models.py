from django.db import models
from django.contrib.auth.models import AbstractUser

import random
import string

from insider.base_model import BaseModel


def get_random_id(k=12) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=get_random_id, unique=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    email = models.EmailField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name="districts")

    def __str__(self):
        return self.name
