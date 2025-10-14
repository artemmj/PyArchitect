from abc import ABC, abstractmethod
from typing import List


# Понимание, как обойти ACID в распределённой системе.
# Паттерны: Choreography и Orchestration.
# Умение откатить транзакцию, если один из шагов не удался.

# Управление сложными транзакциями в распределённой системе.
# Паттерн Saga помогает избежать распределённых транзакций.
# Подходит для систем с высокой надёжностью.


class SagaStep(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def compensate(self):
        pass


class ReserveInventoryStep(SagaStep):
    def execute(self):
        print("Reserving inventory...")
        # Здесь была бы логика бронирования
        return True

    def compensate(self):
        print("Releasing inventory...")


class ChargePaymentStep(SagaStep):
    def execute(self):
        print("Charging payment...")
        # Здесь была бы логика оплаты
        return True

    def compensate(self):
        print("Refunding payment...")


class OrderSaga:
    def __init__(self, steps: List[SagaStep]):
        self.steps = steps
        self.executed_steps = []

    def execute(self):
        for step in self.steps:
            try:
                step.execute()
                self.executed_steps.append(step)
            except Exception as e:
                print(f"Error in step {step}, compensating...")
                self.compensate()
                return False
        return True

    def compensate(self):
        for step in reversed(self.executed_steps):
            step.compensate()


# Использование
saga = OrderSaga([
    ReserveInventoryStep(),
    ChargePaymentStep(),
])

success = saga.execute()
print("Order succeeded:", success)
