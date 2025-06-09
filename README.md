## Run Project
Run core module
```
uv run -m core_module
```
Run tests
```
uv run -m tests.xxx
```

## Project Structure

```
.
├── core_module/               # Core functionality modules
│   ├── agent/                 # Agent management and prompt handling
│   ├── asr/                   # Automatic Speech Recognition adapters
│   ├── link_session/          # WebSocket connection management
│   ├── llm/                   # Large Language Model adapters
│   ├── tts/                   # Text-to-Speech adapters
│   ├── util/                  # Utility functions
│   ├── __init__.py
│   ├── __main__.py
│   └── router_setup.py
├── tests/                     # Unit and integration tests
├── .gitignore
├── .python-version
├── conf.yaml                  # Configuration file
├── pyproject.toml
├── StartServer_Win.bat        # Windows server startup script
├── uv.lock                    # Dependency lock file
└── README.md                  # This file
```