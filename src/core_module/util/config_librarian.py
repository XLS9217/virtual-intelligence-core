import os
import yaml

class ConfigLibrarian:
    _config = {}
    
    @classmethod
    def get_cache_dir(cls, sub_dir: str = "") -> str:
        base = os.path.join(os.getcwd(), cls._config["system_config"]["cache_dir"])
        if sub_dir == "token":
            return os.path.join(base, cls._config["system_config"]["token_cache_dir"])
        elif sub_dir == "mcp":
            return os.path.join(base, cls._config["system_config"]["mcp_cache_dir"])
        return base

    @classmethod
    def load_config(cls, path="personal_conf.yaml"):
        if cls._config:
            return  # Already loaded, skip reloading

        print("[ConfigLibrarian] running at " + os.getcwd())
        if not os.path.exists(path):
            print(f"[ConfigLibrarian] Config file not found at '{path}'.")
            print(f"Please create a personal_conf.yaml config file at {os.getcwd()}")
            return

        with open(path, "r") as f:
            cls._config = yaml.safe_load(f)

    @classmethod
    def get_service_config(cls , service_name:str):
        return cls._config["service_config"][service_name]

    @classmethod
    def get_system_host(cls):
        return cls._config["system_config"]["host"]

    @classmethod
    def get_system_port(cls):
        return cls._config["system_config"]["port"]

    @classmethod
    def get_default_asr(cls):
        return cls._config["asr_config"]["using"]

    @classmethod
    def get_default_llm(cls):
        return cls._config["llm_config"]["using"]

    @classmethod
    def get_default_tts(cls):
        return cls._config["tts_config"]["using"]

    @classmethod
    def get_asr_provider_info(cls, name):
        return cls._config["asr_config"]["providers"][name]

    @classmethod
    def get_llm_provider_info(cls, name):
        return cls._config["llm_config"]["providers"][name]

    @classmethod
    def get_tts_provider_info(cls, name):
        return cls._config["tts_config"]["providers"][name]


ConfigLibrarian.load_config()