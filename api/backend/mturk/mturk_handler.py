from typing import List, Optional, Dict, Union

import boto3
from loguru import logger
from tqdm import tqdm

from backend.db import RedisHandler
from backend.mturk.external_question import ExternalQuestion
from config import conf
from models import BaseSample, StudyType


class MTurkHandler(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            logger.info(f"Instantiating MTurk Handler!")
            cls.__singleton = super(MTurkHandler, cls).__new__(cls)

            cls.__conf = conf.backend.mturk
            cls.sandbox = cls.__conf.sandbox

            cls.__hit_config = {st: cls.__conf[st] for st in StudyType}

            cls.__hit_type_id = {st: None for st in StudyType}

            cls.__mturk_env = {
                "live": {
                    "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
                    "preview": "https://www.mturk.com/mturk/preview",
                    "manage": "https://requester.mturk.com/mturk/manageHITs"
                },
                "sandbox": {
                    "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                    "preview": "https://workersandbox.mturk.com/mturk/preview",
                    "manage": "https://requestersandbox.mturk.com/mturk/manageHITs"
                },
            }

            cls.__get_default_client(cls.__singleton)

            cls.__rh = RedisHandler()

        return cls.__singleton

    def init_hit_types(self):
        for st in StudyType:
            self.__hit_type_id[st] = self.__create_or_get_hit_type(st)

    def __get_default_client(self):
        self.__client = boto3.client(
            'mturk',
            endpoint_url=self.__mturk_env['sandbox' if self.sandbox else 'live']['endpoint'],
            region_name=self.__conf.aws_region_name,
            aws_access_key_id=self.__conf.aws_access_key,
            aws_secret_access_key=self.__conf.aws_secret,
        )
        self.init_hit_types()

    def create_new_client(self, sandbox: bool, aws_access_key: str, aws_secret: str):
        self.__client = boto3.client(
            'mturk',
            endpoint_url=self.__mturk_env['sandbox' if sandbox else 'live']['endpoint'],
            region_name=self.__conf.aws_region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret,
        )
        self.init_hit_types()

    @staticmethod
    def __parse_custom_hit_qualification_config(qualification_id: str,
                                                customHitConfig: Dict[str, Union[str, List[int]]]):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.create_hit_type
        comp_types = ['LessThan',
                      'LessThanOrEqualTo',
                      'GreaterThan',
                      'GreaterThanOrEqualTo',
                      'EqualTo',
                      'NotEqualTo',
                      'Exists',
                      'DoesNotExist',
                      'In',
                      'NotIn']

        actions = ['Accept', 'PreviewAndAccept', 'DiscoverPreviewAndAccept']

        try:
            # check comparator type
            comp_type = customHitConfig['comparator']
            if comp_type not in comp_types:
                raise ValueError(f'Comparator {customHitConfig["comparator"]} is not supported by MTurk!')
            is_existing_comp_type = 'Exist' in comp_type

            # check actions guarded
            if customHitConfig['actionsGuarded'] not in actions:
                raise ValueError(f'Action Guard {customHitConfig["actionsGuarded"]} is not supported by MTurk!')

            if not is_existing_comp_type:
                # we only need to check and provide IntegerValues for all comparators except Exist and DoesNotExist
                # check int values
                for intVal in customHitConfig['integerValues']:
                    if not type(intVal) == int:
                        raise ValueError(f'IntegerValue {intVal} is not an Integer!')
                int_values = list(customHitConfig['integerValues'])

                qualificationRequirement = {
                    'QualificationTypeId': qualification_id,
                    'Comparator': comp_type,
                    'IntegerValues': int_values,
                    'ActionsGuarded': customHitConfig['actionsGuarded']
                }

            else:
                qualificationRequirement = {
                    'QualificationTypeId': qualification_id,
                    'Comparator': comp_type,
                    'ActionsGuarded': customHitConfig['actionsGuarded']
                }

            return qualificationRequirement

        except ValueError as e:
            logger.error(f"Cannot create custom HIT qualification with ID {qualification_id}! {e}")

    def __create_or_get_hit_type(self, study_type: str) -> Optional[str]:
        logger.debug(f"Creating {study_type} HIT Type...")
        try:
            # https://docs.aws.amazon.com/de_de/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
            qualificationRequirements = [
                {
                    'QualificationTypeId': '00000000000000000040',
                    'Comparator': 'GreaterThanOrEqualTo',
                    'IntegerValues': [
                        self.__hit_config[study_type].worker_quali_req_min_hits_approved,
                    ],
                    'ActionsGuarded': 'Accept'
                },
                {
                    'QualificationTypeId': '000000000000000000L0',
                    'Comparator': 'GreaterThanOrEqualTo',
                    'IntegerValues': [
                        self.__hit_config[study_type].worker_quali_req_min_percent_approved,
                    ],
                    'ActionsGuarded': 'Accept'
                },
            ]

            # add custom qualifications from config
            if self.__hit_config[study_type].hit_custom_qualifications is not None:
                for qualification_id, quali_config in self.__hit_config[study_type].hit_custom_qualifications.items():
                    qualificationRequirements.append(self.__parse_custom_hit_qualification_config(qualification_id,
                                                                                                  quali_config))

            resp = self.__client.create_hit_type(
                AutoApprovalDelayInSeconds=self.__hit_config[study_type].hit_auto_approval_delay_in_seconds,
                AssignmentDurationInSeconds=self.__hit_config[study_type].hit_assignment_duration_in_seconds,
                Reward=str(self.__hit_config[study_type].hit_reward),
                Title=self.__hit_config[study_type].hit_title,
                Keywords=self.__hit_config[study_type].hit_keywords,
                Description=self.__hit_config[study_type].hit_description,
                QualificationRequirements=qualificationRequirements
            )

            hit_type_id = resp['HITTypeId']
            logger.info(f"Created HIT Type {hit_type_id}")
            return hit_type_id
        except Exception as e:
            logger.error(f"Cannot create HIT Type")
            logger.error(f"Exception: {e}")

    def create_hit_from_sample(self, sample: BaseSample) -> Optional[Dict]:
        try:
            # create an ExternalQuestion
            eq = ExternalQuestion(sample, base_url=self.__hit_config[sample.get_type()].external_question_base_url)
            # create the HIT
            resp = self.__client.create_hit_with_hit_type(
                HITTypeId=self.__hit_type_id[sample.get_type()],
                MaxAssignments=self.__hit_config[sample.get_type()].hit_max_assignments,
                LifetimeInSeconds=self.__hit_config[sample.get_type()].hit_lifetime,
                UniqueRequestToken=sample.id,
                RequesterAnnotation=sample.get_type(),  # use the type als requester annotation to filter later
                Question=eq.get_encoded()
            )
            logger.debug(
                f"Successfully created HIT {resp['HIT']['HITId']} for {sample.get_type().capitalize()}Sample {sample.id}!")
            # store HIT Info
            self.__rh.store_hit_info(resp['HIT'], sample)
            return resp['HIT']
        except Exception as e:
            logger.error(f"Cannot create HIT from {sample.get_type().capitalize()}Sample {sample.id}. Exception: {e}")
            return None

    def create_hits_from_samples(self, samples: List[BaseSample]):
        created = 0
        for sample in tqdm(samples):
            created += 1 if self.create_hit_from_sample(sample) is not None else 0
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

    def delete_all_hits(self, study_type: str):
        deleted = 0
        hit_ids = self.list_hit_ids(study_type)
        for hid in tqdm(hit_ids):
            deleted += 1 if self.delete_hit(hid) else 0
        return deleted

    def list_hits(self, study_type: str) -> List[Dict]:
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
            return [hit for hit in hits if hit['RequesterAnnotation'] == study_type]
        except Exception as e:
            logger.error(f"Cannot ListHITs! Exception: {e}")
            return []

    def list_hit_ids(self, study_type: str) -> List[str]:
        try:
            return [hit['HITId'] for hit in self.list_hits(study_type)]
        except Exception as e:
            logger.error(f"Cannot list HIT IDs! Exception: {e}")

    def get_hit_info_via_sample(self, sample: BaseSample):
        return self.__rh.load_hit_info(sample)

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
            asses = []
            next_token = None
            resp = self.__client.list_assignments_for_hit(HITId=hit_id)
            if resp['NumResults'] > 0:
                asses.extend(resp['Assignments'])
                next_token = resp['NextToken']
            while next_token is not None:
                resp = self.__client.list_assignments_for_hit(HITId=hit_id)
                if resp['NumResults'] > 0:
                    asses.extend(resp['Assignments'])
                    next_token = resp['NextToken']
                else:
                    next_token = None

            logger.debug(f"Found {len(asses)} assignments for HIT {hit_id}")
            return asses
        except Exception as e:
            logger.error(f"Cannot list Assignments for HIT {hit_id}! Exception: {e}")
            return None

    def list_reviewable_hits(self, study_type: str) -> Optional[List[Dict]]:
        try:
            reviewable_hits = []
            next_token = None
            resp = self.__client.list_reviewable_hits(
                HITTypeId=self.__hit_type_id[study_type],
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

    def list_submitted_assignments(self, study_type: str, return_only_ids: bool) -> List[Union[Dict, str]]:
        # get all hits of the study
        all_hits = self.list_hit_ids(study_type)

        # get all assignments of all hits
        asses = []
        for hit in all_hits:
            asses.extend(self.list_assignments_for_hit(hit_id=hit))

        # filter only submitted
        asses = [ass for ass in asses if ass is not None and ass['AssignmentStatus'] == 'Submitted']

        if return_only_ids:
            return [ass['AssignmentId'] for ass in asses if ass is not None]

        return asses

    def approve_submitted_assignments(self, study_type: str, feedback: str) -> int:
        asses = self.list_submitted_assignments(study_type, return_only_ids=True)
        return self.approve_assignments(asses, feedback)

    def approve_assignment(self, assignment_id: str, feedback: str) -> bool:
        if len(feedback) > 1024:
            logger.error("Feedback cannot be longer than 1024 characters!")
            return False
        if feedback is None:
            feedback = "Thank you for your work!"

        try:
            resp = self.__client.approve_assignment(
                AssignmentId=assignment_id,
                RequesterFeedback=feedback,
            )
        except Exception as e:
            logger.error(f"Error while approving Assignment with ID {assignment_id}")
            logger.error(e)
            return False
        logger.debug(f"Successfully approved Assignment with ID {assignment_id}")
        return True

    def approve_assignments(self, assignment_ids: List[str], feedback: str) -> int:
        res = sum([self.approve_assignment(assignment_id=aid, feedback=feedback) for aid in tqdm(assignment_ids)])
        if res != len(assignment_ids):
            logger.error("Error during approving Assignments!")
        return res

    def associate_qualification_with_worker(self,
                                            worker_id: str,
                                            qualification_type_id: str,
                                            integer_value: int = 1312) -> bool:
        if integer_value is None:
            integer_value = 1312
        try:
            resp = self.__client.associate_qualification_with_worker(
                QualificationTypeId=qualification_type_id,
                WorkerId=worker_id,
                IntegerValue=integer_value
            )
        except Exception as e:
            logger.error(f"Error while associating Qualification for Worker with ID {worker_id}\n"
                         f"QualificationTypeId: {qualification_type_id}\n"
                         f"IntegerValue: {integer_value}")
            logger.error(e)
            return False
        logger.debug(f"Successfully associated Qualification {qualification_type_id} for Worker with ID {worker_id}")
        return True

    def associate_qualification_with_workers(self,
                                             worker_ids: List[str],
                                             qualification_type_id: str,
                                             integer_value: int = 1312) -> int:
        res = sum([self.associate_qualification_with_worker(worker_id=wid,
                                                            qualification_type_id=qualification_type_id,
                                                            integer_value=integer_value) for wid in tqdm(worker_ids)])
        if res != len(worker_ids):
            logger.error("Error during associating Qualifications!")
        return res

    def disassociate_qualification_with_worker(self,
                                               worker_id: str,
                                               qualification_type_id: str,
                                               reason: str = "") -> bool:
        if len(reason) > 1024:
            logger.error("Reason cannot be longer than 1024 characters!")
            return False
        try:
            resp = self.__client.disassociate_qualification_from_worker(
                QualificationTypeId=qualification_type_id,
                WorkerId=worker_id,
                Reason=reason
            )
        except Exception as e:
            logger.error(f"Error while disassociating Qualification for Worker with ID {worker_id}\n"
                         f"QualificationTypeId: {qualification_type_id}\n"
                         f"Reason: {reason}")
            logger.error(e)
            return False
        logger.debug(f"Successfully associated Qualification {qualification_type_id} for Worker with ID {worker_id}")
        return True

    def disassociate_qualification_with_workers(self,
                                                worker_ids: List[str],
                                                qualification_type_id: str,
                                                reason: str = "") -> int:
        res = sum([self.disassociate_qualification_with_worker(worker_id=wid,
                                                               qualification_type_id=qualification_type_id,
                                                               reason=reason) for wid in tqdm(worker_ids)])
        if res != len(worker_ids):
            logger.error("Error during disassociating Qualifications!")
        return res

    def notify_workers(self, subject: str, message_text: str, worker_ids: List[str]) -> bool:
        def chunks(lst: List, n: int):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        if len(subject) > 200:
            logger.error("Subject cannot be longer than 200 characters!")
            return False
        if len(message_text) > 4096:
            logger.error("MessageText cannot be longer than 4096 characters!")
            return False
        try:
            for worker_chunk in chunks(worker_ids, 100):
                resp = self.__client.notify_workers(
                    Subject=subject,
                    MessageText=message_text,
                    WorkerIds=worker_chunk
                )
                if len(resp) != 0:  # FIXME
                    logger.error(f"Error while notifying Workers!\n"
                                 f"NotifyWorkersFailureStatuses: {resp}")

        except Exception as e:
            logger.error(f"Error while notifying Workers!")
            logger.error(e)
            return False

        return True

    def get_account_balance(self) -> Optional[Dict[str, str]]:
        try:
            resp = self.__client.get_account_balance()
            return resp
        except Exception as e:
            logger.error(f"Error while checking account balance!")
            logger.error(e)
        return None
