from abc import ABC
from abc import abstractmethod
from typing import BinaryIO
from typing import Literal

import bpy
import requests

from . import preferences
from . import util


class StableDiffusionAPI(ABC):
    default_headers = {
        'User-Agent': 'Blender/' + bpy.app.version_string,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    @abstractmethod
    def img2img(
        self,
        params: dict,
        img: BinaryIO,
    ) -> bytes | Literal[False]:
        ...


class Automatic1111API(StableDiffusionAPI):
    IMG_2_IMG_ENDPOINT = '/sdapi/v1/img2img'

    def img2img(self, params: dict, img: BinaryIO) -> bytes | Literal[False]:
        params['init_images'] = [util.img2base64(img)]

        url = preferences.get_stable_diffusion_url() + self.IMG_2_IMG_ENDPOINT

        try:
            response = requests.post(
                url, json=params, headers=self.default_headers,
            )
            if response.status_code != 200:
                return util.handle_error(response.content)
            return util.base64ToImg(response.json()['images'][0])
        except Exception as e:
            return util.handle_error(error=e)


def provideApi() -> StableDiffusionAPI:
    return Automatic1111API()
