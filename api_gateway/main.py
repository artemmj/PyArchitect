import asyncio
import aiohttp
from typing import List


# Понимание роли API Gateway в микросервисной архитектуре.
# Маршрутизация, балансировка, аутентификация, логирование.
# Использование aiohttp, asyncio, proxy.

# Простая реализация API Gateway с балансировкой.
# Подходит для начального понимания архитектуры микросервисов.
# Можно расширить: аутентификация, кеширование, мониторинг.


class ServiceRegistry:
    def __init__(self):
        self.services = {}

    def register(self, name: str, urls: List[str]):
        self.services[name] = urls

    def get_url(self, name: str) -> str:
        urls = self.services.get(name)
        if urls:
            # Простой round-robin
            return urls.pop(0)
        raise ValueError(f"No available instance for service: {name}")


class APIGateway:
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    async def handle_request(self, service_name: str, path: str, method: str = "GET", data: dict = None):
        url = self.registry.get_url(service_name)
        full_url = f"{url}{path}"

        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(full_url) as resp:
                    return await resp.json()
            elif method == "POST":
                async with session.post(full_url, json=data) as resp:
                    return await resp.json()


# Использование
registry = ServiceRegistry()
registry.register("user_service", ["http://user1:8000", "http://user2:8000"])
gateway = APIGateway(registry)


async def main():
    result = await gateway.handle_request("user_service", "/users/1", "GET")
    print(result)


asyncio.run(main())
