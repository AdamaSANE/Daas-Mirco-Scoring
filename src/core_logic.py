"""Logique metier principale de la boutique."""

from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class Transaction:
	"""Represente une transaction realisee par la boutique."""

	montant: float
	type_transaction: str
	date: str


class GestionnaireBoutique:
	"""Gere les transactions associees a une boutique."""

	def __init__(self, nom_boutique: str, id_boutique: str | None = None) -> None:
		"""Initialise un gestionnaire pour la boutique indiquee.

		Args:
			nom_boutique: Nom de la boutique geree.
			id_boutique: Identifiant unique fourni ou genere automatiquement.
		"""
		self.nom_boutique: str = nom_boutique
		self.id_boutique: str = id_boutique or str(uuid.uuid4())
		self.transactions: list[Transaction] = []

	def ajouter_transaction(
		self,
		montant: float,
		type_transaction: str,
		date: str,
	) -> None:
		"""Ajoute une transaction a l'historique de la boutique.

		Args:
			montant: Montant de la transaction.
			type_transaction: Nature de la transaction, par exemple ``entree`` ou ``sortie``.
			date: Date de la transaction au format texte convenu par l'application.
		"""
		self.transactions.append(Transaction(montant, type_transaction, date))
