import bpy

from . import config


class StableDiffusionPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    stable_diffusion_url: bpy.props.StringProperty(
        name='URL of the Stable Diffusion Web Server',
        description='The location of the web server that is currently running on your local machine',
        default=config.default_sd_url,
    )

    def draw(self, _):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text='Local Web Server URL:')
        row.prop(self, 'stable_diffusion_url', text='')


def get_addon_preferences(context=None):
    if context is None:
        context = bpy.context
    prefs = context.preferences.addons.get(__package__, None)
    if prefs:
        return prefs.preferences
    return None


def get_stable_diffusion_url(context=None):
    return get_addon_preferences(context).stable_diffusion_url.rstrip('/').strip()


classes = (StableDiffusionPreferences,)


register, unregister = bpy.utils.register_classes_factory(classes)
