import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://quarkus:quarkus@localhost:5432/quarkus",
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "attendees")
