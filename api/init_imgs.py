import argparse
import glob
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from PIL import Image
from loguru import logger
from tqdm import tqdm

LOCK_FILE = '__lock_file__'


def convert_to_webp(pth: str,
                    webp: bool = True,
                    webp_quality: int = 50,
                    remove_original: bool = True,
                    thumbnails: bool = True,
                    thumbnail_size: int = 120):
    f, _ = os.path.splitext(pth)
    assert os.path.lexists(pth), f"Cannot find image at {pth}"
    with Image.open(pth) as im:
        if webp:
            im.save(f + ".webp", "WEBP", quality=webp_quality, lossless=True, method=6)
        if thumbnails:
            im.thumbnail((thumbnail_size, thumbnail_size))
            im.save(f + "_thumbnail.webp", "WEBP", quality=85, lossless=True, method=6)
    if remove_original:
        os.remove(pth)

    return


def create_lock_file(image_dir: str):
    pth = os.path.join(image_dir, LOCK_FILE)
    logger.info(f"Created LOCK FILE at {pth}")
    with open(pth, 'w') as lf:
        lf.write(f'created: {datetime.now()}')


def remove_lock_file(image_dir: str):
    pth = os.path.join(image_dir, LOCK_FILE)
    assert lock_file_exists(image_dir), f"Cannot find LOCK FILE {pth}!"
    logger.info(f"Removed LOCK FILE at {pth}")
    os.remove(pth)


def lock_file_exists(image_dir: str):
    return os.path.isfile(os.path.join(image_dir, LOCK_FILE))


def init_images(image_dir: str = '../data/images/',
                n_workers: int = 8,
                webp: bool = True,
                webp_quality: int = 50,
                remove_original: bool = True,
                thumbnails: bool = True,
                thumbnail_size: int = 120):
    assert os.path.lexists(image_dir), f"Cannot find {image_dir}!"

    if not lock_file_exists(image_dir):
        create_lock_file(image_dir)
        imgs = []
        for ext in ['png', 'jpg', 'jpeg']:
            imgs += glob.glob(f"{image_dir}/*.{ext}")
            imgs += glob.glob(f"{image_dir}/*.{ext.upper()}")
        if len(imgs) == 0:
            logger.info(f"All images are already initialized!")
            remove_lock_file(image_dir)
            return

        logger.info(f"Found {len(imgs)} images to convert!")
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            with tqdm(total=len(imgs)) as progress:
                futures = []
                for pth in imgs:
                    future = executor.submit(convert_to_webp,
                                             pth,
                                             webp,
                                             webp_quality,
                                             remove_original,
                                             thumbnails,
                                             thumbnail_size)
                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)

                # wait for all complete
                for f in futures:
                    f.result()

        remove_lock_file(image_dir)
    else:
        with open(os.path.join(image_dir, LOCK_FILE), 'r') as lf:
            logger.warning(f"Image initialization already started at {lf.read()}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default='../data/images/')
    parser.add_argument('--n_workers', type=int, default=8)
    parser.add_argument('--webp', action='store_true', default=True,
                        help='If True, all images get converted to webp format')
    parser.add_argument('--webp_quality', type=int, default=50, help='WebP quality between [0, 100]')
    parser.add_argument('--remove_original', action='store_true', default=True,
                        help='If True, all original images get removed')
    parser.add_argument('--thumbnails', action='store_true', default=True,
                        help='If True, thumbnails of all images are created')
    parser.add_argument('--thumbnail_size', type=int, default=120,
                        help='Size of the thumbnails in px (e.g. 120 means 120x120px)')

    opts = parser.parse_args()

    init_images(opts.image_dir,
                opts.n_workers,
                opts.webp,
                opts.webp_quality,
                opts.remove_original,
                opts.thumbnails,
                opts.thumbnail_size)
