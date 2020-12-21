import pytest

from book_library_app import create_app, db


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    app.config['DB_FILE_PATH'].unlink(missing_ok=True)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def user(client):
    user = {
        'username': 'test25',
        'password': ' 123456',
        'email': 'test25@gmail.com'
    }
    client.post('/api/v1/auth/register', json=user)
    return user
