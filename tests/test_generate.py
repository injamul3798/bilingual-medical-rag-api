def test_generate_response_default_language(client, auth_headers):
    files = {"file": ("doc.txt", "Ibuprofen may reduce pain and inflammation.", "text/plain")}
    ingest_resp = client.post("/ingest", files=files, headers=auth_headers)
    assert ingest_resp.status_code == 200

    response = client.post("/generate", json={"query": "What does ibuprofen do?", "top_k": 3}, headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["query_language"] in ["en", "ja"]
    assert body["output_language"] in ["en", "ja"]
    assert isinstance(body["source_documents"], list)


def test_generate_with_translation_toggle(client, auth_headers):
    files = {"file": ("doc.txt", "Paracetamol helps with fever.", "text/plain")}
    ingest_resp = client.post("/ingest", files=files, headers=auth_headers)
    assert ingest_resp.status_code == 200

    response = client.post(
        "/generate",
        json={"query": "What is paracetamol for?", "output_language": "ja", "top_k": 3},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["output_language"] == "ja"
