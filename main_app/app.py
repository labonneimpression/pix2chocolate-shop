import os
import re
import subprocess
import sys
import time
from urllib.request import urlretrieve

from django.db import models
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.utils import timezone
from nanodjango import Django

app = Django()

settings.STATIC_URL = "/static/"
settings.STATICFILES_DIRS = []
settings.STATIC_ROOT = os.path.join(settings.BASE_DIR, "staticfiles")
settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, "uploads")


@app.admin
class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField()
    quantity = models.IntegerField()
    with_biscuit = models.BooleanField(default=True)
    # Uploads to settings.MEDIA_ROOT
    preview = models.FileField(
        upload_to="preview_%Y-%m-%d%/%H-%M-%S/", blank=True, null=True
    )
    CAD_part = models.FileField(
        upload_to="CAD_part_%Y-%m-%d%/%H-%M-%S/", blank=True, null=True
    )

    def download_preview_to_local(self, url):
        try:
            name, _ = urlretrieve(url)
            self.preview.save(
                "{timestamp}.png".format(
                    timestamp=timezone.now().strftime("%Y-%m-%d%/%H-%M-%S")
                ),
                File(open(tempname, "rb")),
            )
        finally:
            urlcleanup()


@app.route("/")
def order_form(request):
    return f"<p>This is the order form :)</p>"
