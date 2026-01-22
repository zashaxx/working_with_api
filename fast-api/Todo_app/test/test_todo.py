from venv import create
import pytest
from sqlalchemy import Engine, create_engine, over, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..routers.todos import get_current_user, get_db
from ..database import Base
from ..main import app
from ..models import Todo
from fastapi.testclient import TestClient
from fastapi import status


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base.metadata.create_all(bind=Engine)


def override_get_db():

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "testuser", "id": 1, "user_id": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todo(
        title="Install Linux",
        description="Uninstall Windows Embrace Linux !",
        priority=5,
        completed=True,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with Engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Install Linux",
            "description": "Uninstall Windows Embrace Linux !",
            "priority": 5,
            "completed": True,
            "owner_id": 1,
            "id": 1,
        }
    ]
