import pytest
from unittest.mock import Mock
from library.models.models import Person
from library.services.person_service import PersonService

@pytest.fixture
def person_service():
    """Provides a PersonService instance with a mocked repository."""
    mock_repo = Mock()
    return PersonService(mock_repo)

def test_add_new_person_success(person_service):
    """Tests a successful person addition."""
    # The repository's add_person method should return the person with an ID from the database
    person_service.person_repository.add_person.return_value = Person(id=1, name="Mock Person", phone_number="123-456")
    new_person = person_service.add_new_person("Mock Person", "123-456")
    assert new_person.name == "Mock Person"
    assert new_person.id == 1
    person_service.person_repository.add_person.assert_called_once()

def test_add_new_person_with_empty_name_raises_error(person_service):
    """Tests that adding a person with an empty name raises a ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        person_service.add_new_person("", "123-456")
    person_service.person_repository.add_person.assert_not_called()

def test_update_person_success(person_service):
    """Tests that a person can be successfully updated."""
    # Mock the get_person_by_id call to simulate finding a person
    person_service.person_repository.get_person_by_id.return_value = Person(id=1, name="Old Name", phone_number="123")
    
    person_service.update_person(1, "New Name", "456")
    
    # Assert that the update method was called correctly
    person_service.person_repository.update_person.assert_called_once_with(1, "New Name", "456")

def test_update_nonexistent_person_raises_error(person_service):
    """Tests that updating a non-existent person raises an error."""
    # Mock the get_person_by_id call to simulate not finding a person
    person_service.person_repository.get_person_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Person with ID '999' not found."):
        person_service.update_person(999, new_name="New Name")
        
    person_service.person_repository.update_person.assert_not_called()