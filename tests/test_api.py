def test_create_and_list_companies(client):
    response = client.post(
        "/companies",
        json={
            "name": "Apple Inc.",
            "ticker": "aapl",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "description": "Builds devices, software, and services.",
        },
    )

    assert response.status_code == 201
    assert response.json()["ticker"] == "AAPL"

    list_response = client.get("/companies")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_search_and_get_company_by_ticker(client):
    client.post(
        "/companies",
        json={
            "name": "Apple Inc.",
            "ticker": "AAPL",
            "sector": "Technology",
            "industry": "Consumer Electronics",
        },
    )
    client.post(
        "/companies",
        json={
            "name": "JPMorgan Chase & Co.",
            "ticker": "JPM",
            "sector": "Financial Services",
            "industry": "Banks",
        },
    )

    search_response = client.get("/companies/search", params={"query": "tech"})

    assert search_response.status_code == 200
    assert [company["ticker"] for company in search_response.json()] == ["AAPL"]

    ticker_response = client.get("/companies/aapl")

    assert ticker_response.status_code == 200
    assert ticker_response.json()["name"] == "Apple Inc."


def test_get_company_unknown_ticker_returns_404(client):
    response = client.get("/companies/NOPE")

    assert response.status_code == 404


def test_create_and_get_research_report(client):
    client.post(
        "/companies",
        json={"name": "Microsoft Corporation", "ticker": "MSFT", "sector": "Technology"},
    )

    create_response = client.post("/research", json={"ticker": "MSFT"})

    assert create_response.status_code == 201
    payload = create_response.json()
    assert payload["ticker"] == "MSFT"
    assert payload["summary"].startswith("Research summary for MSFT")
    assert payload["model"] == "fake-test-model"

    get_response = client.get(f"/research/{payload['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == payload["id"]


def test_research_unknown_ticker_returns_404(client):
    response = client.post("/research", json={"ticker": "NOPE"})

    assert response.status_code == 404
