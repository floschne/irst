from enum import Enum, unique


@unique
class StudyType(str, Enum):
    RANKING = "ranking"
    LIKERT = "likert"
    RATING = "rating"
