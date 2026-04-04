import os
import uuid
import sys
from pathlib import Path

import bpy

# bpy.app.debug_wm = True  # Show all called operators

CAD_BLENDER_SCENE_PATH = "chocolate_biscuit_CAD_part.blend"
CAD_PART_OBJECT_NAME = "ChocolateRelief_RealDisplacement_CADPart"
UUID = uuid.uuid1()
CAD_OUTPUT_FILENAME = f"output/chocolate_mold_matrix_insert_CAD_part_{UUID}.stl"

# Change input displacement texture and export to STL
def export_cad_part():
    if "--" not in sys.argv:
        print("No displacement image input parameter provided.")
        sys.exit(1)
    input_image_path = sys.argv[sys.argv.index("--") + 1]
    input_image = Path(input_image_path)
    if not input_image.is_file():
        print(f"Given path ({input_image_path}) is not an image.")
        sys.exit(1)


    # Load product staging scene
    bpy.ops.wm.open_mainfile(filepath=CAD_BLENDER_SCENE_PATH)

    # Replace displacement map file path on the fly (without saving file)
    chocoMapKey = "ChocolateHeightmap"
    if chocoMapKey not in bpy.data.images.keys():
        raise IndexError("Failed to export STL for part (source 3d file misses texture)")
    bpy.data.images[chocoMapKey].filepath = input_image_path

    # Export to STL
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_pattern(pattern=CAD_PART_OBJECT_NAME)
    try:
        ret = bpy.ops.wm.stl_export(
            filepath=CAD_OUTPUT_FILENAME,
            export_selected_objects=True,
            apply_modifiers=True,
        )
        assert ret == {"FINISHED"}
    except:
        raise RuntimeError("Failed to export to STL.")


if __name__ == "__main__":
    export_cad_part()
