# Run Project

You can run by the guide <code> uv run -m cli </code>

Run core module <code> uv run -m src.core_module </code>
Run tests and tools <code> uv run -m src.tests/tools.specific_tests/tools </code>



# Project Structure

## ./cache
Runtime cache managed by src\core_module\util\cache_manager.py

## ./src
The source folder

### ./src/cases
The custom case scripts that sets up cases like adding a specific agent to a link session

### ./src/core_module
The core module that starts the server

### ./src/tools
Run tools <code> uv run -m src.tools.xxx </code>

### ./src/tests
Run tests <code> uv run -m src.tests.xxx </code>
