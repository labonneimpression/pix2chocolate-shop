import os
import re
import subprocess
import sys
import time

from django.db import models
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from nanodjango import Django

app = Django()

settings.STATIC_URL = "/static/"
settings.STATICFILES_DIRS = [
]
settings.STATIC_ROOT = os.path.join(settings.BASE_DIR, "staticfiles")
settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, "uploads")

@app.admin
class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

@app.route("/")
def order_form(request):
    return f"<p>This is the order form :)</p>"

