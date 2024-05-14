import pydantic


class UserCredentials(pydantic.BaseModel):
    username: str
    password_hash: str
