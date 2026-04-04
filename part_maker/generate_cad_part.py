import os
import uuid

import bpy

bpy.app.debug_wm = True  # Show all called operators

ASSETS_PATH = os.getcwd() + "/static/assets"
CAD_BLENDER_SCENE_PATH = f"{ASSETS_PATH}/chocolate_biscuit_CAD_part.blend"
CAD_PART_OBJECT_NAME = "ChocolateRelief_RealDisplacement_CADPart"
UUID = uuid.uuid1()
CAD_OUTPUT_FILENAME = f"output/chocolate_mold_matrix_insert_CAD_part_{UUID}.stl"


def main():
    # Load product staging scene
    bpy.ops.wm.open_mainfile(filepath=CAD_BLENDER_SCENE_PATH)

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
    main()
