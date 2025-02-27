import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.fixture()
def post_data():
    return {
        "title": "Тестовый заголовок",
        "content": "Тестовый контент",
        "category": "Тест",
        "tags": ["тег1", "тег2"],
    }


async def test_get_posts(client: AsyncClient):
    response = await client.get("/api/v1/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_post(client: AsyncClient, post_data, test_user):
    post_data["user_id"] = test_user.id

    response = await client.post("/api/v1/posts", json=post_data)
    assert response.status_code == 200
    post = response.json()

    assert post["title"] == post_data["title"]
    assert post["content"] == post_data["content"]
    assert post["category"] == post_data["category"]
    assert post["tags"] == post_data["tags"]
    assert post["user"] == test_user.email


async def test_get_post(client: AsyncClient, post_data):
    response = await client.post("/api/v1/posts", json=post_data)
    assert response.status_code == 200
    post_id = response.json()["id"]

    response = await client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id

    response = await client.get("/api/v1/posts/404")
    assert response.status_code == 404


async def test_update_post(client: AsyncClient, post_data):
    response = await client.post("/api/v1/posts", json=post_data)
    assert response.status_code == 200
    post_id = response.json()["id"]

    update_data = {"title": "Обновлённый заголовок"}
    response = await client.patch(f"/api/v1/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]

    response = await client.patch("/api/v1/posts/404", json=update_data)
    assert response.status_code == 404


async def test_delete_post(client: AsyncClient, post_data):
    response = await client.post("/api/v1/posts", json=post_data)
    assert response.status_code == 200
    post_id = response.json()["id"]

    response = await client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200

    response = await client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 404
