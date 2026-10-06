"""Tests de l'API FastAPI."""

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_health_check() -> None:
	response = client.get("/api/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok"}


def test_frontend_et_documentation_sont_accessibles() -> None:
	frontend = client.get("/")
	documentation = client.get("/openapi.json")

	assert frontend.status_code == 200
	assert "DaaS Micro-Scoring" in frontend.text
	assert "FCFA" in client.get("/static/app.js").text
	assert documentation.status_code == 200
	assert "/api/score" in documentation.json()["paths"]


def test_score_endpoint_retourne_le_resultat_metier() -> None:
	response = client.post(
		"/api/score",
		json={
			"transactions": [
				{"montant": 1000, "type_transaction": "entree"},
				{"montant": 500, "type_transaction": "sortie"},
			]
		},
	)

	assert response.status_code == 200
	assert response.json() == {
		"total_entrees": 1000.0,
		"total_sorties": 500.0,
		"solde": 500.0,
		"score": 100.0,
	}


def test_score_endpoint_refuse_un_montant_negatif() -> None:
	response = client.post(
		"/api/score",
		json={
			"transactions": [
				{"montant": -1, "type_transaction": "entree"},
			]
		},
	)

	assert response.status_code == 422


def test_score_endpoint_refuse_une_liste_vide() -> None:
	response = client.post("/api/score", json={"transactions": []})

	assert response.status_code == 422
