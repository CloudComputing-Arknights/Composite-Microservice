from pydantic import BaseModel

class UploadSuccessResponse(BaseModel):
    status: str
    filename: str
    message: str

class ImageUrlResponse(BaseModel):
    url: str