import logging

from .models.people import People

# An ephemeral dict in which to store people. Normally this would be a database
# or some other system that provides persistence, but this is fine for an example.
people_storage: People = dict()

logger: logging.Logger = logging.getLogger("my_application")


async def people_data():
    return people_storage


async def app_logs() -> logging.Logger:
    return logger
