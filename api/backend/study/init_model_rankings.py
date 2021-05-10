import glob
import os
import time

import numpy as np
import pandas as pd
from loguru import logger

from backend.db import RedisHandler
from config import conf
from models import ModelRanking


def init_model_rankings():
    # we wait a random amount of time here to support multi-processing (gunicorn spawns multiple processes) so
    # only the instance that reads the init_flag first will init Redis! Otherwise it gets initialized multiple
    # times
    time.sleep(np.random.uniform(low=0.3, high=1.0))
    if len(RedisHandler().list_model_rankings(1)) != 1:
        data_root = conf.study_initialization.model_rankings.data_root
        if not os.path.lexists(data_root):
            logger.error(f"Cannot read Dataframe {data_root}")
            raise FileNotFoundError(f"Cannot find Dataframe at {data_root}")

        if os.path.isdir(data_root):
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
            dataframe = feathers[0]
        elif os.path.isfile(data_root):
            dataframe = data_root
        else:
            logger.error(f"Cannot read Dataframe {data_root}")
            raise FileNotFoundError(f"Cannot find Dataframe at {data_root}")

        logger.info(f"Initializing ModelRankings from Dataframe {dataframe}")
        # load the Dataframe
        df = pd.read_feather(dataframe)

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
        logger.info(f"Instantiated {len(rankings)} ModelRankings from Dataframe {dataframe}")

        # shuffle and slice
        if conf.study_initialization.model_rankings.shuffle:
            logger.debug("Shuffling ModelRankings")
            np.random.shuffle(rankings)

        # store the ModelRankings
        for mr in rankings:
            RedisHandler().store_model_ranking(mr)
