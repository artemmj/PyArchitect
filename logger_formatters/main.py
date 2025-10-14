from abc import ABC, abstractmethod


# Принцип Single Responsibility (SRP): разные классы для форматирования, вывода и логики логирования.
# Паттерн Strategy или Observer для разных обработчиков логов.
# Гибкость и расширяемость архитектуры.

# Код легко расширяем: можно добавить новые форматы и обработчики.
# Соблюдены принципы SOLID: SRP, OCP.
# Подходит для систем с высокой гибкостью.


class LogFormatter(ABC):
    @abstractmethod
    def format(self, message: str) -> str:
        pass


class PlainTextFormatter(LogFormatter):
    def format(self, message: str) -> str:
        return f"[LOG] {message}"


class JSONFormatter(LogFormatter):
    def format(self, message: str) -> str:
        import json
        return json.dumps({"level": "INFO", "message": message})
    

class LogHandler(ABC):
    def __init__(self, formatter: LogFormatter):
        self.formatter = formatter

    @abstractmethod
    def handle(self, message: str):
        pass


class ConsoleHandler(LogHandler):
    def handle(self, message: str):
        print(self.formatter.format(message))


class FileHandler(LogHandler):
    def __init__(self, formatter: LogFormatter, filename: str):
        super().__init__(formatter)
        self.filename = filename

    def handle(self, message: str):
        with open(self.filename, "a") as f:
            f.write(self.formatter.format(message) + "\n")


class Logger:
    def __init__(self, handlers):
        self.handlers = handlers

    def log(self, message: str):
        for handler in self.handlers:
            handler.handle(message)


# Использование
logger = Logger([
    ConsoleHandler(PlainTextFormatter()),
    FileHandler(JSONFormatter(), "app.log")
])
logger.log("Test message")
