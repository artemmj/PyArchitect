from abc import ABC, abstractmethod
from collections import OrderedDict
import time


# Понимание паттерна "Стратегия".
# Знание структур данных (например, OrderedDict для LRU).
# Умение проектировать масштабируемые и производительные компоненты.

# Архитектура позволяет легко переключаться между стратегиями кеширования.
# Подходит для высоконагруженных систем.
# Используется паттерн "Стратегия".


class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def put(self, key: str, value):
        pass


class LRUCache(CacheStrategy):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key: str, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value


class TTLCache(CacheStrategy):
    def __init__(self, ttl: int):  # время в секундах
        self.ttl = ttl
        self.cache = {}

    def get(self, key: str):
        item = self.cache.get(key)
        if item:
            value, timestamp = item
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None

    def put(self, key: str, value):
        self.cache[key] = (value, time.time())


class CacheManager:
    def __init__(self, strategy: CacheStrategy):
        self.strategy = strategy

    def get(self, key: str):
        return self.strategy.get(key)

    def put(self, key: str, value):
        self.strategy.put(key, value)


# Использование
cache = CacheManager(LRUCache(2))
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))  # 1
cache.put("c", 3)  # "b" вытесняется
print(cache.get("b"))  # None
