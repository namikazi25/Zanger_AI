import logging
from typing import Any, Dict, List, Optional # Added List, Optional

class Planner:
    @staticmethod
    async def plan(query: str, session: Dict[str, Any], processed_file_contents: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]: # Added processed_file_contents
        # MVP: Always plan to search, then generate
        plan = [
            {"step": "search", "query": query},
            {"step": "generate", "input": query}
        ]
        # TODO: Modify the plan to incorporate processed_file_contents if available.
        # For example, if files are present, the plan might include a step to summarize them
        # or use their content directly in the generation step.
        logging.info(f"Planner received processed_file_contents: {len(processed_file_contents) if processed_file_contents else 0} files")
        logging.info(f"Planner generated plan: {plan}")
        return {"plan": plan, "meta": {"query": query, "session": session, "processed_files_count": len(processed_file_contents) if processed_file_contents else 0}}