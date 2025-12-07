import os
from datetime import timedelta
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
from app.models.dto.image_dto import UploadSuccessResponse, ImageUrlResponse
import uuid
from datetime import timedelta
load_dotenv()

app = FastAPI()


BUCKET_NAME = os.getenv("IMAGE_BUCKET_NAME")  
CREDENTIALS_FILE = os.getenv("GCS_IMAGE_KEY_FILE")




if os.path.exists(CREDENTIALS_FILE):
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    storage_client = storage.Client(credentials=credentials)
else:
    raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")

def get_bucket():
    return storage_client.bucket(BUCKET_NAME)


async def upload_image(file: UploadFile = File(...)):
    """
    upload image to GCS
    """
    try:
        bucket = get_bucket()
        # create blob object (file object in GCS)
        # use uuid to rename file, prevent file name conflict overwrite
        file_name = f"{uuid.uuid4()}_{str(file.filename).split('.')[0]}"
        blob = bucket.blob(file_name)
        # upload file from memory to GCS
        blob.upload_from_file(file.file, content_type=file.content_type)

        return UploadSuccessResponse(
            status="success",
            filename=file_name,
            message="file uploaded successfully"
        )
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="file upload failed")


async def get_image_url(filename: str):
    """
    get image url from GCS
    the frontend can use this url to display the image
    """
    try:
        bucket = get_bucket()
        blob = bucket.blob(filename)
        
        if not blob.exists():
            raise HTTPException(status_code=404, detail="image not found")
            
        # generate signed url, valid for 15 minutes, for security and performance
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="GET"
        )
        
        return ImageUrlResponse(url=signed_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get image url failed: {str(e)}")

