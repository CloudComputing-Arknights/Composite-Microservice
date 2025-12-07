from app.models.dto.image_dto import UploadSuccessResponse, ImageUrlResponse
from app.services.image_service import upload_image, get_image_url
from fastapi import APIRouter, UploadFile, File, HTTPException

image_router = APIRouter(
    tags=["Image"],
)

@image_router.post("/image/upload")
async def upload_image_endpoint(file: UploadFile = File(...)):
    return await upload_image(file)

@image_router.get("/image/{filename}")
async def get_image_url_endpoint(filename: str):
    return await get_image_url(filename)