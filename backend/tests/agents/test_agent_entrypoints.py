"""
This test ensures that the agent entrypoint files in the source directory match the expected architecture.
The purpose is to enforce repository cleanliness and prevent obsolete agent files from remaining in the codebase.
By maintaining this constraint, we help ensure a clear and maintainable project structure as the backend evolves.
This test is part of a test-driven approach to repository cleanup and ongoing codebase hygiene.
"""
import os
import pytest

def test_agent_entrypoints_exist():
    agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/agents'))
    files = [f for f in os.listdir(agents_dir) if f.endswith('.py') and not f.startswith('__') and not f.startswith('test_')]
    expected_files = sorted(['my_agent.py', 'planner.py', 'executor.py', 'evaluator.py'])
    assert sorted(files) == expected_files, f"Expected agent files: {expected_files}, found: {files}"