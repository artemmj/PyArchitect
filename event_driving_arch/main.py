from typing import Callable, List


# Понимание Event-Driven Architecture.
# Паттерн Observer или Publish-Subscribe.
# Модульность и слабую связанность компонентов.

# Слабая связанность между компонентами.
# Подходит для систем с высокой модульностью.
# Используется паттерн Observer.


class EventManager:
    def __init__(self):
        self._listeners: dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)

    def publish(self, event_type: str, data: dict):
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(data)


class UserService:
    def __init__(self, events: EventManager):
        self.events = events

    def register_user(self, name: str):
        print(f"User {name} registered.")
        # Публикуем событие
        self.events.publish("user_registered", {"name": name})


def send_welcome_email(data):
    print(f"Sending welcome email to {data['name']}")


def log_user_registration(data):
    print(f"Log: User {data['name']} registered.")


# Использование
events = EventManager()
events.subscribe("user_registered", send_welcome_email)
events.subscribe("user_registered", log_user_registration)


service = UserService(events)
service.register_user("Alice")
