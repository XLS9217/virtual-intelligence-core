import os
import json

from src.core_module.util.config_librarian import ConfigLibrarian

class CacheManager:

    @staticmethod
    def _get_cache_file_path(cache_type: str, file_name: str) -> str:
        cache_dir = ConfigLibrarian.get_cache_dir(cache_type)
        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, file_name)

    @staticmethod
    def save_cache(cache_type: str, file_name: str, data):
        file_path = CacheManager._get_cache_file_path(cache_type, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            if isinstance(data, dict) or isinstance(data, list):
                json_str = json.dumps(data, ensure_ascii=False, indent=4)
                f.write(json_str)
            else:
                f.write(str(data))

    @staticmethod
    def read_cache(cache_type: str, file_name: str) -> str | None:
        file_path = CacheManager._get_cache_file_path(cache_type, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
