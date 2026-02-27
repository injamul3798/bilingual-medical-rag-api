def test_ingest_txt_success(client, auth_headers):
    files = {"file": ("sample.txt", "This is a test medical document.\nIt has multiple lines.", "text/plain")}
    response = client.post("/ingest", files=files, headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "sample.txt"
    assert body["language_detected"] in ["en", "ja"]
    assert body["chunks_ingested"] >= 1
    assert "doc_id" in body


def test_ingest_reject_non_txt(client, auth_headers):
    files = {"file": ("sample.pdf", "fake", "application/pdf")}
    response = client.post("/ingest", files=files, headers=auth_headers)
    assert response.status_code == 400


def test_ingest_requires_api_key(client):
    files = {"file": ("sample.txt", "test", "text/plain")}
    response = client.post("/ingest", files=files)
    assert response.status_code == 403
