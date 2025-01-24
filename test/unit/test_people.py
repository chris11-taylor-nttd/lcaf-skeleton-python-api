import random
from uuid import UUID, uuid4

from src.models.people import Person


def test_person_birthday(yesterday, today):
    person = Person(
        identifier=uuid4(),
        name="Diana",
    )
    assert not person.is_birthday()

    person.birthday = yesterday
    assert not person.is_birthday()

    person.birthday = today
    assert person.is_birthday()


def test_read_empty_people(empty_server_client):
    response = empty_server_client.get("/people")
    assert response.status_code == 200
    assert response.json() == {}


def test_read_all_people_emits_log(caplog, empty_server_client):
    with caplog.at_level("INFO"):
        empty_server_client.get("/people")
        assert "Retrieving all people!" in caplog.text


def test_read_populated_people(populated_server_client, example_users_response):
    response = populated_server_client.get("/people")
    assert response.status_code == 200
    assert response.json() == example_users_response


def test_get_person(populated_server_client, example_users):
    person_to_get = random.choice([k for k in example_users.keys()])

    response = populated_server_client.get(f"/people/{person_to_get}")
    assert response.status_code == 200
    retrieved = response.json()
    assert retrieved["name"] == example_users[person_to_get].name
    assert retrieved["birthday"] == example_users[person_to_get].birthday.strftime(
        "%Y-%m-%d"
    )
    assert retrieved["identifier"] == str(person_to_get)


def test_get_person_missing(empty_server_client):
    nonexistent_uuid = str(uuid4())

    response = empty_server_client.get(f"/people/{nonexistent_uuid}")
    assert response.status_code == 404


def test_add_person(empty_server_client):
    response = empty_server_client.post(
        "/people", json={"name": "Alice", "birthday": "2001-01-01"}
    )
    assert response.status_code == 200
    retrieved = response.json()
    assert retrieved["name"] == "Alice"
    assert retrieved["birthday"] == "2001-01-01"
    assert retrieved["identifier"] is not None
    assert UUID(retrieved["identifier"], version=4)


def test_replace_person(populated_server_client, example_users):
    person_to_replace = random.choice([k for k in example_users.keys()])

    response = populated_server_client.put(
        f"/people/{person_to_replace}",
        json={"name": "Replaced", "birthday": "1999-01-01"},
    )
    assert response.status_code == 200
    retrieved = response.json()
    assert retrieved["name"] == "Replaced"
    assert retrieved["birthday"] == "1999-01-01"
    assert retrieved["identifier"] is not None
    assert UUID(retrieved["identifier"], version=4) == person_to_replace


def test_replace_person_missing(empty_server_client):
    nonexistent_uuid = str(uuid4())

    response = empty_server_client.put(
        f"/people/{nonexistent_uuid}",
        json={"name": "Should 404", "birthday": "1999-01-01"},
    )
    assert response.status_code == 404


def test_partial_update_person(populated_server_client, example_users):
    person_to_update = random.choice([k for k in example_users.keys()])

    pre_update = example_users[person_to_update]

    response = populated_server_client.patch(
        f"/people/{person_to_update}",
        json={
            "name": "Renamed",
        },
    )
    assert response.status_code == 200
    retrieved = response.json()
    assert retrieved["name"] == "Renamed"
    assert retrieved["birthday"] == pre_update.birthday.strftime("%Y-%m-%d")
    assert retrieved["identifier"] is not None
    assert UUID(retrieved["identifier"], version=4) == person_to_update


def test_partial_update_person_missing(empty_server_client):
    nonexistent_uuid = str(uuid4())

    response = empty_server_client.patch(
        f"/people/{nonexistent_uuid}",
        json={
            "name": "Should 404",
        },
    )
    assert response.status_code == 404


def test_delete_person(populated_server_client, example_users):
    original_people_count = len(example_users)
    person_to_delete = random.choice([k for k in example_users.keys()])

    response = populated_server_client.delete(f"/people/{person_to_delete}")
    assert response.status_code == 200

    retrieved_people = populated_server_client.get("/people").json()
    assert str(person_to_delete) not in retrieved_people.keys()
    assert len(retrieved_people.keys()) == original_people_count - 1


def test_delete_person_missing(empty_server_client):
    nonexistent_uuid = str(uuid4())

    response = empty_server_client.delete(f"/people/{nonexistent_uuid}")
    assert response.status_code == 200
