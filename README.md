## Run Project
Run core module
```
uv run -m src.core_module
```
Run tests
```
uv run -m tests.xxx
```

## Project Structure

```
.
├── cache/                                 # Runtime cache directory
│   ├── mcp/
│   │   ├── mcp_conversation.json          # Saved conversation logs for MCP
│   │   └── prompt.md                     # Cached prompt text
│   └── token/
│       └── aliyun_token.json              # Cached Aliyun token with expiration
│
├── core_module/                           # Core backend code
│   ├── agent/
│   │   ├── agent_prompts/
│   │   │   ├── chatter_logic.py           # System prompt logic for chatter agents
│   │   │   └── mcp_logic.py               # System prompt logic for MCP agents
│   │   ├── agent_types/
│   │   │   ├── agent_chatter.py           # Chatter agent implementation
│   │   │   ├── agent_mcp_handler.py       # MCP agent implementation
│   │   │   └── mcp_conversation.json      # MCP conversation data for testing/dev
│   │   ├── agent_factory.py               # Factory for agent creation
│   │   ├── agent_interface.py             # Abstract base for agents
│   │   ├── prompt.txt                     # Generated prompt output (temp)
│   │   └── prompt_forger.py               # Prompt generation and extraction helpers
│   │
│   ├── asr/
│   │   ├── asr_adapter_nls.py             # Adapter for Aliyun NLS ASR
│   │   ├── asr_factory.py                 # ASR factory
│   │   ├── asr_interface.py               # Abstract ASR interface
│   │   └── __init__.py
│   │
│   ├── link_session/
│   │   ├── LinkSession.py                 # WebSocket link session manager
│   │   ├── LS_Rule.md                     # Documentation for link session logic
│   │   └── __init__.py
│   │
│   ├── llm/
│   │   ├── llm_adapter_deepseek.py        # LLM adapter for DeepSeek
│   │   ├── llm_adapter_qfan.py            # LLM adapter for Qfan
│   │   ├── llm_adapter_volcengine.py      # LLM adapter for Volcengine
│   │   ├── llm_factory.py                 # LLM factory
│   │   ├── llm_interface.py               # Abstract LLM interface
│   │   └── __init__.py
│   │
│   ├── mcp/
│   │   ├── mcp_handler.py                 # MCP tool handler logic
│   │   └── mcp_manager.py                 # MCP session manager
│   │
│   ├── tts/
│   │   ├── tts_adapter_nls.py             # Adapter for Aliyun NLS TTS
│   │   ├── tts_factory.py                 # TTS factory
│   │   ├── tts_interface.py               # Abstract TTS interface
│   │   └── __init__.py
│   │
│   ├── util/
│   │   ├── service_helper/
│   │   │   └── aliyun_token_manager.py    # Token management for Aliyun
│   │   ├── cache_manager.py               # CacheManager for managing cached data
│   │   ├── config_librarian.py            # ConfigLibrarian for loading configs
│   │   └── ffmpeg_helper.py               # Audio processing utilities with FFmpeg
│   │
│   ├── router_http.py                     # FastAPI HTTP routes
│   ├── __init__.py
│   └── __main__.py                        # Application entry point
│
├── tests/                                 # Test directory
│   ├── abc.py                             # Misc test file
│   ├── agent_test.py                      # Tests for agent logic
│   ├── ai_interface_test.py               # Tests for LLM interface
│   ├── mcp_test.py                        # Tests for MCP logic
│   ├── ws_test.py                         # Tests for WebSocket communication
│   └── __init__.py
│
├── tool_script/                           # Developer helper scripts
│   ├── asr_hands_free.py                  # ASR script without extra dependencies
│   ├── mcp_simple.py                      # Simple MCP testing script
│   ├── show-tree.ps1                      # PowerShell tree visualization script
│   ├── ws_audio_input_SR.py               # WebSocket audio input handler
│   ├── ws_control_basic.py                # Basic WebSocket control
│   ├── ws_control_msg.py                  # WebSocket messaging control
│   └── ws_display.py                      # WebSocket display script
│
├── .gitignore                             # Ignore cache, .venv, audio, etc.
├── .python-version                        # Python version specifier
├── aud.wav                                # Example or temporary audio file
├── conf.yaml                              # General configuration
├── output_audio.wav                       # Temporary generated audio output
├── personal_conf.yaml                     # Personal sensitive configuration
├── pyproject.toml                         # Project configuration and dependencies
├── README.md                              # Documentation
├── StartServer_Win.bat                    # Windows start server script
└── uv.lock                                # Lockfile for uv environment

```