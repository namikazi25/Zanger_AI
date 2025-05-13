import pytest
import asyncio
from unittest.mock import patch, MagicMock, mock_open
from fastapi import UploadFile
import io

# Adjust the import path based on your project structure
from backend.app.utils.preprocessing import preprocess_files, detect_mime_type, preprocess_image, preprocess_document, ALLOWED_MIME_TYPES

# Helper to create mock UploadFile
def create_mock_upload_file(filename: str, content_bytes: bytes, content_type: str) -> UploadFile:
    file_like_object = io.BytesIO(content_bytes)
    # Pass content_type via headers as per recent FastAPI versions
    upload_file = UploadFile(filename=filename, file=file_like_object, headers={"content-type": content_type})
    return upload_file

@pytest.mark.asyncio
async def test_preprocess_files_no_files():
    result = await preprocess_files([])
    assert result == []

@pytest.mark.asyncio
@patch('backend.app.utils.preprocessing.detect_mime_type')
@patch('backend.app.utils.preprocessing.preprocess_image')
async def test_preprocess_files_with_image(mock_preprocess_image, mock_detect_mime_type):
    mock_detect_mime_type.return_value = "image/png"
    mock_preprocess_image.return_value = "Processed image text"
    
    mock_file_content = b"dummy png data"
    mock_file = create_mock_upload_file("test.png", mock_file_content, "image/png")
    
    result = await preprocess_files([mock_file])
    
    mock_detect_mime_type.assert_called_once_with(mock_file_content)
    mock_preprocess_image.assert_called_once_with(mock_file_content)
    assert len(result) == 1
    assert result[0]["filename"] == "test.png"
    assert result[0]["mime_type"] == "image/png"
    assert result[0]["content"] == "Processed image text"

@pytest.mark.asyncio
@patch('backend.app.utils.preprocessing.detect_mime_type')
@patch('backend.app.utils.preprocessing.preprocess_document')
async def test_preprocess_files_with_docx(mock_preprocess_document, mock_detect_mime_type):
    mock_detect_mime_type.return_value = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    mock_preprocess_document.return_value = "Processed docx text"
    
    mock_file_content = b"dummy docx data"
    mock_file = create_mock_upload_file("test.docx", mock_file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    result = await preprocess_files([mock_file])
    
    mock_detect_mime_type.assert_called_once_with(mock_file_content)
    mock_preprocess_document.assert_called_once_with(mock_file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert len(result) == 1
    assert result[0]["filename"] == "test.docx"
    assert result[0]["mime_type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert result[0]["content"] == "Processed docx text"

@pytest.mark.asyncio
@patch('backend.app.utils.preprocessing.detect_mime_type')
async def test_preprocess_files_unsupported_type(mock_detect_mime_type):
    mock_detect_mime_type.return_value = "application/zip"
    
    mock_file_content = b"dummy zip data"
    mock_file = create_mock_upload_file("test.zip", mock_file_content, "application/zip")
    
    result = await preprocess_files([mock_file])
    
    mock_detect_mime_type.assert_called_once_with(mock_file_content)
    assert len(result) == 1
    assert result[0]["filename"] == "test.zip"
    assert result[0]["mime_type"] == "application/zip"
    assert result[0]["content"] == "Unsupported file type: application/zip"

@pytest.mark.asyncio
@patch('backend.app.utils.preprocessing.detect_mime_type')
@patch('backend.app.utils.preprocessing.preprocess_image')
@patch('backend.app.utils.preprocessing.preprocess_document')
async def test_preprocess_files_multiple_mixed_types(mock_preprocess_document, mock_preprocess_image, mock_detect_mime_type):
    def side_effect_detect_mime(file_bytes):
        if file_bytes == b"dummy png data":
            return "image/png"
        if file_bytes == b"dummy docx data":
            return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        if file_bytes == b"dummy zip data":
            return "application/zip"
        return None
    mock_detect_mime_type.side_effect = side_effect_detect_mime
    mock_preprocess_image.return_value = "Processed image text"
    mock_preprocess_document.return_value = "Processed docx text"

    png_content = b"dummy png data"
    docx_content = b"dummy docx data"
    zip_content = b"dummy zip data"

    file_png = create_mock_upload_file("image.png", png_content, "image/png")
    file_docx = create_mock_upload_file("document.docx", docx_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    file_zip = create_mock_upload_file("archive.zip", zip_content, "application/zip")

    files_to_process = [file_png, file_docx, file_zip]
    result = await preprocess_files(files_to_process)

    assert mock_detect_mime_type.call_count == 3
    mock_preprocess_image.assert_called_once_with(png_content)
    mock_preprocess_document.assert_called_once_with(docx_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    assert len(result) == 3
    assert result[0]["filename"] == "image.png"
    assert result[0]["content"] == "Processed image text"
    assert result[1]["filename"] == "document.docx"
    assert result[1]["content"] == "Processed docx text"
    assert result[2]["filename"] == "archive.zip"
    assert result[2]["content"] == "Unsupported file type: application/zip"

# Tests for individual helper functions

@patch('magic.Magic')
def test_detect_mime_type(MockMagic):
    mock_magic_instance = MockMagic.return_value
    mock_magic_instance.from_buffer.return_value = "image/jpeg"
    
    mime_type = detect_mime_type(b"dummy_bytes")
    
    MockMagic.assert_called_once_with(mime=True)
    mock_magic_instance.from_buffer.assert_called_once_with(b"dummy_bytes")
    assert mime_type == "image/jpeg"

@patch('backend.app.utils.preprocessing.Image.open')
def test_preprocess_image_success(MockImageOpen):
    mock_image_instance = MagicMock()
    mock_image_instance.size = (100, 200)
    MockImageOpen.return_value = mock_image_instance
    
    result = preprocess_image(b"dummy_image_bytes")
    
    MockImageOpen.assert_called_once()
    # Check that the first argument to the call is an io.BytesIO object
    # and that its content is the expected bytes.
    args, _ = MockImageOpen.call_args
    assert isinstance(args[0], io.BytesIO)
    assert args[0].getvalue() == b"dummy_image_bytes"
    assert result == "Image detected with dimensions: 100x200"

@patch('backend.app.utils.preprocessing.Image.open', side_effect=Exception("PIL error"))
def test_preprocess_image_error(MockImageOpen):
    result = preprocess_image(b"bad_image_bytes")
    assert "Error processing image: PIL error" in result

@patch('mammoth.extract_raw_text')
def test_preprocess_document_docx_success(mock_extract_raw_text):
    mock_mammoth_result = MagicMock()
    mock_mammoth_result.value = "Extracted text from docx"
    mock_extract_raw_text.return_value = mock_mammoth_result
    
    result = preprocess_document(b"dummy_docx_bytes", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    mock_extract_raw_text.assert_called_once()
    # Check the content of the BytesIO object passed to the mock
    called_arg = mock_extract_raw_text.call_args[0][0]
    assert isinstance(called_arg, io.BytesIO)
    assert called_arg.read() == b"dummy_docx_bytes"
    assert result == "Extracted text from docx"

@patch('mammoth.extract_raw_text', side_effect=Exception("Mammoth error"))
def test_preprocess_document_docx_error(mock_extract_raw_text):
    result = preprocess_document(b"bad_docx_bytes", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert "Error processing document: Mammoth error" in result

def test_preprocess_document_unsupported_type():
    result = preprocess_document(b"dummy_doc_bytes", "application/msword") # .doc is in ALLOWED_MIME_TYPES but not handled by mammoth in this func
    assert result == "Unsupported document type for direct text extraction."