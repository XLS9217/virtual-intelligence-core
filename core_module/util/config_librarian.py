import os
import yaml

class ConfigLibrarian:
    _config = {}

    @classmethod
    def load_config(cls, path="personal_conf.yaml"):
        if cls._config:
            return  # Already loaded, skip reloading

        print(os.getcwd())
        if not os.path.exists(path):
            print(f"[ConfigLibrarian] Config file not found at '{path}'.")
            print("Please create a personal_conf.yaml config file at the expected location.")
            return

        with open(path, "r") as f:
            cls._config = yaml.safe_load(f)

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