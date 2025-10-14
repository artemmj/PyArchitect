from abc import ABC, abstractmethod
import asyncio


# Понимание паттерна "Исполнитель" (Executor) или Strategy.
# Возможность выполнения задач в разных средах.
# Обработка ошибок, логирование, асинхронность.

# Поддержка разных способов выполнения задач.
# Можно легко добавлять новые исполнители (например, через Celery, HTTP API и т.д.).
# Подходит для систем с разными уровнями сложности и нагрузкой.


class TaskExecutor(ABC):
    @abstractmethod
    def execute(self, task_func, *args, **kwargs):
        pass


class LocalExecutor(TaskExecutor):
    def execute(self, task_func, *args, **kwargs):
        return task_func(*args, **kwargs)


class AsyncExecutor(TaskExecutor):
    async def execute(self, task_func, *args, **kwargs):
        if asyncio.iscoroutinefunction(task_func):
            return await task_func(*args, **kwargs)
        else:
            return task_func(*args, **kwargs)


def sample_task(x, y):
    return x + y


# Использование
executor = LocalExecutor()
result = executor.execute(sample_task, 5, 3)
print(result)  # 8
