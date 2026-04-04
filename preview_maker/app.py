from typing import Annotated
import uuid
import glob
import os
import shutil
import subprocess

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

UPLOADS_DIR = "uploads"
OUTPUT_DIR = "output"
STATIC_PATH = "/static"

app.mount(STATIC_PATH, StaticFiles(directory=OUTPUT_DIR), name="static")

@app.get("/preview/")
async def get_previews():
    list_of_files = glob.glob(f"{OUTPUT_DIR}/*")
    return {"files": list_of_files}

@app.post("/preview/")
async def get_order_preview(file: UploadFile | None = None):
    UUID = uuid.uuid1()
    input_displacement_texture_filename = f"{UPLOADS_DIR}/displacement_map_{UUID}.png"
    print(input_displacement_texture_filename)

    if not file:
        return {"message": "No upload file sent"}
    else:
        try:
            with open(input_displacement_texture_filename, "wb") as f:
                shutil.copyfileobj(file.file, f)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Something went wrong" + str(e))
        finally:
            file.file.close()

        command = [
            "uv",
            "run",
            "generate_preview.py",
            "--",
            os.path.join(os.getcwd(), input_displacement_texture_filename),
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        list_of_files = glob.glob(f"{OUTPUT_DIR}/*")
        latest_preview_file = max(list_of_files, key=os.path.getctime) if list_of_files else ""
        return {"filename": latest_preview_file.replace(OUTPUT_DIR, STATIC_PATH)}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8036, reload=True)
