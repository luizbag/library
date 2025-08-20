import pytest
from unittest.mock import Mock
from library.models import Person
from library.services.person_service import PersonService

@pytest.fixture
def person_service():
    """Provides a PersonService instance with a mocked repository."""
    mock_repo = Mock()
    return PersonService(mock_repo)

def test_add_new_person_success(person_service):
    """Tests successful person addition via the service."""
    person_service.person_repository.add_person.return_value = None
    new_person = person_service.add_new_person("Mock Person", "123-456")
    assert new_person.name == "Mock Person"
    person_service.person_repository.add_person.assert_called_once()

def test_add_new_person_with_empty_name_raises_error(person_service):
    """Tests that adding a person with an empty name raises a ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        person_service.add_new_person("", "123-456")
    person_service.person_repository.add_person.assert_not_called()

def test_add_new_person_that_already_exists_raises_error(person_service):
    """Tests that trying to add an existing person raises an error."""
    person_service.person_repository.add_person.side_effect = ValueError("already exists")
    with pytest.raises(ValueError, match="already exists"):
        person_service.add_new_person("Existing Person", "123-456")
    person_service.person_repository.add_person.assert_called_once()