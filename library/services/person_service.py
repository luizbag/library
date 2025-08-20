from typing import List
from ..models.models import Person
from ..data.person_repository import PersonRepository

class PersonService:
    def __init__(self, person_repository: PersonRepository):
        self.person_repository = person_repository

    def add_new_person(self, name: str, phone_number: str) -> Person:
        """
        Validates person data and adds a new person.
        
        Args:
            name: The name of the person.
            phone_number: The person's phone number.
            
        Returns:
            The newly created Person object.
        
        Raises:
            ValueError: If the name is empty or if a person with the
                        same name already exists.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
            
        new_person = Person(name, phone_number)
        return self.person_repository.add_person(new_person)
        
    def update_person(self, person_id: int, new_name: str = None, new_phone_number: str = None):
        """
        Updates a person's details.
        
        Args:
            person_id: The ID of the person to update.
            new_name: The new name (optional).
            new_phone_number: The new phone number (optional).
            
        Raises:
            ValueError: If the person to update is not found.
        """
        person_to_update = self.person_repository.get_person_by_id(person_id)
        if person_to_update is None:
            raise ValueError(f"Person with ID '{person_id}' not found.")
            
        self.person_repository.update_person(person_id, new_name, new_phone_number)


    def get_person_by_name(self, name: str) -> Person:
        """
        Retrieves a single person by their name.
        
        Args:
            name: The name of the person to retrieve.
            
        Returns:
            The Person object, or None if not found.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
            
        return self.person_repository.get_person_by_name(name)

    def get_all_people(self) -> List[Person]:
        """
        Retrieves all people from the library.
        
        Returns:
            A list of all Person objects.
        """
        return self.person_repository.get_all_people()