import logging
from typing import Any, Dict

class Planner:
    @staticmethod
    async def plan(query: str, session: Dict[str, Any]) -> Dict[str, Any]:
        # MVP: Always plan to search, then generate
        plan = [
            {"step": "search", "query": query},
            {"step": "generate", "input": "search_context + user_query"}
        ]
        logging.info(f"Planner generated plan: {plan}")
        return {"plan": plan, "meta": {"query": query, "session": session}}