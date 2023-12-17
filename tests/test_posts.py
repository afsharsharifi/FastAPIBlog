from schemas import post as post_schemas
import pytest


def test_get_all_posts(client, test_posts):
    res = client.get("/posts")

    def validate(post):
        return post_schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(posts_list) == len(test_posts)
    assert res.status_code == 200


def test_get_single_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    post = post_schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.created_at == test_posts[0].created_at
    assert res.status_code == 200


@pytest.mark.parametrize(
    "post_id, status_code",
    [
        (0, 404),
        ("string_pass", 422),
    ],
)
def test_get_invalid_single_post(client, post_id, status_code):
    res = client.get(f"/posts/{post_id}")
    assert res.status_code == status_code


@pytest.mark.parametrize(
    "title, content, is_published",
    [
        ("title 1", "<h1>This is Content 1</h1>", True),
        ("title 1", "<h1>This is Content 1</h1>", False),
        ("title 1", "<h1>This is Content 1</h1>", True),
    ],
)
def test_create_post(authorized_client, test_user, test_posts, title, content, is_published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "is_published": is_published},
    )
    created_post = post_schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.is_published == is_published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_is_published(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/",
        json={"title": "is_published default value", "content": "Default Value for is_published is True"},
    )
    created_post = post_schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "is_published default value"
    assert created_post.is_published == True
    assert created_post.owner_id == test_user["id"]


def test_create_post_unauthorized(client, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "is_published default value", "content": "Default Value for is_published is True"},
    )
    assert res.status_code == 401


@pytest.mark.parametrize(
    "title, content",
    [
        (None, "<h1>This is Content 1</h1>"),
        ("title 1", None),
    ],
)
def test_create_post_invalid(authorized_client, test_posts, title, content):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content},
    )
    assert res.status_code == 422
