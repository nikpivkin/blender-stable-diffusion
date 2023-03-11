bl_info = {
    'name': 'Stable Diffusion',
    'author': 'Nikita Pivkin',
    'description': '',
    'blender': (2, 80, 0),
    'version': (0, 0, 1),
    'location': 'Render Properties > Stable Diffusion',
    'warning': '',
    'category': 'Render',
}

if 'bpy' in locals():
    import importlib

    importlib.reload(panels)  # noqa: F821
    importlib.reload(properties)  # noqa: F821
    importlib.reload(preferences)  # noqa: F821
    importlib.reload(handlers)  # noqa: F821
    importlib.reload(operators)  # noqa: F821
    importlib.reload(task_queue)  # noqa: F821
else:
    import bpy  # noqa: F401
    from . import panels
    from . import properties
    from . import preferences
    from . import handlers
    from . import operators
    from . import task_queue


def register():
    panels.register()
    properties.register()
    preferences.register()
    handlers.register()
    operators.register()
    task_queue.register()


def unregister():
    panels.unregister()
    properties.unregister()
    preferences.unregister()
    handlers.unregister()
    operators.unregister()
    task_queue.unregister()


if __name__ == '__main__':
    register()
