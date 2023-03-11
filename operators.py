import random
import time

import bpy

from . import sd_api
from . import util


def apply_stable_diffusion(scene):
    props = scene.sd_props

    timestamp = int(time.time())
    original_filename_prefix = f'sd-render-{timestamp}-1-before'
    generated_filename_prefix = f'sd-render-{timestamp}-2-after'

    render_file = save_render_to_file(scene, original_filename_prefix)

    generate_new_random_seed(scene)

    params = {
        'prompt': props.prompt_text,
        'negative_prompt': props.negative_prompt_text,
        'width': get_output_width(scene),
        'height': get_output_height(scene),
        'seed': props.seed,
        'sampler_index': props.sampling_method,
        'cfg_scale': props.cfg_scale,
        'steps': props.sampling_steps,
        'denoising_strength': round(1 - props.image_similarity, 2),
        'restore_faces': props.restore_faces,
        'tilling': props.tilling,
    }

    if props.extra_seed:
        params = {
            **params,
            'subseed': props.variation_seed,
            'subseed_strength': props.variation_strength,
            'seed_resize_from_h': props.resize_seed_from_height,
            'seed_resize_from_w': props.resize_seed_from_width,
        }

    with open(render_file, 'rb') as img:
        generated_img = sd_api.provideApi().img2img(params, img)

        if generated_img:
            tf = util.create_temp_file(generated_filename_prefix)
            with open(tf, 'wb') as f:
                f.write(generated_img)
            try:
                bpy.data.images.load(tf, check_existing=False)
            except Exception as e:
                return util.handle_error(e)
            return True
        else:
            return False


def get_output_width(scene):
    return round(scene.render.resolution_x * scene.render.resolution_percentage / 100)


def get_output_height(scene):
    return round(scene.render.resolution_y * scene.render.resolution_percentage / 100)


def generate_new_random_seed(scene):
    props = scene.sd_props
    if props.use_random_seed:
        props.seed = random.randint(1000000000, 2147483647)


def save_render_to_file(scene, filename_prefix):
    temp_file = util.create_temp_file(filename_prefix + '-')
    orig_render_file_format = scene.render.image_settings.file_format
    orig_render_color_mode = scene.render.image_settings.color_mode
    orig_render_color_depth = scene.render.image_settings.color_depth

    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'

    bpy.data.images['Render Result'].save_render(temp_file)

    scene.render.image_settings.file_format = orig_render_file_format
    scene.render.image_settings.color_mode = orig_render_color_mode
    scene.render.image_settings.color_depth = orig_render_color_depth

    return temp_file


classes = ()


register, unregister = bpy.utils.register_classes_factory(classes)
