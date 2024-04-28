import unittest
from unittest.mock import Mock
from source.model.meta_model import Meta
from source.model.person_model import Person
from source.enum.gender_enum import GenderEnum
from source.services.person_service import PersonService
from datetime import datetime

class TestPersonService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.person_service = PersonService(repository=self.mock_repo)
        self.person_id = "12"
        self.meta_id = "34"

    def test_get_person(self):
        self.mock_repo.get_person.return_value = Person(
            id=self.person_id, name="John", age=30, weight=80, gender=GenderEnum.male, created_at= datetime.now(), meta = None
        )
        person = self.person_service.get_person(self.person_id)

        self.mock_repo.get_person.assert_called_once_with(self.person_id)
        self.assertIsInstance(person, Person)

    def test_create_person(self):
        
        self.person_service.create_person(
            name="Alice", age=28, weight=70, gender=GenderEnum.female
        )
        self.mock_repo.add_person.assert_called_once()
        person = self.mock_repo.add_person.call_args[0][0]
        
        self.assertIsNotNone(person.created_at)
        self.assertEqual(person.name, "Alice")
        self.assertEqual(person.age, 28)
        self.assertEqual(person.weight, 70)
        self.assertEqual(person.gender, GenderEnum.female)
        self.assertIsNone(person.meta)

    def test_update_person(self):
        self.person_service.update_person(person_id=self.person_id, name="Bob", age=35, weight=90, gender=GenderEnum.male)
        self.mock_repo.update_person.assert_called_once()
        
        person = self.mock_repo.update_person.call_args[0][0]
        self.assertEqual(person.id, self.person_id)
        self.assertEqual(person.name, "Bob")
        self.assertEqual(person.age, 35)
        self.assertEqual(person.weight, 90)
        self.assertEqual(person.gender, GenderEnum.male)

    def test_delete_person(self):
        self.person_service.delete_person(self.person_id)
        self.mock_repo.delete_person.assert_called_once_with(self.person_id)

    def test_add_meta(self):
        self.person_service.add_meta(self.person_id, 2.5, 1)
        self.mock_repo.add_meta.assert_called_once_with(self.person_id, Meta(quantity=2.5, period=1))

    def test_update_meta(self):
        self.person_service.update_meta(self.person_id, self.meta_id, 3.0, 2)
        self.mock_repo.update_meta.assert_called_once_with(self.person_id, Meta(id=self.meta_id, quantity=3.0, period=2))

    def test_remove_meta(self):
        self.person_service.remove_meta(self.person_id, self.meta_id)
        self.mock_repo.remove_meta.assert_called_once_with(self.person_id, self.meta_id)

if __name__ == '__main__':
    unittest.main()