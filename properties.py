import bpy


class StableDiffusionProperties(bpy.types.PropertyGroup):
    """
    https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/f968270fec57d4818b823afb8023ce24b669e426/javascript/hints.js
    """

    is_enabled: bpy.props.BoolProperty(
        name='Enable Stable Diffusion',
        default=True,
        description='Generate a new image automatically after each render. When off, you will need to manually generate a new image',
    )

    # base

    prompt_text: bpy.props.StringProperty(  # type: ignore
        name='Prompt',
        description='Describe anything for Stable Diffusion to create',
        default='Stable Diffusion',
    )

    negative_prompt_text: bpy.props.StringProperty(
        name='Negative propmpt',
        description='Optionally, describe what Stable Diffusion needs to steer away from',
    )

    # advanced

    use_random_seed: bpy.props.BoolProperty(name='Random seed', default=True)

    seed: bpy.props.IntProperty(
        name='Seed',
        default=-1,
        min=-1,
        description="A value that determines the output of random number generator - if you create an image with same parameters and seed as another image, you'll get the same result",
    )

    extra_seed: bpy.props.BoolProperty(
        name='Extra seed',
        default=False,
    )

    variation_seed: bpy.props.IntProperty(
        name='Variation seed',
        default=-1,
        min=-1,
        description='Seed of a different picture to be mixed into the generation.',
    )

    variation_strength: bpy.props.FloatProperty(
        name='Variation strength',
        default=0,
        min=0,
        max=1,
        description='How strong of a variation to produce. At 0, there will be no effect. At 1, you will get the complete picture with variation seed (except for ancestral samplers, where you will just get something).',
    )

    resize_seed_from_width: bpy.props.IntProperty(
        name='Resize seed from width',
        default=0,
        min=0,
        max=2048,
        description='Make an attempt to produce a picture similar to what would have been produced with same seed at specified resolution',
    )

    resize_seed_from_height: bpy.props.IntProperty(
        name='Resize seed from height',
        default=0,
        min=0,
        max=2048,
        description='Make an attempt to produce a picture similar to what would have been produced with same seed at specified resolution',
    )

    cfg_scale: bpy.props.FloatProperty(
        name='CFG scale',
        default=7,
        min=1,
        max=30,
        description='Classifier Free Guidance Scale - how strongly the image should conform to prompt - lower values produce more creative results',
    )

    image_similarity: bpy.props.FloatProperty(
        name='Image Similarity',
        default=0.4,
        soft_min=0.0,
        soft_max=0.8,
        min=0.0,
        max=1.0,
        description='How closely the final image will match the initial rendered image. Values around 0.1-0.4 will turn simple renders into new creations. Around 0.5 will keep a lot of the composition, and transform into something like the prompt. 0.6-0.7 keeps things more stable between renders. Higher values may require more steps for best results. You can set this to 0.0 to use only the prompt',
    )

    sampling_steps: bpy.props.IntProperty(
        name='Sampling steps',
        default=20,
        min=1,
        max=150,
        description='How many times to improve the generated image iteratively; higher values take longer; very low values can produce bad results',
    )

    batch_count: bpy.props.IntProperty(
        name='Batch count',
        default=1,
        min=1,
        max=100,
        description='How many batches of images to create (has no impact on generation performance or VRAM usage)',
    )

    batch_size: bpy.props.IntProperty(
        name='Batch size',
        default=1,
        min=1,
        max=8,
        description='How many image to create in a single batch (increases generation performance at cost of higher VRAM usage)',
    )

    restore_faces: bpy.props.BoolProperty(name='Restore faces', default=False)

    tilling: bpy.props.BoolProperty(
        name='Tilling', default=False, description='Produce an image that can be tiled.',
    )

    sampling_method: bpy.props.EnumProperty(
        name='Sampling method',
        items=[
            ('Euler', 'Euler', '', 10),
            ('Euler a', 'Euler a', '', 20),
            ('Heun', 'Heun', '', 30),
            ('DPM2', 'DPM2', '', 40),
            ('DPM2 a', 'DPM2 a', '', 50),
            ('LMS', 'LMS', '', 60),
            ('LMS Karras', 'LMS Karras', '', 62),
            ('DPM fast', 'DPM fast', '', 70),
            ('DPM adaptive', 'DPM adaptive', '', 80),
            ('DPM++ 2S a Karras', 'DPM++ 2S a Karras', '', 90),
            ('DPM++ 2M Karras', 'DPM++ 2M Karras', '', 100),
            ('DPM++ 2S a', 'DPM++ 2S a', '', 110),
            ('DPM++ 2M', 'DPM++ 2M', '', 120),
            ('PLMS', 'PLMS', '', 200),
            ('DDIM', 'DDIM', '', 210),
            ('DPM2 Karras', 'DPM2 Karras', '', 220),
            ('DPM2 a Karras', 'DPM2 a Karras', '', 230),
        ],
        default=20,
        description='Which algorithm to use to produce the image',
    )


classes = (StableDiffusionProperties,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.sd_props = bpy.props.PointerProperty(
        type=StableDiffusionProperties,
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.sd_props
