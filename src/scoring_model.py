"""Calcul du score de viabilite financiere d'une boutique."""

import pandas as pd


_COLONNES_REQUISES = {"montant", "type_transaction"}


def calculer_score_viabilite(df: pd.DataFrame) -> dict[str, float]:
	"""Calcule les totaux financiers et un score de viabilite sur 100.

	Le DataFrame doit contenir les colonnes ``montant`` et
	``type_transaction``. Les types de transaction acceptes sont ``entree``
	et ``sortie`` et les montants doivent etre positifs ou nuls.

	Le score commence a 50 points. Une tresorerie positive ajoute 20 points
	et une tresorerie negative en retire 20. Le ratio entre les entrees et
	les sorties ajoute ensuite jusqu'a 30 points lorsque les entrees couvrent
	confortablement les sorties, ou retire 20 points lorsqu'elles ne les
	couvrent pas. Un DataFrame vide obtient un score de 0, car aucune activite
	financiere ne permet d'etablir une viabilite.

	Args:
		df: Transactions a analyser.

	Returns:
		Un dictionnaire contenant ``total_entrees``, ``total_sorties``,
		``solde`` et ``score``.

	Raises:
		TypeError: Si ``df`` n'est pas un DataFrame.
		ValueError: Si des colonnes sont absentes, si un type de transaction
			est inconnu ou si un montant n'est pas numerique et non negatif.
	"""
	if not isinstance(df, pd.DataFrame):
		raise TypeError("df doit etre un pandas.DataFrame")

	colonnes_manquantes = _COLONNES_REQUISES.difference(df.columns)
	if colonnes_manquantes:
		manquantes = ", ".join(sorted(colonnes_manquantes))
		raise ValueError(f"Colonnes requises absentes : {manquantes}")

	montants = pd.to_numeric(df["montant"], errors="coerce")
	if montants.isna().any() or (montants < 0).any():
		raise ValueError("La colonne 'montant' doit contenir des valeurs positives ou nulles")

	types = df["type_transaction"]
	types_inconnus = set(types.dropna().unique()).difference({"entree", "sortie"})
	if types.isna().any() or types_inconnus:
		raise ValueError("La colonne 'type_transaction' doit contenir 'entree' ou 'sortie'")

	total_entrees = float(montants[types == "entree"].sum())
	total_sorties = float(montants[types == "sortie"].sum())
	solde = total_entrees - total_sorties

	if df.empty:
		score = 0.0
	else:
		score = 50.0
		score += 20.0 if solde > 0 else -20.0 if solde < 0 else 0.0

		if total_sorties == 0:
			score += 30.0 if total_entrees > 0 else 0.0
		else:
			ratio_entrees_sorties = total_entrees / total_sorties
			if ratio_entrees_sorties >= 2:
				score += 30.0
			elif ratio_entrees_sorties >= 1.5:
				score += 20.0
			elif ratio_entrees_sorties >= 1:
				score += 10.0
			else:
				score -= 20.0

	score = max(0.0, min(100.0, score))
	return {
		"total_entrees": total_entrees,
		"total_sorties": total_sorties,
		"solde": float(solde),
		"score": float(score),
	}
