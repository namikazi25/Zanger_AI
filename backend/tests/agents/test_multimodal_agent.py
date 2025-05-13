import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from fastapi import UploadFile
import io
from typing import List, Dict, Any, Optional

# Adjust the import path based on your project structure
# Assuming 'backend' is a top-level package or accessible in PYTHONPATH
from backend.app.agents.my_agent import run_agent
# If preprocess_files is tested separately or its behavior is complex,
# you might mock it as well. For now, we'll let run_agent call the real one.
# from app.utils.preprocessing import preprocess_files

# Mock data and responses for Planner, Executor, Evaluator
MOCK_PLAN = {"plan": [{"step": "mock_step"}], "meta": {}}
MOCK_EXECUTION_RESULTS = {"results": "mock_execution_data"}
MOCK_EVALUATION = {"final_answer": "mock_final_answer"}

@pytest.fixture
def mock_session() -> Dict[str, Any]:
    return {"session_id": "test_session_123"}

def create_mock_upload_file(filename: str, content: bytes, content_type: str) -> UploadFile:
    # FastAPI's UploadFile is a class, so we instantiate it.
    # It needs 'file' to be a file-like object (e.g., BytesIO)
    # Pass content_type via headers as per recent FastAPI versions
    return UploadFile(filename=filename, file=io.BytesIO(content), headers={"content-type": content_type})

@pytest.mark.asyncio
@patch('backend.app.agents.my_agent.Planner.plan', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Executor.execute', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Evaluator.evaluate', new_callable=AsyncMock)
async def test_run_agent_no_files(
    mock_evaluate: AsyncMock,
    mock_execute: AsyncMock,
    mock_plan: AsyncMock,
    mock_session: Dict[str, Any]
):
    mock_plan.return_value = MOCK_PLAN
    mock_execute.return_value = MOCK_EXECUTION_RESULTS
    mock_evaluate.return_value = MOCK_EVALUATION

    query = "Test query without files"
    result = await run_agent(query, mock_session, files=None)

    mock_plan.assert_called_once_with(query, mock_session, []) # Expect empty list for processed_file_contents
    mock_execute.assert_called_once_with(MOCK_PLAN)
    mock_evaluate.assert_called_once_with(MOCK_EXECUTION_RESULTS)
    assert result == MOCK_EVALUATION

