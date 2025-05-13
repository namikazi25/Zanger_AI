import logging
from .planner import Planner
from .executor import Executor
from .evaluator import Evaluator
from ..utils.preprocessing import preprocess_files # Added import
from typing import List, Optional, Any # Added for type hinting
from fastapi import UploadFile # Added for type hinting
import asyncio

async def run_agent(query: str, session: Any, files: Optional[List[UploadFile]] = None): # Modified signature
    logging.info(f"Agent received query: {query} with session: {session}, files: {files is not None and len(files) > 0}")
    
    processed_file_contents = []
    if files:
        processed_file_contents = await preprocess_files(files)
        # logging.info(f"Processed file contents: {processed_file_contents}")
        # You might want to combine query and processed_file_contents before sending to Planner
        # For now, let's assume Planner can handle them separately or they are passed in session/context

    # Modify the query or session to include processed_file_contents as needed by your Planner
    # Example: query_with_context = query
    # if processed_file_contents:
    #     file_texts = "\n".join([f"File {idx+1} ({item['filename']}):\n{item['content']}" for idx, item in enumerate(processed_file_contents)])
    #     query_with_context = f"{query}\n\nAttached Files Content:\n{file_texts}"

    # For now, we'll pass the original query and let the planner decide how to use file content if available via session or other means.
    # The planner might need to be updated to be aware of `processed_file_contents`.
    plan = await Planner.plan(query, session, processed_file_contents) # Pass processed_file_contents to Planner
    logging.info(f"Agent plan: {plan}")
    results = await Executor.execute(plan)
    logging.info(f"Agent execution results: {results}")
    final = await Evaluator.evaluate(results)
    logging.info(f"Agent final evaluation: {final}")
    return final

# Example usage for testing (remove in production)
if __name__ == "__main__":
    import asyncio
    query = "What is the statute of limitations for contract disputes in California?"
    session = {"session_id": "test123"}
    # Example with a dummy file (requires a running FastAPI app to test UploadFile properly)
    # For standalone testing, you might mock UploadFile or adapt this example.
    # from fastapi import UploadFile
    # import io
    # dummy_file_content = b"This is a test docx content."
    # dummy_file = UploadFile(filename="test.docx", file=io.BytesIO(dummy_file_content), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    # result = asyncio.run(run_agent(query, session, files=[dummy_file]))
    result = asyncio.run(run_agent(query, session)) # Original call for non-file testing
    print(result)

def main():
    pass