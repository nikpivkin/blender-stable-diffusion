import base64
import tempfile
from logging import Logger
from typing import BinaryIO
from typing import Literal

from . import log


def create_temp_file(prefix, suffix='.png') -> str:
    return tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix).name


logger: Logger = log.LOGGER.getChild(__package__)


def handle_error(error, msg='Error') -> Literal[False]:
    logger.error(f'{msg} : {error}')
    return False


def img2base64(img: BinaryIO) -> str:
    return base64.b64encode(img.read()).decode()


def base64ToImg(base64img: str) -> bytes:
    return base64.b64decode(base64img.replace('data:image/png;base64,', ''))
