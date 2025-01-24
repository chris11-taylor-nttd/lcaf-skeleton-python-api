from uuid import uuid4

from src.models.people import Person


def test_greeting_nobody(empty_server_client):
    response = empty_server_client.get("/greetings")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hello!"}


def test_greeting_missing_user(empty_server_client):
    nonexistent_uuid = str(uuid4())

    response = empty_server_client.get(f"/greetings/{nonexistent_uuid}")
    assert response.status_code == 404


def test_greeting_not_birthday(empty_server_client, yesterday):
    person = Person(
        identifier=uuid4(),
        name="Diana",
        birthday=yesterday,
    )

    create_response = empty_server_client.post(
        "/people", json={k: str(v) for k, v in person.model_dump().items()}
    )
    assert create_response.status_code == 200
    greet_response = empty_server_client.get("/greetings/" + str(person.identifier))
    retrieved = greet_response.json()
    assert retrieved["greeting"] == f"Hello, {person.name}!"


def test_greeting_birthday(empty_server_client, today):
    person = Person(
        identifier=uuid4(),
        name="Diana",
        birthday=today,
    )

    create_response = empty_server_client.post(
        "/people", json={k: str(v) for k, v in person.model_dump().items()}
    )
    assert create_response.status_code == 200
    greet_response = empty_server_client.get("/greetings/" + str(person.identifier))
    retrieved = greet_response.json()
    assert retrieved["greeting"] == f"Hello and happy birthday, {person.name}!"
