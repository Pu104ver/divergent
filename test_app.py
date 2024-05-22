import pytest

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_posts(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'application/json' in response.content_type
    data = response.get_json()
    assert 'posts' in data
    assert 'total_results' in data
    assert isinstance(data['posts'], list)

def test_get_post(client):
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert 'application/json' in response.content_type
    data = response.get_json()
    assert 'id' in data
    assert 'title' in data
    assert 'body' in data
    assert 'author' in data
    assert 'created_at' in data
    assert 'comments' in data
    assert isinstance(data['comments'], list)

def test_get_post_not_found(client):
    response = client.get('/posts/100')
    assert response.status_code == 404
    data = response.get_json()
    assert data is None

