from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import json


# Понимание, что такое Event Store и зачем он нужен.
# Как хранить, читать, и восстанавливать события.
# Связь с Event Sourcing и CQRS.

# Простая реализация Event Store.
# Подходит для систем с Event Sourcing.
# Можно расширить: persistence, versioning, snapshots.


@dataclass
class Event:
    event_type: str
    data: Dict[str, Any]


class EventStore:
    def __init__(self):
        self.events: List[Event] = []
        self.streams: Dict[str, List[Event]] = {}

    def append_to_stream(self, stream_name: str, event: Event):
        if stream_name not in self.streams:
            self.streams[stream_name] = []
        self.streams[stream_name].append(event)
        self.events.append(event)

    def get_stream(self, stream_name: str) -> List[Event]:
        return self.streams.get(stream_name, [])

    def replay_stream(self, stream_name: str) -> List[Dict[str, Any]]:
        events = self.get_stream(stream_name)
        return [asdict(e) for e in events]


# Использование
store = EventStore()

# Записываем события
store.append_to_stream("user-123", Event("UserCreated", {"name": "Alice", "email": "alice@example.com"}))
store.append_to_stream("user-123", Event("UserUpdated", {"name": "Alice Cooper"}))

# Читаем события
events = store.replay_stream("user-123")
print(json.dumps(events, indent=2))
