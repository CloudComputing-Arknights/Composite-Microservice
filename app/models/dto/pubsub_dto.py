from pydantic import BaseModel

class PubSubMessage(BaseModel):
    data: str
    messageId: str
    publishTime: str


class PubSubEnvelope(BaseModel):
    message: PubSubMessage
    subscription: str