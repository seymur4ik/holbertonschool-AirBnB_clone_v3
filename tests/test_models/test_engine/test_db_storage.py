#!/usr/bin/python3
"""Defines unnittests for models/engine/db_storage.py."""
import unittest
from os import getenv
import os

from models import storage
import MySQLdb
import pep8
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

import models
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup.

        Instantiate new DBStorage.
        Fill DBStorage test session with instances of all classes.
        """
        if type(models.storage) is DBStorage:
            cls.storage = DBStorage()
            Base.metadata.create_all(cls.storage._DBStorage__engine)
            Session = sessionmaker(bind=cls.storage._DBStorage__engine)
            cls.storage._DBStorage__session = Session()
            cls.state = State(name="California")
            cls.storage._DBStorage__session.add(cls.state)
            cls.city = City(name="San_Jose", state_id=cls.state.id)
            cls.storage._DBStorage__session.add(cls.city)
            cls.user = User(email="poppy@holberton.com", password="betty")
            cls.storage._DBStorage__session.add(cls.user)
            cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                              name="School")
            cls.storage._DBStorage__session.add(cls.place)
            cls.amenity = Amenity(name="Wifi")
            cls.storage._DBStorage__session.add(cls.amenity)
            cls.review = Review(place_id=cls.place.id, user_id=cls.user.id,
                                text="stellar")
            cls.storage._DBStorage__session.add(cls.review)
            cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """DBStorage testing teardown.

        Delete all instantiated test classes.
        Clear DBStorage session.
        """
        if type(models.storage) is DBStorage:
            cls.storage._DBStorage__session.delete(cls.state)
            cls.storage._DBStorage__session.delete(cls.city)
            cls.storage._DBStorage__session.delete(cls.user)
            cls.storage._DBStorage__session.delete(cls.amenity)
            cls.storage._DBStorage__session.commit()
            del cls.state
            del cls.city
            del cls.user
            del cls.place
            del cls.amenity
            del cls.review
            cls.storage._DBStorage__session.close()
            del cls.storage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_attributes(self):
        """Check for attributes."""
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.storage, DBStorage))

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_all(self):
        """Test default all method."""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_all_cls(self):
        """Test all method with specified cls."""
        obj = self.storage.all(State)
        self.assertEqual(type(obj), dict)

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        """Test new method."""
        st = State(name="Washington")
        self.storage.new(st)
        store = list(self.storage._DBStorage__session.new)
        self.assertIn(st, store)

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_delete(self):
        """Test delete method."""
        st = State(name="New_York")
        self.storage._DBStorage__session.add(st)
        self.storage._DBStorage__session.commit()
        self.storage.delete(st)
        self.assertIn(st, list(self.storage._DBStorage__session.deleted))

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_delete_none(self):
        """Test delete method with None."""
        try:
            self.storage.delete(None)
        except Exception:
            self.fail

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_reload(self):
        """Test reload method."""
        og_session = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(og_session, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = og_session

# updated
    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_get(self):
        # state_id = "8f165686-c98d-46d9-87d9-d6059ade2d99"
        # state_name = "Louisiana"
        # state = State(id=state_id, name=state_name)
        # state.save()
        # retrieved_state = storage.get(State, state_id)
        # self.assertIsNotNone(retrieved_state)
        # self.assertEqual(retrieved_state.name, state_name)
        state1 = State(name="California")
        state2 = State(name="New York")
        state3 = State(name="Texas")
        state1.save()
        state2.save()
        state3.save()
        count = storage.count(State)
        self.assertEqual(count, 15)

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Testing FileStorage")
    def test_count(self):
        """Test the count method of the storage"""
        state1 = State(name="California")
        state2 = State(name="New York")
        state3 = State(name="Texas")
        state1.save()
        state2.save()
        state3.save()
        count = storage.count(State)
        self.assertEqual(count, 11)


if __name__ == "__main__":
    unittest.main()