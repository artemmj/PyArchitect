from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


# Понимание слоёв архитектуры: Domain, Application, Infrastructure, UI.
# Value Object, Entity, Aggregate Root, Repository, Domain Service, Factory.
# Как доменная логика изолирована от инфраструктуры.

# Ясно разделены доменная логика и инфраструктура.
# Подходит для сложных бизнес-областей.
# Легко тестировать и расширять.


# =============== Value Object ===============
@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Currencies must match")
        return Money(self.amount + other.amount, self.currency)


# =============== Entity ===============
@dataclass
class Customer:
    id: int
    name: str


# =============== Aggregate Root ===============
@dataclass
class Order:
    customer: Customer
    total: Money
    status: str = "pending"

    def complete(self):
        if self.status == "pending":
            self.status = "completed"
        else:
            raise ValueError("Order already completed or cancelled")


# =============== Repository (interface) ===============
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        pass


# =============== Concrete Repository ===============
class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = {}

    def save(self, order: Order):
        self.orders[order.customer.id] = order

    def find_by_id(self, order_id: int) -> Optional[Order]:
        return self.orders.get(order_id)


# =============== Application Service ===============
class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, customer: Customer, total: Money):
        order = Order(customer=customer, total=total)
        self.repo.save(order)
        return order


# Использование
repo = InMemoryOrderRepository()
service = OrderService(repo)

customer = Customer(id=1, name="Alice")
order = service.create_order(customer, Money(100.0, "USD"))
print(order)  # Order(customer=Customer(id=1, name='Alice'), total=Money(amount=100.0, currency='USD'), status='pending')
order.complete()
print(order.status)  # completed
