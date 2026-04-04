import os
import re
import subprocess
import sys
import time

from django.db import models
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


# TODO Order API


# TODO Part API
@app.api.post("/cad_part")
def get_cad_part(request):
    if not hasattr(request, "FILES") or not request.FILES:
        return {"status": False, "details": {"message": "Missing files body"}}, 400
    if "file" not in request.FILES:
        return {"status": False, "details": {"message": "No file provided."}}, 400

    uploaded_file = request.FILES["file"]
    if uploaded_file.size > 10 * 1024 * 1024:  # 10 MB limit
        return {"status": False, "details": {"message": "File too large"}}, 400

    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_url = fs.url(filename)

    start = time.perf_counter()
    command = [
        sys.executable,
        "generate_cad_part.py",
        os.path.join(os.getcwd(), settings.BASE_DIR, file_url[1:]).replace(
            "/media/", "/uploads/"
        ),
    ]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )
    end = time.perf_counter()
    print(result.returncode, result.stdout, result.stderr)
    search = re.search(r"bpy.ops.wm.stl_export\(filepath=\"(.*\.stl)\"", result.stdout)
    if search:
        return {
            "status": result.returncode == 0,
            "details": {
                "duration": f"{end - start}",
                "cad_part": request.build_absolute_uri(
                    settings.STATIC_URL + search.group(1)
                ).replace("/output/", "/"),
            },
        }
    else:
        return {"status": False, "details": {"message": "cad part generation failed."}}

