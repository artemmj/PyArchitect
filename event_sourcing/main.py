from abc import ABC, abstractmethod
from typing import List


# Понимание, что состояние системы формируется из событий.
# Применение в системах, где история изменений важна (например, банковские транзакции).
# Как восстанавливается состояние из событий.

# Полная история изменений сохраняется.
# Состояние можно восстановить из событий.
# Подходит для систем с аудитом, транзакциями, откатом состояния.


class Event(ABC):
    pass


class AccountCreatedEvent(Event):
    def __init__(self, account_id: str, initial_balance: float):
        self.account_id = account_id
        self.initial_balance = initial_balance


class MoneyDepositedEvent(Event):
    def __init__(self, account_id: str, amount: float):
        self.account_id = account_id
        self.amount = amount


class BankAccount:
    def __init__(self):
        self.account_id = None
        self.balance = 0.0
        self.events: List[Event] = []

    def apply_event(self, event: Event):
        if isinstance(event, AccountCreatedEvent):
            self.account_id = event.account_id
            self.balance = event.initial_balance
        elif isinstance(event, MoneyDepositedEvent):
            self.balance += event.amount
        self.events.append(event)

    def deposit(self, amount: float):
        event = MoneyDepositedEvent(self.account_id, amount)
        self.apply_event(event)

    def replay(self, events: List[Event]):
        self.balance = 0.0
        for event in events:
            self.apply_event(event)


# Использование
account = BankAccount()
account.apply_event(AccountCreatedEvent("123", 100.0))
account.deposit(50.0)
print(account.balance)  # 150.0


# Восстановление состояния из событий
new_account = BankAccount()
new_account.replay(account.events)
print(new_account.balance)  # 150.0
