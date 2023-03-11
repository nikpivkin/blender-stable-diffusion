import bpy
from bpy.app.handlers import persistent

from . import operators
from . import task_queue


@persistent
def render_complete_handler(scene):
    if not scene.sd_props.is_enabled:
        return
    task_queue.put(lambda: operators.apply_stable_diffusion(scene))


@persistent
def render_render_cancel(scene):
    if not scene.sd_props.is_enabled:
        return


def register():
    bpy.app.handlers.render_complete.append(render_complete_handler)
    bpy.app.handlers.render_cancel.append(render_render_cancel)


def unregister():
    bpy.app.handlers.render_complete.remove(render_complete_handler)
    bpy.app.handlers.render_cancel.remove(render_render_cancel)
