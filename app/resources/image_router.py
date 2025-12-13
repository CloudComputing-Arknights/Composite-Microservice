from httpx import Response
from app.models.dto.image_dto import UploadSuccessResponse, ImageUrlResponse
from app.services.image_service import upload_image, get_image_url
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Annotated
import logging
logger = logging.getLogger("composite_api")

import os
import requests
image_router = APIRouter(
    tags=["Image"],
)

@image_router.post("/image/upload")
async def upload_image_endpoint(file: UploadFile = File(...), fcm_token: Annotated[str | None, Form()] = None):
    logger.info(f"Uploading image with FCM token: {fcm_token}")
    result = await upload_image(file)
    if result.status == "success" and fcm_token:
        cloud_function_url = os.getenv("CLOUD_FUNCTION_URL")
        payload = {
        "fcm_token": fcm_token,
        "title":"New Image Compressed",
        "body":"You have a new image compressed successfully, please check your app"
    }
        response = requests.post(cloud_function_url, json=payload)
        if response.status_code == 200:
           logger.info(f"FCM token {fcm_token} updated successfully, response: {str(Response)}")
        else:
            logger.error(f"Failed to update FCM token: {response.status_code}, response: {str(response)}")
            raise HTTPException(status_code=500, detail="Failed to update FCM token")
    
    return result

@image_router.get("/image/{filename}")
async def get_image_url_endpoint(filename: str):
    return await get_image_url(filename)