from pydantic import BaseModel, Field


class AWSCreds(BaseModel):
    access_key: str = Field(description="AWS Access Key")
    secret: str = Field(description="AWS Secret Key")
