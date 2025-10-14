# Разделение чтения и записи.
# Понимание, зачем нужен CQRS (производительность, масштабируемость, сложные бизнес-операции).
# Использование паттернов: Command, Query, Event.

# Четкое разделение команд и запросов.
# Подходит для систем с высокой нагрузкой на чтение/запись.
# Можно использовать с Event Sourcing.

from typing import List, Dict
from dataclasses import dataclass


# =============== Commands ===============
@dataclass
class CreateTaskCommand:
    title: str
    description: str


@dataclass
class UpdateTaskCommand:
    task_id: int
    title: str = None
    description: str = None


# =============== Queries ===============
@dataclass
class GetTaskQuery:
    task_id: int


@dataclass
class GetAllTasksQuery:
    pass


# =============== Models ===============
@dataclass
class Task:
    id: int
    title: str
    description: str


# =============== Write Model (для команд) ===============
class TaskWriteModel:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self._next_id = 1

    def create_task(self, command: CreateTaskCommand) -> int:
        task_id = self._next_id
        self.tasks[task_id] = Task(id=task_id, title=command.title, description=command.description)
        self._next_id += 1
        return task_id

    def update_task(self, command: UpdateTaskCommand):
        task = self.tasks.get(command.task_id)
        if not task:
            raise ValueError(f"Task with id {command.task_id} not found")
        if command.title is not None:
            task.title = command.title
        if command.description is not None:
            task.description = command.description


# =============== Read Model (для запросов) ===============
class TaskReadModel:
    def __init__(self, write_model: TaskWriteModel):
        self.write_model = write_model

    def get_task(self, query: GetTaskQuery) -> Task:
        return self.write_model.tasks.get(query.task_id)

    def get_all_tasks(self, query: GetAllTasksQuery) -> List[Task]:
        return list(self.write_model.tasks.values())


# =============== Handlers ===============
class CommandHandler:
    def __init__(self, write_model: TaskWriteModel):
        self.write_model = write_model

    def handle(self, command):
        if isinstance(command, CreateTaskCommand):
            return self.write_model.create_task(command)
        elif isinstance(command, UpdateTaskCommand):
            self.write_model.update_task(command)
        else:
            raise ValueError(f"Unknown command: {type(command)}")


class QueryHandler:
    def __init__(self, read_model: TaskReadModel):
        self.read_model = read_model

    def handle(self, query):
        if isinstance(query, GetTaskQuery):
            return self.read_model.get_task(query)
        elif isinstance(query, GetAllTasksQuery):
            return self.read_model.get_all_tasks(query)
        else:
            raise ValueError(f"Unknown query: {type(query)}")


# =============== Использование ===============
write_model = TaskWriteModel()
read_model = TaskReadModel(write_model)

command_handler = CommandHandler(write_model)
query_handler = QueryHandler(read_model)

# Создаём задачу
task_id = command_handler.handle(CreateTaskCommand("Купить молоко", "С утра"))
print(f"Created task with id: {task_id}")

# Читаем задачу
task = query_handler.handle(GetTaskQuery(task_id))
print(f"Task: {task}")

# Читаем все задачи
all_tasks = query_handler.handle(GetAllTasksQuery())
print(f"All tasks: {all_tasks}")
