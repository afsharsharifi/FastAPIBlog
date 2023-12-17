def test_get_all_posts(client):
    res = client.get("/posts")
    print(res.json())
    assert res.status_code == 200
