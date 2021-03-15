from typing import List, Optional, Dict

import boto3
from loguru import logger
from omegaconf import OmegaConf

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

            cls.__client = boto3.client(
                'mturk',
                endpoint_url=cls.__mturk_env['sandbox' if cls.sandbox else 'live']['endpoint'],
                region_name=cls.__conf.aws_region_name,
                aws_access_key_id=cls.__conf.aws_access_key,
                aws_secret_access_key=cls.__conf.aws_secret,
            )

            cls.__rh = RedisHandler()

        return cls.__singleton

    def init(self):
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
        logger.debug(f"Creating HIT from EvalSample {es.id}")
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
            logger.debug(f"Successfully created HIT {resp['HIT']} for EvalSample {es.id}!")

            # store HIT Info
            self.__rh.store_hit_info(resp['HIT'], es)

            return resp['HIT']
        except Exception as e:
            logger.error(f"Cannot create HIT from EvalSample {es.id}")
            logger.error(f"Exception: {e}")
            return None

    def create_hits_from_es(self, samples: List[EvalSample]):
        for es in samples:
            self.create_hit_from_es(es)

    def delete_hit(self, hit_id: str):
        try:
            self.__client.update_expiration_for_hit(HITId=hit_id, ExpireAt=0)
            self.__client.delete_hit(HITId=hit_id)
            logger.debug(f"Deleted HIT {hit_id}")
            return True
        except Exception as e:
            logger.error(f"Cannot delete HIT! Exception: {e}")
            return False

    def delete_all_hits(self):
        hit_ids = self.list_hit_ids()
        for hid in hit_ids:
            self.delete_hit(hid)

    def list_hits(self) -> List[Dict]:
        try:
            resp = self.__client.list_hits()
            logger.debug(f"Found {resp['NumResults']} HITs!")
            return resp['HITs']
        except Exception as e:
            logger.error(f"Cannot delete HIT! Exception: {e}")

    def list_hit_ids(self) -> List[str]:
        try:
            resp = self.__client.list_hits()
            logger.debug(f"Found {resp['NumResults']} HITs!")
            return resp['HITs']
        except Exception as e:
            logger.error(f"Cannot delete HIT! Exception: {e}")

    def get_hit_info(self, es: EvalSample):
        return self.__rh.load_hit_info(es)
