import logging
from .planner import Planner
from .executor import Executor
from .evaluator import Evaluator
import asyncio

async def run_agent(query, session):
    logging.info(f"Agent received query: {query} with session: {session}")
    plan = await Planner.plan(query, session)
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
    result = asyncio.run(run_agent(query, session))
    print(result)

def main():
    pass