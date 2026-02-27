def test_retrieve_returns_results(client, auth_headers):
    files = {"file": ("doc.txt", "Heart rate normal range is 60 to 100 bpm.", "text/plain")}
    ingest_resp = client.post("/ingest", files=files, headers=auth_headers)
    assert ingest_resp.status_code == 200

    response = client.post("/retrieve", json={"query": "normal heart rate", "top_k": 3}, headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["query_language"] in ["en", "ja"]
    assert len(body["results"]) >= 1
    first = body["results"][0]
    assert "text" in first
    assert "score" in first
    assert "doc_id" in first


def test_retrieve_top_k_limit(client, auth_headers):
    response = client.post("/retrieve", json={"query": "test", "top_k": 11}, headers=auth_headers)
    assert response.status_code == 422
