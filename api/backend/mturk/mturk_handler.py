from typing import List, Optional, Dict

import boto3
from loguru import logger
from omegaconf import OmegaConf
from tqdm import tqdm

from backend.db import RedisHandler
from backend.mturk.external_question import ExternalQuestion
from models import EvalSample


class MTurkHandler(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info(f"Instantiating MTurk Handler!")
            cls.__singleton = super(MTurkHandler, cls).__new__(cls)

            cls.__conf = OmegaConf.load("config/config.yml").backend.mturk
            cls.sandbox = cls.__conf.sandbox

            cls.__mturk_env = {
                "live": {
                    "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
                    "preview": "https://www.mturk.com/mturk/preview",
                    "manage": "https://requester.mturk.com/mturk/manageHITs",
                    "reward": f"{cls.__conf.hit_reward_live}"
                },
                "sandbox": {
                    "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                    "preview": "https://workersandbox.mturk.com/mturk/preview",
                    "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
                    "reward": f"{cls.__conf.hit_reward_sandbox}"
                },
            }

            cls.__hit_type_id = None

            cls.__get_default_client(cls.__singleton)

            cls.__rh = RedisHandler()

        return cls.__singleton

    def init(self):
        self.__hit_type_id = self.__create_or_get_hit_type()

    def __get_default_client(self):
        self.__client = boto3.client(
            'mturk',
            endpoint_url=self.__mturk_env['sandbox' if self.sandbox else 'live']['endpoint'],
            region_name=self.__conf.aws_region_name,
            aws_access_key_id=self.__conf.aws_access_key,
            aws_secret_access_key=self.__conf.aws_secret,
        )
        self.__hit_type_id = self.__create_or_get_hit_type()

    def create_new_client(self, sandbox: bool, aws_access_key: str, aws_secret: str):
        self.__client = boto3.client(
            'mturk',
            endpoint_url=self.__mturk_env['sandbox' if sandbox else 'live']['endpoint'],
            region_name=self.__conf.aws_region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret,
        )
        self.__hit_type_id = self.__create_or_get_hit_type()

    def __create_or_get_hit_type(self) -> Optional[str]:
        logger.debug(f"Creating HIT Type...")
        try:
            resp = self.__client.create_hit_type(
                AutoApprovalDelayInSeconds=self.__conf.hit_auto_approval_delay_in_seconds,
                AssignmentDurationInSeconds=self.__conf.hit_assignment_duration_in_seconds,
                Reward=self.__mturk_env['sandbox' if self.sandbox else 'live']['reward'],
                Title=self.__conf.hit_title,
                Keywords=self.__conf.hit_keywords,
                Description=self.__conf.hit_description,
                # TODO hardcoded - do we want this in the config.yml?
                # https://docs.aws.amazon.com/de_de/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
                QualificationRequirements=[
                    {
                        'QualificationTypeId': '00000000000000000040',
                        'Comparator': 'GreaterThanOrEqualTo',
                        'IntegerValues': [
                            self.__conf.worker_quali_req_min_hits_approved,
                        ],
                        'ActionsGuarded': 'Accept'
                    },
                    {
                        'QualificationTypeId': '000000000000000000L0',
                        'Comparator': 'GreaterThanOrEqualTo',
                        'IntegerValues': [
                            self.__conf.worker_quali_req_min_percent_approved,
                        ],
                        'ActionsGuarded': 'Accept'
                    },
                ]
            )
            hit_type_id = resp['HITTypeId']
            logger.info(f"Created HIT Type {hit_type_id}")
            return hit_type_id
        except Exception as e:
            logger.error(f"Cannot create HIT Type")
            logger.error(f"Exception: {e}")

    def create_hit_from_es(self, es: EvalSample) -> Optional[Dict]:
        try:
            # create an ExternalQuestion
            eq = ExternalQuestion(es, base_url=self.__conf.external_question_base_url)
            # create the HIT
            resp = self.__client.create_hit_with_hit_type(
                HITTypeId=self.__hit_type_id,
                MaxAssignments=self.__conf.hit_max_assignments,
                LifetimeInSeconds=self.__conf.hit_lifetime,
                UniqueRequestToken=es.id,
                RequesterAnnotation=es.id,
                Question=eq.get_encoded()
            )
            logger.debug(f"Successfully created HIT {resp['HIT']['HITId']} for EvalSample {es.id}!")
            # store HIT Info
            self.__rh.store_hit_info(resp['HIT'], es)
            return resp['HIT']
        except Exception as e:
            logger.error(f"Cannot create HIT from EvalSample {es.id}. Exception: {e}")
            return None

    def create_hits_from_es(self, samples: List[EvalSample]):
        created = 0
        for es in tqdm(samples):
            created += 1 if self.create_hit_from_es(es) is not None else 0
        return created

    def delete_hit(self, hit_id: str):
        try:
            self.__client.update_expiration_for_hit(HITId=hit_id, ExpireAt=0)
            self.__client.delete_hit(HITId=hit_id)
            logger.debug(f"Deleted HIT {hit_id}")
            return True
        except Exception as e:
            logger.error(f"Cannot delete HIT {hit_id}! Exception: {e}")
            return False

    def delete_all_hits(self):
        deleted = 0
        hit_ids = self.list_hit_ids()
        for hid in tqdm(hit_ids):
            deleted += 1 if self.delete_hit(hid) else 0
        return deleted

    def list_hits(self) -> List[Dict]:
        try:
            hits = []
            next_token = None
            resp = self.__client.list_hits(MaxResults=100)
            if resp['NumResults'] > 0:
                hits.extend(resp['HITs'])
                next_token = resp['NextToken']
            while next_token is not None:
                resp = self.__client.list_hits(MaxResults=100, NextToken=next_token)
                if resp['NumResults'] > 0:
                    hits.extend(resp['HITs'])
                    next_token = resp['NextToken']
                else:
                    next_token = None
            logger.debug(f"Found {len(hits)} HITs!")
            return hits
        except Exception as e:
            logger.error(f"Cannot ListHITs! Exception: {e}")
            return []

    def list_hit_ids(self) -> List[str]:
        try:
            return [hit['HITId'] for hit in self.list_hits()]
        except Exception as e:
            logger.error(f"Cannot ListHIT IDs! Exception: {e}")

    def get_hit_info_via_es(self, es: EvalSample):
        return self.__rh.load_hit_info(es)

    def get_hit_info(self, hit_id: str) -> Optional[Dict]:
        try:
            hit = self.__client.get_hit(HITId=hit_id)['HIT']
            logger.debug(f"Successfully retrieved HIT {hit_id}")
            return hit
        except Exception as e:
            logger.error(f"Cannot retrieve HIT {hit_id}! Exception: {e}")
            return None

    def list_assignments_for_hit(self, hit_id: str) -> Optional[List[Dict]]:
        try:
            resp = self.__client.list_assignments_for_hit(HITId=hit_id)
            logger.debug(f"Found {resp['NumResults']} assignments for HIT {hit_id}")
            return resp['Assignments']
        except Exception as e:
            logger.error(f"Cannot list Assignments for HIT {hit_id}! Exception: {e}")
            return None

    def list_reviewable_hits(self) -> Optional[List[Dict]]:
        try:
            reviewable_hits = []
            next_token = None
            resp = self.__client.list_reviewable_hits(
                HITTypeId=self.__hit_type_id,
                MaxResults=100
            )
            if resp['NumResults'] > 0:
                reviewable_hits.extend(resp['HITs'])
                next_token = resp['NextToken']
            while next_token is not None:
                resp = self.__client.list_reviewable_hits(MaxResults=100, NextToken=next_token)
                if resp['NumResults'] > 0:
                    reviewable_hits.extend(resp['HITs'])
                    next_token = resp['NextToken']
                else:
                    next_token = None
            logger.debug(f"Found {len(reviewable_hits)} reviewable HITs!")
            return reviewable_hits
        except Exception as e:
            logger.error(f"Cannot list reviewable HITs! Exception: {e}")
            return None

    def list_reviewable_assignments(self) -> Optional[Dict]:
        reviewable_hits = self.list_reviewable_hits()
        # since we only have a little num of max assignments (3) per HIT we don't need to paginate through them
        return {r_hit['HITId']: self.list_assignments_for_hit(r_hit['HITId']) for r_hit in reviewable_hits}
