"""Transformation des transactions en donnees tabulaires."""

import pandas as pd

from .core_logic import Transaction


_TYPES_TRANSACTION_RECONNUS = {"entree", "sortie"}


def convertir_en_dataframe(
	transactions: list[Transaction],
) -> pd.DataFrame:
	"""Convertit des transactions validees en DataFrame Pandas.

	Args:
		transactions: Transactions a ingerer dans le pipeline.

	Returns:
		Un DataFrame contenant les colonnes ``montant``, ``type_transaction``
		et ``date``, avec ``date`` convertie en datetime Pandas.

	Raises:
		ValueError: Si une transaction contient un type non reconnu ou une date
			invalide.
	"""
	for transaction in transactions:
		if transaction.type_transaction not in _TYPES_TRANSACTION_RECONNUS:
			raise ValueError(
				f"Type de transaction non reconnu : {transaction.type_transaction!r}"
			)

	dataframe = pd.DataFrame(
		[
			{
				"montant": transaction.montant,
				"type_transaction": transaction.type_transaction,
				"date": transaction.date,
			}
			for transaction in transactions
		],
		columns=["montant", "type_transaction", "date"],
	)
	dataframe["date"] = pd.to_datetime(dataframe["date"], errors="raise")
	return dataframe
