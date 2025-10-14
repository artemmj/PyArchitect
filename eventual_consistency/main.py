import asyncio
from typing import List, Dict


# Понимание, что данные не синхронизируются мгновенно.
# Как согласованность достигается со временем.
# Как события могут использоваться для синхронизации между сервисами.

# Состояние синхронизируется асинхронно.
# Подходит для систем, где мгновенная согласованность не обязательна.
# Используется в микросервисах, Event Sourcing, CQRS.


class Event:
    def __init__(self, type: str, data: dict):
        self.type = type
        self.data = data


class EventStore:
    def __init__(self):
        self.events: List[Event] = []

    def append(self, event: Event):
        self.events.append(event)


class UserService:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.users: Dict[int, str] = {}

    def create_user(self, user_id: int, name: str):
        self.users[user_id] = name
        event = Event("UserCreated", {"id": user_id, "name": name})
        self.event_store.append(event)


class NotificationService:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.notifications: List[dict] = []

    async def sync_from_events(self):
        for event in self.event_store.events:
            if event.type == "UserCreated":
                self.notifications.append({
                    "message": f"Welcome, {event.data['name']}!",
                    "to": event.data['id']
                })


# Использование
store = EventStore()
user_service = UserService(store)
notification_service = NotificationService(store)

user_service.create_user(1, "Alice")


async def main():
    await notification_service.sync_from_events()
    print(notification_service.notifications)


asyncio.run(main())
