import os
import re
import subprocess
import sys
import time

from django.conf.urls.static import static
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from nanodjango import Django

app = Django()

settings.STATIC_URL = "/static/"
settings.STATICFILES_DIRS = [
    os.path.join(settings.BASE_DIR, "output"),
]
settings.STATIC_ROOT = os.path.join(settings.BASE_DIR, "staticfiles")
settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, "uploads")


@app.api.post("/preview")
def get_order_preview(request):
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
        "blender/blender",
        "--background",
        "-P",
        "generate_preview.py",
        "--",
        os.path.join(os.getcwd(), settings.BASE_DIR, file_url[1:]).replace(
            "/media/", "/uploads/"
        ),
    ]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )
    end = time.perf_counter()
    print(result.returncode, result.stdout, result.stderr)
    search = re.search(r"Saved: 'output/(.*\.png)'", result.stdout)
    if search:
        return {
            "status": result.returncode == 0,
            "details": {
                "duration": f"{end - start}",
                "preview": request.build_absolute_uri(
                    settings.STATIC_URL + search.group(1)
                ),
            },
        }
    else:
        return {"status": False, "details": {"message": "preview rendering failed."}}
