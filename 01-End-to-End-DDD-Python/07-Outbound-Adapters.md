# Step 7: Outbound Adapters

## tl;dr

_If you want to get the application up and running as quickly as possible you can copy/paste the code into the stubbed classes without reading the rest of the material._

Create `conference/attendees/infrastructure/event_publisher.py`:

```python
import json
import logging

from aiokafka import AIOKafkaProducer

from conference.attendees.domain.events import AttendeeRegisteredEvent

logger = logging.getLogger(__name__)


class AttendeeEventPublisher:
    def __init__(self, producer: AIOKafkaProducer, topic: str = "attendees"):
        self._producer = producer
        self._topic = topic

    async def publish(self, event: AttendeeRegisteredEvent) -> None:
        if self._producer is None:
            logger.warning("No Kafka producer configured; skipping event publish for %s", event.email)
            return
        value = json.dumps({"email": event.email}).encode("utf-8")
        await self._producer.send_and_wait(self._topic, value=value)
        logger.info("Published AttendeeRegisteredEvent for %s", event.email)
```

[Step 8: Application Services](08-Application-Services.md)

---

## Concept

An **outbound adapter** is the piece of your architecture that talks to external systems on behalf of the domain. The domain produces an event (an `AttendeeRegisteredEvent`) and hands it to a port. The adapter behind that port knows how to translate the event into whatever the external system expects -- in our case, a JSON message on a Kafka topic.

The critical insight is that the domain never knows about Kafka. The `AttendeeRegisteredEvent` is a plain frozen dataclass. The `AttendeeEventPublisher` is the only class that imports `aiokafka` or calls `send_and_wait`. If you later replace Kafka with RabbitMQ, Redis Streams, or even a simple log file, you change only this one adapter class. The domain and services remain untouched.

In the Java version, Quarkus uses MicroProfile Reactive Messaging with `@Channel` and `Emitter<>` to send messages. The Python equivalent is `aiokafka`, an asyncio-native Kafka client. Where Java injects an `Emitter` via CDI, we inject an `AIOKafkaProducer` via the constructor.

## Implementation

Create or update `conference/attendees/infrastructure/event_publisher.py`:

```python
import json
import logging

from aiokafka import AIOKafkaProducer

from conference.attendees.domain.events import AttendeeRegisteredEvent

logger = logging.getLogger(__name__)


class AttendeeEventPublisher:
    """
    Outbound adapter for publishing domain events to Kafka.

    "The application is blissfully ignorant of the nature of the input device.
    When the application has something to send out, it sends it out through a port
    to an adapter, which creates the appropriate signals needed by the receiving
    technology."
    -- Alistair Cockburn, Hexagonal Architecture, 2005
    """

    def __init__(self, producer: AIOKafkaProducer, topic: str = "attendees"):
        # The producer is injected from the outside.
        # In Java/Quarkus this would be: @Channel("attendees") Emitter<AttendeeRegisteredEvent>
        self._producer = producer
        self._topic = topic

    async def publish(self, event: AttendeeRegisteredEvent) -> None:
        """Publish a domain event to the Kafka topic."""

        # Guard clause: when Kafka is not available (e.g., during testing
        # or local development without Docker), skip publishing gracefully.
        if self._producer is None:
            logger.warning(
                "No Kafka producer configured; skipping event publish for %s",
                event.email,
            )
            return

        # Serialize the domain event to JSON bytes.
        # The adapter is responsible for this translation -- the domain
        # event itself is a plain dataclass with no serialization logic.
        value = json.dumps({"email": event.email}).encode("utf-8")

        # send_and_wait is the async equivalent of Emitter.send().
        # It blocks (awaits) until Kafka acknowledges receipt.
        await self._producer.send_and_wait(self._topic, value=value)
        logger.info("Published AttendeeRegisteredEvent for %s", event.email)
```

### Comparing to the Java Version

| Java (MicroProfile Reactive Messaging)         | Python (aiokafka)                              |
|------------------------------------------------|------------------------------------------------|
| `@Channel("attendees") Emitter<Event> emitter` | `__init__(self, producer: AIOKafkaProducer)`   |
| `emitter.send(event)`                          | `await self._producer.send_and_wait(...)`      |
| Automatic JSON serialization                   | Manual `json.dumps()` + `.encode("utf-8")`     |
| `@Inject` via CDI                              | Constructor parameter                          |
| MicroProfile config for topic name             | `topic` parameter with default value           |

### The None-Producer Guard

Notice the `if self._producer is None` check at the top of `publish()`. This is a practical pattern for workshop and development environments where Kafka may not be running. Instead of crashing the entire registration flow because a message broker is unavailable, the adapter logs a warning and continues. In production, you would initialize the producer at application startup and this guard would never trigger.

## Key Design Decisions

- **The domain does not know about Kafka.** The `AttendeeRegisteredEvent` is a frozen dataclass defined in the domain layer. It has no `to_json()` method, no Kafka-specific annotations, and no serialization logic. The adapter handles all technology translation.

- **The publisher is async.** Kafka I/O is inherently asynchronous. By making `publish()` an `async` method, we integrate naturally with FastAPI's async request handling without blocking the event loop. The Java `Emitter.send()` is also non-blocking under the hood.

- **Graceful degradation via the None guard.** Rather than making Kafka a hard dependency, the adapter can operate with `producer=None`. This keeps the application functional during development and testing even when Kafka is not available.

## Testing

Create `tests/infrastructure/test_event_publisher.py`:

```python
from unittest.mock import AsyncMock, MagicMock

import pytest

from conference.attendees.domain.events import AttendeeRegisteredEvent
from conference.attendees.infrastructure.event_publisher import AttendeeEventPublisher


class TestAttendeeEventPublisher:
    @pytest.mark.asyncio
    async def test_publish_sends_to_kafka(self):
        mock_producer = MagicMock()
        mock_producer.send_and_wait = AsyncMock()

        publisher = AttendeeEventPublisher(producer=mock_producer, topic="attendees")
        event = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")

        await publisher.publish(event)

        mock_producer.send_and_wait.assert_called_once()
        # Verify the topic and serialized value
        call_args = mock_producer.send_and_wait.call_args
        assert call_args[0][0] == "attendees"

    @pytest.mark.asyncio
    async def test_publish_skips_when_no_producer(self):
        publisher = AttendeeEventPublisher(producer=None)
        event = AttendeeRegisteredEvent(email="gandalfthegrey@istari.net")

        # Should not raise -- just logs a warning
        await publisher.publish(event)
```

Because the publisher depends on an `AIOKafkaProducer` passed via the constructor, we can substitute a `MagicMock` in tests. No Kafka broker needed, no Docker containers, no network calls. This is the testability benefit of hexagonal architecture.

## Next Step

With the outbound adapter in place, we have both persistence (repository) and messaging (event publisher) ready. Next we will wire them together in the application service: [Step 8: Application Services](08-Application-Services.md)
