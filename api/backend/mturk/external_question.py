import urllib.parse

# https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_ExternalQuestionArticle.html
from models import RankingSample


class ExternalQuestion(object):
    def __init__(self, rs: RankingSample, base_url: str, frame_height: int = 0):
        self.schema_url = "http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd"
        self.external_base_url = base_url
        self.frame_height = frame_height if frame_height > 0 else 0
        self.ranking_sample = rs

    def __build_external_url(self) -> str:
        return f"{self.external_base_url}{self.ranking_sample.id}"

    def __str__(self):
        return str(
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<ExternalQuestion xmlns="{self.schema_url}">'
            f'<ExternalURL>{self.__build_external_url()}</ExternalURL>'
            f'<FrameHeight>{self.frame_height}</FrameHeight>'
            '</ExternalQuestion>'
        )

    def get_encoded(self) -> str:
        return str(self)#urllib.parse.quote_plus(str(self), safe=';/?:@&=+$,')
