import argparse
import glob
import os
from typing import List

import pandas as pd

from backend.db import RedisHandler
from models import ModelRanking


def generate_model_rankings(data_root: str, num_samples: int) -> List[ModelRanking]:
    feathers = glob.glob(os.path.join(data_root, "*.df.feather"))
    assert len(feathers) == 1, \
        f"Found multiple datasources: {feathers}! Please make sure only one datasource exists is in {data_root}!"
    dataframe_path = feathers[0]
    assert os.path.lexists(dataframe_path), f"Cannot find DataFrame at {dataframe_path}"
    df = pd.read_feather(dataframe_path)

    for k in ['sample_id', 'caption', 'top_k_matches']:
        assert k in df.columns, f"Cannot find {k} in the DataFrames columns!"

    def generate_model_ranking(row) -> ModelRanking:
        return ModelRanking(ds_id=row['sample_id'],
                            query=row['caption'],
                            top_k_image_ids=row['top_k_matches'].tolist())

    return df.apply(generate_model_ranking, axis=1).tolist()[:num_samples]


def init_study_data(data_root: str, flush: bool, num_samples: int = -1):
    assert os.path.lexists(data_root), f"Cannot find data root at {data_root}"
    rh = RedisHandler()
    if flush:
        rh.flush(auth=False)

    # generate ModelRankings
    mrs = generate_model_rankings(data_root, num_samples)
    for mr in mrs:
        rh.store_model_ranking(mr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default=f'../data')
    parser.add_argument('--flush', default=True, action='store_true')
    parser.add_argument('--num_samples', type=int, default=-1)

    opts = parser.parse_args()
    init_study_data(opts.data_root, opts.flush)
