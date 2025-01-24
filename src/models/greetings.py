from pydantic import BaseModel

from .people import Person


class Greeting(BaseModel):
    person: Person | None = None

    def greet(self) -> str:
        if self.person is None:
            return "Hello!"
        if self.person.is_birthday():
            return f"Hello and happy birthday, {self.person.name}!"
        return f"Hello, {self.person.name}!"


class GreetingResponse(BaseModel):
    greeting: str
