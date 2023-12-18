def test_like_post_success(authorized_client, test_post):
    authorized_client.post("/like/", json={"post_id": test_post[0].id})
    pass
