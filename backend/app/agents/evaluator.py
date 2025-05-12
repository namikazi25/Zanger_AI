import logging
from typing import Any, List

class Evaluator:
    @staticmethod
    async def evaluate(results: List[Any]) -> Any:
        # MVP: Log and pass through
        logging.info(f"Evaluator received results: {results}")
        return {"response": results[-1]["output"] if results else None, "all_results": results}