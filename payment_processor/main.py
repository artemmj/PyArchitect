from abc import ABC, abstractmethod


# Понимание паттерна Strategy или Adapter.
# Принцип Open/Closed (OCP): система должна быть открыта для расширения, закрыта для модификации.
# Возможность интеграции с внешними API.
# Обработка ошибок, логирование, безопасность.

# Код легко расширяется: можно добавлять новые провайдеры без изменения основной логики.
# Применён паттерн Strategy.
# Подходит для систем с интеграцией с внешними API.


class PaymentProvider(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str) -> dict:
        pass


class StripeProvider(PaymentProvider):
    def process_payment(self, amount: float, currency: str) -> dict:
        # Здесь была бы интеграция с API Stripe
        return {"status": "success", "provider": "stripe", "amount": amount, "currency": currency}


class PayPalProvider(PaymentProvider):
    def process_payment(self, amount: float, currency: str) -> dict:
        # Здесь была бы интеграция с API PayPal
        return {"status": "success", "provider": "paypal", "amount": amount, "currency": currency}


class PaymentProcessor:
    def __init__(self, provider: PaymentProvider):
        self.provider = provider

    def process(self, amount: float, currency: str) -> dict:
        try:
            result = self.provider.process_payment(amount, currency)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Использование
processor = PaymentProcessor(StripeProvider())
result = processor.process(100.0, "USD")
print(result)
