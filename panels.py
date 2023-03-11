import bpy


class RenderPanelMixin:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'


class SD_PT_main(RenderPanelMixin, bpy.types.Panel):
    bl_label = 'Stable Diffusion'
    bl_idname = 'SD_PT_main'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.sd_props

        row = layout.row()
        row.prop(props, 'is_enabled')


class RenderChildPanelMixin(RenderPanelMixin):
    bl_parent_id = 'SD_PT_main'


class SD_PT_base_options(RenderChildPanelMixin, bpy.types.Panel):
    bl_label = 'Prompt'
    bl_idname = 'SD_PT_command'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.sd_props

        row = layout.row()
        row.label(text='Prompt:')

        row = layout.row()
        row.scale_y = 1.8
        row.prop(props, 'prompt_text', text='')

        row = layout.row()
        row.label(text='Negative prompt:')

        row = layout.row()
        row.scale_y = 1.8
        row.prop(props, 'negative_prompt_text', text='')


class SD_PT_advaced_options(RenderChildPanelMixin, bpy.types.Panel):
    bl_label = 'Advanced Options'
    bl_idname = 'SD_PT_advaced_options'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.sd_props

        # Seed
        row = layout.row()

        col = row.column()
        col.prop(props, 'use_random_seed')

        col = row.column()
        col.prop(props, 'seed', slider=False)
        col.enabled = not props.use_random_seed

        # Seed extra
        row = layout.row()
        row.prop(props, 'extra_seed')

        if props.extra_seed:
            row = layout.row()
            row.column().prop(props, 'variation_seed', slider=False)
            row.column().prop(props, 'variation_strength', slider=False)

            row = layout.row()
            row.column().prop(props, 'resize_seed_from_width', slider=False)
            row.column().prop(props, 'resize_seed_from_height', slider=False)

        row = layout.row()
        row.column().label(text='Sampling steps')
        row.column().prop(props, 'sampling_steps', text='', slider=False)

        row = layout.row()
        row.column().label(text='CFG scale')
        row.column().prop(props, 'cfg_scale', text='', slider=False)

        row = layout.row()
        row.column().label(text='Image similarity')
        row.column().prop(props, 'image_similarity', text='', slider=False)

        row = layout.row()
        row.column().label(text='Sampler')
        row.column().prop(props, 'sampling_method', text='')

        row = layout.row()
        row.column().prop(props, 'restore_faces')
        row.column().prop(props, 'tilling')


classes = (SD_PT_main, SD_PT_base_options, SD_PT_advaced_options)


register, unregister = bpy.utils.register_classes_factory(classes)
