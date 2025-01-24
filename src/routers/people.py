import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import UUID4

from ..dependencies import app_logs, people_data
from ..models.people import People, Person, PersonUpdate

router = APIRouter(
    prefix="/people",  # All routes of this router will be prefixed with /people
    tags=["people"],  # Tag the routes for OpenAPI documentation
)


@router.get("")
def get_all_people(
    people_data: Annotated[People, Depends(people_data)],
    logger: Annotated[logging.Logger, Depends(app_logs)],
) -> People:
    """A route that returns all the people contained within
    the system as a dictionary of people keyed by their identifier."""
    logger.info("Retrieving all people!")
    return people_data


@router.get("/{person_id}")
def get_person(
    person_id: UUID4, people_data: Annotated[People, Depends(people_data)]
) -> Person:
    """A route that returns a specific person by their numeric identifier.
    Will result in 404 Not Found if no person with the specified identifier
    is found."""
    if person_id not in people_data:
        raise HTTPException(status_code=404, detail="Person identifier not found")
    return people_data[person_id]


@router.post("")
def create_person(
    person: Person, people_data: Annotated[People, Depends(people_data)]
) -> Person:
    """A route to add a person to the system. Returns the created person."""
    people_data[person.identifier] = person
    return person


@router.put("/{person_id}")
def replace_person(
    person: Person,
    person_id: UUID4,
    people_data: Annotated[People, Depends(people_data)],
) -> Person:
    """A route to replace an existing person by their identifier. May return a
    404 Not Found if no person with the specified identifier is found, or a
    422 Unprocessable Content response if the person object is invalid. On
    success, returns the updated person.
    """
    if person_id not in people_data:
        raise HTTPException(status_code=404, detail="Person identifier not found")
    person.identifier = person_id
    people_data[person_id] = person
    return person


@router.patch("/{person_id}")
def update_person(
    person: PersonUpdate,
    person_id: UUID4,
    people_data: Annotated[People, Depends(people_data)],
) -> Person:
    """A route to perform a partial update of a person. May return a
    404 Not Found if no person with the specified identifier is found, or a
    422 Unprocessable Content response if the person object is invalid. On
    success, returns the updated person.
    """
    if person_id not in people_data:
        raise HTTPException(status_code=404, detail="Person identifier not found")
    existing_person = people_data[person_id]
    update_data = person.model_dump(exclude_unset=True)
    updated_person = existing_person.model_copy(update=update_data)
    people_data[person_id] = updated_person
    return updated_person


@router.delete("/{person_id}")
def delete_person(
    person_id: UUID4, people_data: Annotated[People, Depends(people_data)]
) -> Person:
    """A route to delete a person. On success, returns the deleted person, if they existed."""
    if person_id in people_data:
        deleted_person = people_data[person_id]
        del people_data[person_id]
        return deleted_person
    else:
        return Response(status_code=200)
