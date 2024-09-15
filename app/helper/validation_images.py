from fastapi import UploadFile, HTTPException, status

def validation_images(file: UploadFile):
    FILE_SIZE: int = 1024 * 1024 * 1 # Max SIZE 2MB
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only image files are allowed."
        )
        
    real_file_size = 0

    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large"
            )