import asyncio
from typing import Callable


# Понимание асинхронности и asyncio.
# Паттерны: Observer, Command, Strategy.
# Обработка ошибок, retry-логика.

# Пул задач ограничивает количество одновременных операций.
# Поддерживает retry с экспоненциальной задержкой.
# Подходит для обработки большого количества запросов.


class TaskPool:
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.results = []

    async def execute_with_retry(self, coro: Callable, retries: int = 3):
        for attempt in range(retries):
            try:
                async with self.semaphore:
                    result = await coro()
                    return result
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                await asyncio.sleep(0.5 * (2 ** attempt))  # экспоненциальная задержка
        return None

    async def add_task(self, coro: Callable):
        result = await self.execute_with_retry(coro)
        self.results.append(result)

    async def run_all(self, coroutines):
        tasks = [self.add_task(coro) for coro in coroutines]
        await asyncio.gather(*tasks, return_exceptions=True)
