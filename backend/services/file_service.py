# Import OS
import os

# Import UUID
import uuid

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def save_uploaded_file(file):
    """
    Save uploaded file.
    """

    # Generate unique filename
    unique_name = (
        f"{uuid.uuid4()}_{file.filename}"
    )

    # Build path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )

    with open(file_path,"wb") as buffer:
        
        buffer.write(
            file.file.read()
        )

    return file_path