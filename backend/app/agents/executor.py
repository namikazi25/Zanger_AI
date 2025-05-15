import logging
from typing import Any, Dict, List
from ..models.router import get_model

class Executor:
    @staticmethod
    async def execute(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        steps = plan.get("plan", [])
        results = []
        model = None
        for step in steps:
            logging.info(f"Executor running step: {step}")
            output = None
            original_query = plan.get("meta", {}).get("query", "")
            if step["step"] == "generate":
                # Use model router to get the model instance
                if model is None:
                    from ..models.router import get_model
                    model = get_model(plan.get("meta", {}).get("session", {}), policy=None)
                prompt = step.get("input", original_query)
                if hasattr(model, "generate"):
                    if callable(getattr(model, "generate")) and hasattr(model.generate, "__call__"):
                        # Try to detect if generate is async
                        import inspect
                        if inspect.iscoroutinefunction(model.generate):
                            output = await model.generate(prompt)
                        else:
                            output = model.generate(prompt)
                    else:
                        output = "[Error: Model generate attribute is not callable]"
                else:
                    output = "[Error: Model does not support generate()]"
            else:
                output = f"Executed {step['step']}"
            results.append({"step": step, "output": output})
        return results