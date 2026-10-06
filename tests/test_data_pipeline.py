"""Tests du pipeline de transformation des transactions."""

import pandas as pd
import pytest

from src.core_logic import Transaction
from src.data_pipeline import convertir_en_dataframe


def test_convertir_en_dataframe_convertit_les_transactions() -> None:
	transactions = [
		Transaction(500.0, "entree", "2026-01-15"),
		Transaction(125.0, "sortie", "2026-01-16"),
	]

	resultat = convertir_en_dataframe(transactions)

	assert list(resultat.columns) == ["montant", "type_transaction", "date"]
	assert resultat["montant"].tolist() == [500.0, 125.0]
	assert resultat["type_transaction"].tolist() == ["entree", "sortie"]
	assert pd.api.types.is_datetime64_any_dtype(resultat["date"])


def test_convertir_en_dataframe_refuse_un_type_inconnu() -> None:
	transactions = [Transaction(100.0, "remboursement", "2026-01-15")]

	with pytest.raises(ValueError, match="Type de transaction non reconnu"):
		convertir_en_dataframe(transactions)


def test_convertir_en_dataframe_refuse_une_date_invalide() -> None:
	transactions = [Transaction(100.0, "entree", "date invalide")]

	with pytest.raises(ValueError):
		convertir_en_dataframe(transactions)