@pytest.mark.asyncio
@patch('backend.app.agents.my_agent.Planner.plan', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Executor.execute', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Evaluator.evaluate', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.preprocess_files', new_callable=AsyncMock) # Mock preprocess_files
async def test_run_agent_with_text_file(
    mock_preprocess: AsyncMock,
    mock_evaluate: AsyncMock,
    mock_execute: AsyncMock,
    mock_plan: AsyncMock,
    mock_session: Dict[str, Any]
):
    mock_plan.return_value = MOCK_PLAN
    mock_execute.return_value = MOCK_EXECUTION_RESULTS
    mock_evaluate.return_value = MOCK_EVALUATION
    
    mock_processed_content = [{"filename": "test.txt", "content": "This is text content.", "type": "text"}]
    mock_preprocess.return_value = mock_processed_content

    query = "Test query with a text file"
    test_file_content = b"This is text content."
    test_file = create_mock_upload_file("test.txt", test_file_content, "text/plain")
    
    result = await run_agent(query, mock_session, files=[test_file])

    mock_preprocess.assert_called_once_with([test_file])
    mock_plan.assert_called_once_with(query, mock_session, mock_processed_content)
    mock_execute.assert_called_once_with(MOCK_PLAN)
    mock_evaluate.assert_called_once_with(MOCK_EXECUTION_RESULTS)
    assert result == MOCK_EVALUATION

@pytest.mark.asyncio
@patch('backend.app.agents.my_agent.Planner.plan', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Executor.execute', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Evaluator.evaluate', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.preprocess_files', new_callable=AsyncMock)
async def test_run_agent_with_image_file(
    mock_preprocess: AsyncMock,
    mock_evaluate: AsyncMock,
    mock_execute: AsyncMock,
    mock_plan: AsyncMock,
    mock_session: Dict[str, Any]
):
    mock_plan.return_value = MOCK_PLAN
    mock_execute.return_value = MOCK_EXECUTION_RESULTS
    mock_evaluate.return_value = MOCK_EVALUATION
    
    mock_processed_content = [{"filename": "image.png", "content": "base64_encoded_image_or_path", "type": "image"}]
    mock_preprocess.return_value = mock_processed_content

    query = "Test query with an image file"
    test_file_content = b"dummy image data" 
    test_file = create_mock_upload_file("image.png", test_file_content, "image/png")
    
    result = await run_agent(query, mock_session, files=[test_file])

    mock_preprocess.assert_called_once_with([test_file])
    mock_plan.assert_called_once_with(query, mock_session, mock_processed_content)
    mock_execute.assert_called_once_with(MOCK_PLAN)
    mock_evaluate.assert_called_once_with(MOCK_EXECUTION_RESULTS)
    assert result == MOCK_EVALUATION

@pytest.mark.asyncio
@patch('backend.app.agents.my_agent.Planner.plan', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Executor.execute', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Evaluator.evaluate', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.preprocess_files', new_callable=AsyncMock)
async def test_run_agent_with_docx_file(
    mock_preprocess: AsyncMock,
    mock_evaluate: AsyncMock,
    mock_execute: AsyncMock,
    mock_plan: AsyncMock,
    mock_session: Dict[str, Any]
):
    mock_plan.return_value = MOCK_PLAN
    mock_execute.return_value = MOCK_EXECUTION_RESULTS
    mock_evaluate.return_value = MOCK_EVALUATION
    
    mock_processed_content = [{"filename": "document.docx", "content": "Extracted docx text.", "type": "document"}]
    mock_preprocess.return_value = mock_processed_content

    query = "Test query with a docx file"
    test_file_content = b"dummy docx data"
    test_file = create_mock_upload_file("document.docx", test_file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    result = await run_agent(query, mock_session, files=[test_file])

    mock_preprocess.assert_called_once_with([test_file])
    mock_plan.assert_called_once_with(query, mock_session, mock_processed_content)
    mock_execute.assert_called_once_with(MOCK_PLAN)
    mock_evaluate.assert_called_once_with(MOCK_EXECUTION_RESULTS)
    assert result == MOCK_EVALUATION

@pytest.mark.asyncio
@patch('backend.app.agents.my_agent.Planner.plan', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Executor.execute', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.Evaluator.evaluate', new_callable=AsyncMock)
@patch('backend.app.agents.my_agent.preprocess_files', new_callable=AsyncMock)
async def test_run_agent_with_multiple_files(
    mock_preprocess: AsyncMock,
    mock_evaluate: AsyncMock,
    mock_execute: AsyncMock,
    mock_plan: AsyncMock,
    mock_session: Dict[str, Any]
):
    mock_plan.return_value = MOCK_PLAN
    mock_execute.return_value = MOCK_EXECUTION_RESULTS
    mock_evaluate.return_value = MOCK_EVALUATION
    
    mock_processed_content = [
        {"filename": "text.txt", "content": "Text data.", "type": "text"},
        {"filename": "image.jpg", "content": "Image data.", "type": "image"}
    ]
    mock_preprocess.return_value = mock_processed_content

    query = "Test query with multiple files"
    file1_content = b"Text data."
    file1 = create_mock_upload_file("text.txt", file1_content, "text/plain")
    
    file2_content = b"Image data."
    file2 = create_mock_upload_file("image.jpg", file2_content, "image/jpeg")
    
    files_list = [file1, file2]
    result = await run_agent(query, mock_session, files=files_list)

    mock_preprocess.assert_called_once_with(files_list)
    mock_plan.assert_called_once_with(query, mock_session, mock_processed_content)
    mock_execute.assert_called_once_with(MOCK_PLAN)
    mock_evaluate.assert_called_once_with(MOCK_EXECUTION_RESULTS)
    assert result == MOCK_EVALUATION