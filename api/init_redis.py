import argparse
import os
from typing import List

import pandas as pd

from backend.db import RedisHandler
from models import GroundTruthSample


def generate_gt_samples(data_root: str) -> List[GroundTruthSample]:
    dataframe_path = os.path.join(data_root, "user_study_data.df.feather")
    assert os.path.lexists(dataframe_path), f"Cannot find DataFrame at {dataframe_path}"
    df = pd.read_feather(dataframe_path)

    def generate_gt_sample(row) -> GroundTruthSample:
        return GroundTruthSample(ds_id=row['wikicaps_id'],
                                 query=row['caption'],
                                 top_k_image_ids=row['top50_wids'].tolist())

    return df.apply(generate_gt_sample, axis=1).tolist()


def init_redis(data_root: str):
    assert os.path.lexists(data_root), f"Cannot find data root at {opts.data_root}"
    # generate GTSamples
    gt_samples = generate_gt_samples(opts.data_root)
    redis = RedisHandler()
    for gts in gt_samples:
        redis.store_gt_sample(gts)

    # reset the progress
    redis.reset_progress()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default=f'{os.getcwd()}/data')

    opts = parser.parse_args()
    init_redis(opts.data_root)
