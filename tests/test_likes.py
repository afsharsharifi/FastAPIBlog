import pytest
from core import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_like_post_success(authorized_client, test_posts):
    post_id = test_posts[3].id
    res = authorized_client.post("vote/like", json={"post_id": post_id})
    assert res.status_code == 201
    assert res.json()["detail"] == f"Successfully Liked Post with ID of {post_id}"


def test_like_post_twice(authorized_client, test_posts, test_vote, test_user):
    post_id = test_posts[3].id
    res = authorized_client.post("vote/like", json={"post_id": post_id})
    assert res.status_code == 409
    assert res.json()["detail"] == f"User with id {test_user['id']} has already liked post with id {post_id}"


def test_like_post_own(authorized_client, test_posts):
    post_id = test_posts[0].id
    res = authorized_client.post("vote/like", json={"post_id": post_id})
    assert res.status_code == 403
    assert res.json()["detail"] == f"Cant Like Own Post"


def test_like_post_not_exists(authorized_client):
    res = authorized_client.post("vote/like", json={"post_id": 0})
    assert res.status_code == 404
    assert res.json()["detail"] == f"Post with id 0 does not exists."


def test_dislike_post_success(authorized_client, test_posts, test_vote):
    post_id = test_posts[3].id
    res = authorized_client.post("vote/dislike", json={"post_id": post_id})
    assert res.status_code == 204


def test_dislike_post_twice(authorized_client, test_posts):
    post_id = test_posts[3].id
    res = authorized_client.post("vote/dislike", json={"post_id": post_id})
    assert res.status_code == 404
    assert res.json()["detail"] == "User hasn't liked this post yet"


def test_dislike_post_own(authorized_client, test_posts):
    post_id = test_posts[0].id
    res = authorized_client.post("vote/dislike", json={"post_id": post_id})
    assert res.status_code == 403
    assert res.json()["detail"] == "Cant Dislike Own Post"


def test_dislike_post_not_exists(authorized_client, test_posts):
    res = authorized_client.post("vote/dislike", json={"post_id": 0})
    assert res.status_code == 404
    assert res.json()["detail"] == "Post with id 0 does not exists."
