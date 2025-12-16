import os
from datetime import timedelta
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import Annotated, Tuple
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
from app.models.dto.image_dto import UploadSuccessResponse, ImageUrlResponse
import uuid
from PIL import Image
from io import BytesIO
load_dotenv()
import logging
logger = logging.getLogger("composite_api")
app = FastAPI()


BUCKET_NAME = os.getenv("IMAGE_BUCKET_NAME")  
CREDENTIALS_FILE = os.getenv("GCS_IMAGE_KEY_FILE")




if CREDENTIALS_FILE and os.path.exists(CREDENTIALS_FILE):
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    storage_client = storage.Client(credentials=credentials)
else:
    raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")

async def get_bucket():
    return storage_client.bucket(BUCKET_NAME)


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


async def compress_image(image_data: bytes, max_size: int = MAX_FILE_SIZE) -> Tuple[bytes, str]:
    """
    Compress image to be under max_size (5MB by default).
    Returns compressed image data and content type.
    """
    try:
        # Open image from bytes
        image = Image.open(BytesIO(image_data))
        
        # Get original format
        original_format = image.format or 'JPEG'
        
        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
            output_format = 'JPEG'
            content_type = 'image/jpeg'
        else:
            output_format = original_format
            content_type = f'image/{original_format.lower()}'
        
        # Start with high quality and reduce if needed
        quality = 85
        scale_factor = 1.0
        
        while True:
            # Apply scaling if needed
            if scale_factor < 1.0:
                new_size = (int(image.size[0] * scale_factor), int(image.size[1] * scale_factor))
                resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            else:
                resized_image = image
            
            # Save to bytes with current quality
            output = BytesIO()
            
            if output_format == 'JPEG':
                resized_image.save(output, format='JPEG', quality=quality, optimize=True)
            elif output_format == 'PNG':
                # PNG compression level (0-9, higher = more compression)
                png_compress_level = min(9, int((100 - quality) / 10))
                resized_image.save(output, format='PNG', compress_level=png_compress_level, optimize=True)
            else:
                # For other formats, try to save with optimization
                resized_image.save(output, format=output_format, optimize=True)
            
            compressed_data = output.getvalue()
            compressed_size = len(compressed_data)
            
            # If size is acceptable, return
            if compressed_size <= max_size:
                return compressed_data, content_type
            
            # If still too large, reduce quality or scale
            if quality > 30:
                quality -= 10
            elif scale_factor > 0.5:
                scale_factor -= 0.1
            else:
                # Last resort: force JPEG with low quality
                if output_format != 'JPEG':
                    output_format = 'JPEG'
                    content_type = 'image/jpeg'
                    if resized_image.mode != 'RGB':
                        resized_image = resized_image.convert('RGB')
                quality = max(20, quality - 5)
                if quality <= 20 and compressed_size > max_size:
                    # If still too large, reduce dimensions more aggressively
                    scale_factor = 0.5
                    new_size = (int(image.size[0] * scale_factor), int(image.size[1] * scale_factor))
                    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
                    quality = 30
        
    except Exception as e:
        # If compression fails, return original data
        logger.error(f"Image compression error: {e}")
        return image_data, 'image/jpeg'


async def upload_image(file: UploadFile = File(...)):
    """
    upload image to GCS, compressing to 5MB if necessary
    """
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Compress if file is larger than 5MB
        if file_size > MAX_FILE_SIZE:
            compressed_content, content_type = await compress_image(file_content, MAX_FILE_SIZE)
            file_content = compressed_content
            logger.info(f"Image compressed from {file_size / 1024 / 1024:.2f}MB to {len(file_content) / 1024 / 1024:.2f}MB")
        else:
            content_type = file.content_type or 'image/jpeg'
        
        bucket = await get_bucket()
        # create blob object (file object in GCS)
        # use uuid to rename file, prevent file name conflict overwrite
        file_extension = str(file.filename).split('.')[-1] if '.' in str(file.filename) else 'jpg'
        file_name = f"{uuid.uuid4()}_{str(file.filename).split('.')[0]}.{file_extension}"
        blob = bucket.blob(file_name)
        
        # upload compressed file from memory to GCS
        blob.upload_from_string(file_content, content_type=content_type)

        return UploadSuccessResponse(
            status="success",
            filename=file_name,
            message="file uploaded successfully"
        )
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="file upload failed")


async def get_image_url(filename: str):
    """
    get image url from GCS
    the frontend can use this url to display the image
    """
    try:
        bucket = await get_bucket()
        blob = bucket.blob(filename)
        
        if not blob.exists():
            raise HTTPException(status_code=404, detail="image not found")
            
        # generate signed url with very long expiration (effectively no time limit)
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=3650),  # 10 years - effectively no expiration
            method="GET"
        )
        
        return ImageUrlResponse(url=signed_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get image url failed: {str(e)}")

