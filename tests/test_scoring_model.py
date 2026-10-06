"""Tests du modele de scoring financier."""

import pandas as pd
import pytest

from src.scoring_model import calculer_score_viabilite


def test_calculer_score_viabilite_calcule_totaux_solde_et_score() -> None:
	df = pd.DataFrame(
		{
			"montant": [1000.0, 400.0, 100.0],
			"type_transaction": ["entree", "sortie", "sortie"],
		}
	)

	assert calculer_score_viabilite(df) == {
		"total_entrees": 1000.0,
		"total_sorties": 500.0,
		"solde": 500.0,
		"score": 100.0,
	}


def test_calculer_score_viabilite_gere_les_sorties_nulles() -> None:
	df = pd.DataFrame(
		{"montant": [50000.0], "type_transaction": ["entree"]}
	)

	resultat = calculer_score_viabilite(df)

	assert resultat["score"] == 100.0
	assert resultat["solde"] == 50000.0


def test_calculer_score_viabilite_retire_des_points_si_sorties_superieures() -> None:
	df = pd.DataFrame(
		{
			"montant": [100.0, 200.0],
			"type_transaction": ["entree", "sortie"],
		}
	)

	assert calculer_score_viabilite(df)["score"] == 10.0


def test_calculer_score_viabilite_retourne_zero_pour_un_dataframe_vide() -> None:
	df = pd.DataFrame(columns=["montant", "type_transaction"])

	assert calculer_score_viabilite(df) == {
		"total_entrees": 0.0,
		"total_sorties": 0.0,
		"solde": 0.0,
		"score": 0.0,
	}


@pytest.mark.parametrize(
	"df",
	[
		pd.DataFrame({"montant": [-1.0], "type_transaction": ["entree"]}),
		pd.DataFrame({"montant": [None], "type_transaction": ["entree"]}),
		pd.DataFrame({"montant": ["invalide"], "type_transaction": ["entree"]}),
	],
)
def test_calculer_score_viabilite_refuse_les_montants_invalides(
	df: pd.DataFrame,
) -> None:
	with pytest.raises(ValueError, match="montant"):
		calculer_score_viabilite(df)


@pytest.mark.parametrize(
	"type_transaction",
	[None, "inconnu"],
)
def test_calculer_score_viabilite_refuse_les_types_invalides(
	type_transaction: str | None,
) -> None:
	df = pd.DataFrame({"montant": [100.0], "type_transaction": [type_transaction]})

	with pytest.raises(ValueError, match="type_transaction"):
		calculer_score_viabilite(df)


def test_calculer_score_viabilite_verifie_le_dataframe() -> None:
	with pytest.raises(TypeError, match="DataFrame"):
		calculer_score_viabilite([{"montant": 100.0}])  # type: ignore[arg-type]


def test_calculer_score_viabilite_verifie_les_colonnes_requises() -> None:
	df = pd.DataFrame({"montant": [100.0]})

	with pytest.raises(ValueError, match="type_transaction"):
		calculer_score_viabilite(df)
