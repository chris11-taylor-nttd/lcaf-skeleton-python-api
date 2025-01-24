import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from ..dependencies import app_logs, people_data
from ..models.greetings import Greeting, GreetingResponse
from ..models.people import People

router = APIRouter(
    prefix="/greetings",  # All routes of this router will be prefixed with /greetings
    tags=["greetings"],  # Tag the routes for OpenAPI documentation
)


@router.get("")
def greet_nobody() -> GreetingResponse:
    """A route that returns a greeting for nobody in particular."""
    return {"greeting": Greeting().greet()}


@router.get("/{person_id}")
def greet_person(
    person_id: UUID4,
    people_data: Annotated[People, Depends(people_data)],
    logger: Annotated[logging.Logger, Depends(app_logs)],
) -> GreetingResponse:
    """A route that returns a specific person by their numeric identifier.
    Will result in 404 Not Found if no person with the specified identifier
    is found."""
    if person_id not in people_data:
        raise HTTPException(status_code=404, detail="Person identifier not found")
    logger.info(f"Generating greeting for person with ID {person_id}")
    return {"greeting": Greeting(person=people_data[person_id]).greet()}
