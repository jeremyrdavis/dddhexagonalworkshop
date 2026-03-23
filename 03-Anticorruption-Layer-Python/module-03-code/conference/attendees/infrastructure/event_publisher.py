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
        self._producer = producer
        self._topic = topic

    async def publish(self, event: AttendeeRegisteredEvent) -> None:
        """Publish a domain event to the Kafka topic."""
        if self._producer is None:
            logger.warning("No Kafka producer configured; skipping event publish for %s", event.email)
            return
        value = json.dumps({"email": event.email, "full_name": event.full_name}).encode("utf-8")
        await self._producer.send_and_wait(self._topic, value=value)
        logger.info("Published AttendeeRegisteredEvent for %s", event.email)
