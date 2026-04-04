# Run me from inside Blender
import os
import uuid
import sys
from pathlib import Path

import bpy

# bpy.app.debug_wm = True # Show all called operators

PREVIEW_BLENDER_SCENE_PATH = f"chocolate_biscuit_rig_micro_displacement.blend"
PREVIEW_OUTPUT_PREFIX = "output/chocolate_preview_"
UUID = uuid.uuid1()
PREVIEW_OUTPUT_FILENAME = f"{PREVIEW_OUTPUT_PREFIX}{UUID}.png"


# Change input displacement texture and render to image file
def render_preview():
    if "--" not in sys.argv:
        print("No displacement image input parameter provided.")
    input_image_path = sys.argv[sys.argv.index["--"] + 1]
    input_image = Path(input_image_path)
    if not input_image.is_file():
        print(f"Given path ({input_image_path}) is not an image.")
        sys.exit(1)

    # Load product staging scene
    bpy.ops.wm.open_mainfile(filepath=PREVIEW_BLENDER_SCENE_PATH)

    # Replace displacement map file path on the fly (without saving file)
    chocoMapKey = "ChocolateHeightmap"
    if chocoMapKey not in bpy.data.images.keys():
        raise IndexError("Failed to render preview (source 3d file misses texture)")
    bpy.data.images[chocoMapKey].filepath = input_image_path

    # Make a regular render
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.render.filepath = PREVIEW_OUTPUT_FILENAME

    # Render a still image
    try:
        ret = bpy.ops.render.render(write_still=True)
        assert ret == {"FINISHED"}
    except:
        raise RuntimeError("Failed to render preview.")


if __name__ == "__main__":
    render_preview()
