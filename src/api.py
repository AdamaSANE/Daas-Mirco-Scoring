"""API HTTP du service de micro-scoring."""

from pathlib import Path
from typing import Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .scoring_model import calculer_score_viabilite


class TransactionRequest(BaseModel):
	"""Transaction envoyee par un client de l'API."""

	montant: float = Field(ge=0, description="Montant positif ou nul")
	type_transaction: Literal["entree", "sortie"]


class ScoreRequest(BaseModel):
	"""Demande de calcul d'un score de viabilite."""

	transactions: list[TransactionRequest] = Field(
		min_length=1,
		description="Transactions a analyser",
	)


class ScoreResponse(BaseModel):
	"""Resultat du scoring financier."""

	total_entrees: float
	total_sorties: float
	solde: float
	score: float = Field(ge=0, le=100)


app = FastAPI(
	title="DaaS Micro-Scoring API",
	description="Service de calcul de viabilite financiere pour commerces locaux.",
	version="1.0.0",
)
app.mount(
	"/static",
	StaticFiles(directory=Path(__file__).resolve().parent.parent / "frontend"),
	name="static",
)


@app.get("/api/health", tags=["system"])
def health_check() -> dict[str, str]:
	"""Retourne l'etat de disponibilite de l'API."""
	return {"status": "ok"}


@app.post("/api/score", response_model=ScoreResponse, tags=["scoring"])
def calculate_score(request: ScoreRequest) -> ScoreResponse:
	"""Calcule le score de viabilite des transactions recues."""
	dataframe = pd.DataFrame(
		transaction.model_dump() for transaction in request.transactions
	)
	try:
		resultat = calculer_score_viabilite(dataframe)
	except (TypeError, ValueError) as error:
		raise HTTPException(status_code=422, detail=str(error)) from error
	return ScoreResponse(**resultat)


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
	"""Sert la page web principale."""
	frontend = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
	return FileResponse(frontend)
