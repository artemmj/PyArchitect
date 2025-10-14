from abc import ABC, abstractmethod
from datetime import datetime


# Принцип Open/Closed.
# Паттерн Strategy или Adapter.
# Логика аудита: кто, что, когда, где — часто используется в корпоративных приложениях.

# Простая замена способа логирования.
# Подходит для систем, где требуется аудит.
# Легко расширяется новыми способами хранения логов.


class AuditLogger(ABC):
    @abstractmethod
    def log(self, user: str, action: str, resource: str):
        pass


class FileAuditLogger(AuditLogger):
    def log(self, user: str, action: str, resource: str):
        with open("audit.log", "a") as f:
            f.write(f"[{datetime.now()}] {user} {action} {resource}\n")


class DatabaseAuditLogger(AuditLogger):
    def log(self, user: str, action: str, resource: str):
        # Здесь был бы код для записи в БД
        print(f"DB: {user} {action} {resource}")


class AuditService:
    def __init__(self, logger: AuditLogger):
        self.logger = logger

    def record(self, user: str, action: str, resource: str):
        self.logger.log(user, action, resource)


# Использование
service = AuditService(FileAuditLogger())
service.record("admin", "created", "user123")
