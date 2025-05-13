import magic
from PIL import Image
import mammoth
import io

ALLOWED_MIME_TYPES = {
    # Images
    "image/jpeg": "image",
    "image/png": "image",
    "image/gif": "image",
    # Documents
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/msword": "doc",
}

def detect_mime_type(file_bytes: bytes) -> str | None:
    """Detects the mime type of a file."""
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file_bytes)
    return mime_type

def preprocess_image(file_bytes: bytes) -> str:
    """Extracts text from an image using a placeholder OCR mechanism."""
    # In a real scenario, you would use an OCR library like Tesseract.
    # For this example, we'll simulate text extraction.
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Placeholder: return image dimensions as a form of 'text'
        return f"Image detected with dimensions: {image.size[0]}x{image.size[1]}"
    except Exception as e:
        return f"Error processing image: {e}"

def preprocess_document(file_bytes: bytes, mime_type: str) -> str:
    """Extracts text from a document (docx)."""
    try:
        if mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            result = mammoth.extract_raw_text(io.BytesIO(file_bytes))
            return result.value
        # Add support for other document types if needed (e.g., .doc, .pdf)
        return "Unsupported document type for direct text extraction."
    except Exception as e:
        return f"Error processing document: {e}"

async def preprocess_files(files: list) -> list:
    """Processes a list of uploaded files, extracting text content."""
    processed_contents = []
    if not files:
        return processed_contents

    for file_upload in files:
        file_bytes = await file_upload.read()
        mime_type = detect_mime_type(file_bytes)
        content = f"Unsupported file type: {mime_type}"

        if mime_type in ALLOWED_MIME_TYPES:
            file_category = ALLOWED_MIME_TYPES[mime_type]
            if file_category == "image":
                content = preprocess_image(file_bytes)
            elif file_category == "docx":
                content = preprocess_document(file_bytes, mime_type)
        
        processed_contents.append({
            "filename": file_upload.filename,
            "mime_type": mime_type,
            "content": content
        })
    return processed_contents