import os
import time
import urllib.parse as url
from typing import List

import numpy as np
from loguru import logger
from omegaconf import OmegaConf
from init_imgs import init_images


class ImageServer(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info(f"Instantiating Image Server!")
            cls.__singleton = super(ImageServer, cls).__new__(cls)

            conf = OmegaConf.load("config/config.yml").image_server

            cls.__img_prefix = conf.img_prefix
            cls.__img_suffix = conf.img_suffix
            cls.__img_thumbnail_infix = conf.img_thumbnail_infix
            cls.__use_relative_url = bool(conf.relative_url)

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

            # setup relative url
            cls.__relative_url = conf.context_path
            if cls.__relative_url[-1] != '/':
                cls.__relative_url += '/'
            if cls.__relative_url[0] != '/':
                cls.__relative_url = '/' + cls.__relative_url

        return cls.__singleton

    def __get_img_filename(self, img_id: str):
        img_fn = f"{self.__img_prefix}{img_id}{self.__img_suffix}"
        if not os.path.lexists(os.path.join(self.__img_root, img_fn)):
            logger.warning(f"Cannot find Image {img_id} at {img_fn}")
        return img_fn

    def __get_thumbnail_filename(self, img_id: str):
        thumbnail_fn = f"{self.__img_prefix}{img_id}{self.__img_thumbnail_infix}{self.__img_suffix}"
        if not os.path.lexists(os.path.join(self.__img_root, thumbnail_fn)):
            logger.warning(f"Cannot find Image Thumbnail of {img_id} at {thumbnail_fn}")
        return thumbnail_fn

    def get_img_url(self, img_id: str, thumbnail: bool = False) -> str:
        img_fn = self.__get_img_filename(img_id) if not thumbnail else self.__get_thumbnail_filename(img_id)
        u = self.__relative_url if self.__use_relative_url else self.__base_url
        return url.urljoin(u, img_fn)

    def get_img_urls(self, img_ids: List[str], thumbnail: bool = False) -> List[str]:
        return [self.get_img_url(img_id, thumbnail) for img_id in img_ids]

    def get_img_id(self, img_url: str) -> str:
        u = self.__relative_url if self.__use_relative_url else self.__base_url
        img_id = img_url.replace(u, "") \
            .replace(self.__img_prefix, "") \
            .replace(self.__img_thumbnail_infix, "") \
            .replace(self.__img_suffix, "") \
            .replace("/", "")
        return img_id

    def get_img_ids(self, img_urls: List[str]) -> List[str]:
        return [self.get_img_id(img_url) for img_url in img_urls]

    def init_image_data(self):
        # we wait a random amount of time here to support multi-processing (gunicorn spawns multiple processes) so
        # only the instance that reads the init_flag first will init Redis! Otherwise it gets initialized multiple
        # times
        time.sleep(np.random.uniform(low=0.05, high=0.5))
        logger.info("Initializing Image Data")
        init_images(image_dir=self.__img_root)
