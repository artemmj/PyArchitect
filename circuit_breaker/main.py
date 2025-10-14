import time
from enum import Enum
from typing import Callable


# Понимание, зачем нужен Circuit Breaker.
# Как предотвращать падение системы при отказе внешнего сервиса.
# Состояния: Closed, Open, Half-Open.

# Защищает систему от каскадных отказов.
# Подходит для микросервисов, внешних API.
# Улучшает надёжность и устойчивость системы.


class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half-open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = State.CLOSED

    def call(self, func: Callable, *args, **kwargs):
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = State.HALF_OPEN
            else:
                raise Exception("Circuit is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        self.failure_count = 0
        self.state = State.CLOSED

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = State.OPEN


# Использование
def unreliable_service():
    import random
    if random.random() < 0.8:
        raise Exception("Service failed")
    return "Success"


breaker = CircuitBreaker(failure_threshold=3, timeout=10)

for i in range(10):
    try:
        result = breaker.call(unreliable_service)
        print(f"Attempt {i}: {result}")
    except Exception as e:
        print(f"Attempt {i}: {e}")
    time.sleep(1)
