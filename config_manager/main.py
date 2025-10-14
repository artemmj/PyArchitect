from abc import ABC, abstractmethod
import json
import os


# Понимание паттерна Factory или Strategy.
# Умение работать с разными источниками данных.
# Гибкость и масштабируемость.

# Возможность читать конфигурации из разных источников.
# Поддержка приоритетов (первый найденный ключ используется).
# Применён паттерн Strategy.


class BaseConfigSource(ABC):
    @abstractmethod
    def get(self, key: str, default=None):
        pass


class EnvConfigSource(BaseConfigSource):
    def get(self, key: str, default=None):
        return os.getenv(key, default)


class JSONConfigSource(BaseConfigSource):
    def __init__(self, file_path: str):
        with open(file_path, 'r') as f:
            self.config = json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(key, default)


class ConfigManager:
    def __init__(self, sources: list[BaseConfigSource]):
        self.sources = sources

    def get(self, key: str, default=None):
        for source in self.sources:
            value = source.get(key, default)
            if value is not None:
                return value
        return default


# Использование
config = ConfigManager([
    EnvConfigSource(),
    JSONConfigSource("config.json")
])

print(config.get("DATABASE_URL", "sqlite:///default.db"))
