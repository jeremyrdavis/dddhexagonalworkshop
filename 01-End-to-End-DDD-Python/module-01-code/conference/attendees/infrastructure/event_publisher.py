import logging

from aiokafka import AIOKafkaProducer

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

    # TODO: Add async publish() method
