from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(description='User ID')
    password: str = Field(description='Password in clear text. DOES NOT GET PERSISTED!')
