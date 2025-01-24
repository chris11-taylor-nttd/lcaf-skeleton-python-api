from datetime import date
from typing import TypeAlias
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


# The model classes below are used to define the structure of the data that the
# API will accept and return.
class Person(BaseModel):
    identifier: UUID4 | None = Field(
        default_factory=uuid4,
        description="Unique identifier",
    )
    name: str = Field(description="Name of the person")
    birthday: date | None = Field(
        default=None,
        description="The person's birth date, if known",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "identifier": "0000000-0000-4000-8000-000000000000",
                    "name": "Alice",
                    "birthday": "2001-01-01",
                },
            ]
        }
    }

    def is_birthday(self) -> bool:
        """Check if today is the person's birthday."""
        if self.birthday is None:
            return False
        return (
            self.birthday.month == date.today().month
            and self.birthday.day == date.today().day
        )


# This variant of the Person model is used with the PATCH verb to accept
# partial updates, i.e. only the fields that are provided in the request body
class PersonUpdate(BaseModel):
    name: str | None = None
    birthday: date | None = None


People: TypeAlias = dict[UUID4, Person]
