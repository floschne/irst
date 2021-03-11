import argparse
import os
import glob
from tqdm import tqdm
from PIL import Image

from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_to_webp(im, f):
    im.save(f + ".webp", "WEBP", quality=opts.webp_quality, lossless=True, method=6)

def create_thumbnail(im, f, size):
    im.thumbnail((size, size))
    im.save(f + "_thumbnail.webp", "WEBP", quality=opts.webp_quality, lossless=True, method=6)

def run(pth, opts):
    f, _ = os.path.splitext(pth)
    assert os.path.lexists(pth), f"Cannot find image at {pth}"
    with Image.open(pth) as im:
        if opts.webp:
            convert_to_webp(im, f)
        if opts.thumbnails:
            create_thumbnail(im, f, opts.thumbnail_size)
    if opts.remove_original:
        os.remove(pth)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, default='./data/images/')
    parser.add_argument('--n_workers', type=int, default=8)
    parser.add_argument('--webp', action='store_true', default=True, help='If True, all images get converted to webp format')
    parser.add_argument('--webp_quality', type=int, default=50, help='WebP quality between [0, 100]')
    parser.add_argument('--remove_original', action='store_true', default=True, help='If True, all original images get removed')
    parser.add_argument('--thumbnails', action='store_true', default=True, help='If True, thumbnails of all images are created')
    parser.add_argument('--thumbnail_size', type=int, default=120, help='Size of the thumbnails in px (e.g. 120 means 120x120px)')

    opts = parser.parse_args()

    assert os.path.lexists(opts.image_dir), f"Cannot find {opts.image_dir}!"
    
    imgs = glob.glob(f"{opts.image_dir}*.png")
    print(f"Found {len(imgs)} images!")

    with ThreadPoolExecutor(max_workers=opts.n_workers) as executor:
        with tqdm(total=len(imgs)) as progress:
            futures = []
            for pth in imgs:
                future = executor.submit(run, pth, opts)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)
