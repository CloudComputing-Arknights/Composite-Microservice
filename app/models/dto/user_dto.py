from pydantic import BaseModel


class SignInReq(BaseModel):
    username: str
    password: str


class SignInRes(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SignedInUserRes(BaseModel):
    pass
