import glob
import os

import numpy as np
import pandas as pd
from loguru import logger

from backend.db import RedisHandler
from config import conf
from models import ModelRanking


def init_model_rankings():
    if len(RedisHandler().list_model_rankings(1)) != 1:
        data_root = conf.study_initialization.model_rankings.data_root
        if not os.path.lexists(data_root) or not os.path.isdir(data_root):
            logger.error(f"Cannot read data root {data_root}")
            raise FileNotFoundError(f"Cannot find data root at {data_root}")

        # find the feather serialized Dataframe in the data root
        feathers = glob.glob(os.path.join(data_root, "*.df.feather"))
        if len(feathers) != 1:
            logger.error(
                f"Found multiple Dataframes! Please make sure only one Dataframe like '*.df.feather'"
                f"exists is in {data_root}!"
            )
            raise FileExistsError(
                f"Found multiple Dataframes! Please make sure only one Dataframe like '*.df.feather'"
                f"exists is in {data_root}!"
            )

        logger.info(f"Initializing ModelRankings from Dataframe {feathers[0]}")
        # load the Dataframe
        df = pd.read_feather(feathers[0])

        # make sure the mandatory columns exist
        for k in ['sample_id', 'caption', 'top_k_matches']:
            if k not in df.columns:
                logger.error(f"Cannot find {k} in the columns of the DataFrame!")
                raise IndexError(f"Cannot find {k} in the columns of the DataFrame!")

        # we don't use lambda for cleaner code
        def generate_model_ranking(row) -> ModelRanking:
            return ModelRanking(ds_id=row['sample_id'],
                                query=row['caption'],
                                top_k_image_ids=row['top_k_matches'].tolist())

        # generate ModelRankings from DataFrame
        rankings = df.apply(generate_model_ranking, axis=1).tolist()

        # shuffle and slice
        if conf.study_initialization.model_rankings.shuffle:
            np.random.shuffle(rankings)

        # store the ModelRankings
        for mr in rankings:
            RedisHandler().store_model_ranking(mr)
