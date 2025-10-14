from abc import ABC, abstractmethod


# Проверка понимания инъекции зависимостей, декомпозиции, расширяемости.
# Паттерн: Factory, Strategy, Plugin.

# Архитектура легко расширяема.
# Подходит для систем, требующих подключения внешних модулей.
# Применяется в крупных фреймворках.


class Plugin(ABC):
    @abstractmethod
    def execute(self):
        pass


class EmailPlugin(Plugin):
    def execute(self):
        return "Sending email..."


class SMSPlugin(Plugin):
    def execute(self):
        return "Sending SMS..."


class NotificationSystem:
    def __init__(self):
        self.plugins = {}

    def register(self, name: str, plugin: Plugin):
        self.plugins[name] = plugin

    def notify(self, name: str):
        if name in self.plugins:
            return self.plugins[name].execute()
        raise ValueError(f"Plugin {name} not found")


# Использование
ns = NotificationSystem()
ns.register("email", EmailPlugin())
ns.register("sms", SMSPlugin())
print(ns.notify("email"))
