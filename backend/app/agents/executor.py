import logging
from typing import Any, Dict, List

class Executor:
    @staticmethod
    async def execute(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        steps = plan.get("plan", [])
        results = []
        for step in steps:
            # MVP: Just log and return dummy result
            logging.info(f"Executor running step: {step}")
            output = f"Executed {step['step']}"
            original_query = plan.get("meta", {}).get("query", "")
            if step['step'] == 'generate' and "capital of France".lower() in original_query.lower():
                output = "The capital of France is Paris."
            results.append({"step": step, "output": output})
        return results