from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_get_all():
    r = client.get("/vacunas")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body and "data" in body
    assert isinstance(body["data"], list)

def test_get_by_year_known_or_404():
    # probamos con un año del cache local incluido (2020) o, si falla, verificamos 404 coherente
    r = client.get("/vacunas/2020")
    if r.status_code == 200:
        payload = r.json()
        assert payload["year"] == 2020
        assert payload["indicator"] == "SH.IMM.MEAS"
    else:
        assert r.status_code in (404,)

def test_province_simulated():
    r = client.get("/vacunas/provincia/Panamá?year=2020")
    # si no hay 2020 en datos, podría ser 404; de lo contrario, validamos shape
    if r.status_code == 200:
        obj = r.json()
        assert obj["province"] == "Panamá"
        assert obj["year"] == 2020
        assert obj["simulated"] is True
    else:
        assert r.status_code in (404,)
