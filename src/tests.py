import unittest

from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings
from database import get_db
from main import app
from models import User

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


User.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestUsersAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.client = TestClient(app)
        self.db = TestingSessionLocal()
        hashed_password = pwd_context.hash("password")
        energy = User(
            id=1,
            username="testuser",
            email="qwerty@example.com",
            full_name="<NAME>",
            user_type="default",
            hashed_password=hashed_password,
        )
        self.db.add(energy)
        self.db.commit()
        self.db.refresh(energy)
        self.db.close()

    def tearDown(self):
        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_register_user(self):
        response = self.client.post(
            "/api/users",
            json={
                "username": "testuser1",
                "email": "testuser@example.com",
                "user_type": "default",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("username", response.json())
        self.assertIn("email", response.json())

    def test_login_user_success(self):
        response = self.client.post(
            "/api/login",
            json={
                "username": "testuser",
                "password": "password",
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "testuser")

    def test_login_user_fail(self):
        response = self.client.post(
            "/api/login",
            json={
                "username": "testuser",
                "password": "wrong_password",
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Wrong password")

    def test_register_duplicate_user(self):
        # Attempt to create the same user that in first test
        response = self.client.post(
            "/api/users",
            json={
                "username": "testuser",
                "email": "testuser@example.com",
                "user_type": "default",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn("User for given data already exists", response.json()["detail"])

    def test_get_users(self):
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_user_by_id(self):
        response = self.client.get("/api/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "testuser")

    def test_update_user(self):
        response = self.client.put(
            "/api/users/1",
            json={
                "username": "updateduser",
                "email": "updated@example.com",
                "user_type": "admin",
                "full_name": "Updated User",
            },
        )
        self.assertEqual(response.status_code, 201)
        updated_user = self.db.query(User).first()
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updated@example.com")

    def test_delete_user(self):
        response = self.client.delete("/api/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User deleted successfully.")
        self.assertIsNone(self.db.query(User).first())


if __name__ == "__main__":
    unittest.main()
