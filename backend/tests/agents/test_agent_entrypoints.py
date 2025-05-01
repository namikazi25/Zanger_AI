"""
This test ensures that only 'my_agent.py' exists as an agent entrypoint in the source directory.
The purpose is to enforce repository cleanliness and prevent obsolete agent files from remaining in the codebase.
By maintaining this constraint, we help ensure a clear and maintainable project structure as the backend evolves.
This test is part of a test-driven approach to repository cleanup and ongoing codebase hygiene.
"""
import os
import pytest

def test_only_my_agent_exists():
    agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app/agents'))
    files = [f for f in os.listdir(agents_dir) if f.endswith('.py') and not f.startswith('__') and not f.startswith('test_')]
    assert files == ['my_agent.py'], f"Expected only 'my_agent.py', found: {files}"