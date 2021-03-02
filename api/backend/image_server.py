import os
import urllib.parse as url

from loguru import logger
from omegaconf import OmegaConf


class ImageServer(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info(f"Instantiating Image Server!")
            cls.__singleton = super(ImageServer, cls).__new__(cls)

            conf = OmegaConf.load("config/config.yml").image_server

            cls.__img_prefix = conf.img_prefix
            cls.__img_suffix = conf.img_suffix

            cls.__img_root = conf.img_root
            if not os.path.lexists(cls.__img_root):
                msg = f"Cannot find images root at {cls.__img_root}"
                logger.error(msg)
                raise RuntimeError(msg)

            # setup base url
            base_url = "https://" if conf.https else "http://"
            base_url += conf.host
            base_url += ":" + str(conf.port)
            base_url += conf.context_path
            cls.__base_url = base_url
        return cls.__singleton

    def __get_img_filename(self, img_id: str):
        img_fn = f"{self.__img_prefix}{img_id}{self.__img_suffix}"
        if not os.path.lexists(os.path.join(self.__img_root, img_fn)):
            logger.warning(f"Cannot find Image {img_id} at {img_fn}")
        return img_fn

    def get_img_url(self, img_id: str) -> str:
        img_file_name = self.__get_img_filename(img_id)
        return url.urljoin(self.__base_url, img_file_name)
