# DaaS Micro-Scoring

Service web de scoring financier pour les commerces locaux et informels.
L'application transforme une liste de transactions en indicateurs lisibles :
totaux des entrées et sorties, solde net et score de viabilité sur 100.

## Fonctionnalités

- calcul défensif du score financier ;
- validation des montants et des types de transactions ;
- API REST documentée automatiquement avec FastAPI ;
- interface web responsive en HTML, CSS et JavaScript ;
- affichage des montants en francs CFA (FCFA) ;
- tests unitaires et tests d'intégration de l'API ;
- exécution reproductible avec Docker.

## Architecture

```text
.
├── app.py                 # Point d'entrée FastAPI
├── frontend/
│   ├── index.html         # Interface utilisateur
│   ├── app.js             # Appels fetch et mise à jour dynamique
│   └── styles.css         # Design responsive vert et gris
├── src/
│   ├── api.py             # Routes HTTP et modèles Pydantic
│   ├── core_logic.py      # Entités métier et gestion des transactions
│   ├── data_pipeline.py   # Conversion des transactions en DataFrame
│   └── scoring_model.py   # Calcul du score de viabilité
├── tests/                 # Tests du domaine, du pipeline et de l'API
├── Dockerfile
├── .dockerignore
└── requirements.txt
```

## Règles de scoring

Le score est borné entre 0 et 100.

- score de base : 50 points ;
- trésorerie positive : +20 points ;
- trésorerie négative : -20 points ;
- ratio entrées/sorties supérieur ou égal à 2 : +30 points ;
- ratio supérieur ou égal à 1,5 : +20 points ;
- ratio supérieur ou égal à 1 : +10 points ;
- sorties supérieures aux entrées : -20 points ;
- aucune sortie : gestion explicite de la division par zéro.

Un DataFrame vide retourne un score de `0`.

## Installation locale

Pré-requis :

- Python 3.13 ou version compatible ;
- pip.

Depuis la racine du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Lancer l'application

```powershell
python -m uvicorn app:app --reload
```

L'application est alors disponible à l'adresse :

```text
http://127.0.0.1:8000
```

Documentation interactive :

- Swagger UI : `http://127.0.0.1:8000/docs`
- ReDoc : `http://127.0.0.1:8000/redoc`

## API

### Vérifier la disponibilité

```http
GET /api/health
```

Réponse :

```json
{
  "status": "ok"
}
```

### Calculer un score

```http
POST /api/score
Content-Type: application/json
```

Requête :

```json
{
  "transactions": [
    {
      "montant": 100000,
      "type_transaction": "entree"
    },
    {
      "montant": 40000,
      "type_transaction": "sortie"
    }
  ]
}
```

Réponse :

```json
{
  "total_entrees": 100000.0,
  "total_sorties": 40000.0,
  "solde": 60000.0,
  "score": 100.0
}
```

Les types acceptés sont `entree` et `sortie`. Les montants doivent être
positifs ou nuls. Les requêtes invalides retournent une erreur HTTP `422`.

## Tests

```powershell
python -m pytest tests -q
```

La suite couvre notamment :

- le calcul des totaux et du score ;
- les DataFrames vides ;
- les montants invalides ;
- les types de transactions inconnus ;
- les dates invalides du pipeline ;
- les routes de santé, de scoring et de documentation ;
- le service de fichiers frontend.

## Docker

Construire l'image :

```powershell
docker build -t daas-micro-scoring .
```

Démarrer le conteneur :

```powershell
docker run --rm -p 8000:8000 daas-micro-scoring
```

Ouvrir ensuite `http://localhost:8000`.

Le conteneur démarre l'application avec :

```text
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Choix techniques

- **FastAPI** fournit une API typée et une documentation OpenAPI automatique.
- **Pydantic** valide les payloads avant d'appeler le moteur métier.
- **Pandas** agrège les transactions dans le modèle de scoring.
- **HTML/CSS/JavaScript natif** permet une interface légère et personnalisable,
  sans dépendance à un framework de dashboard.
- **Docker** garantit un environnement d'exécution reproductible.

## Pistes d'évolution

- ajouter une persistance des boutiques et de leurs transactions ;
- intégrer une authentification et une gestion multi-utilisateur ;
- historiser les scores et afficher leur évolution ;
- ajouter une base de données et des migrations ;
- mettre en place une intégration continue avec build Docker et tests ;
- ajouter des métriques et une supervision de l'API.

## À propos

Projet conçu et développé par **Adama SANE**.
Développeur Python et Data Analyst évoluant en autodidacte, je me concentre sur la conception de solutions logicielles robustes ancrées dans l'économie réelle. Mon approche repose sur un apprentissage continu, une forte rigueur architecturale et la volonté de maîtriser toute la chaîne de valeur, de la donnée brute à l'API de production.

Retrouvez l'ensemble de mon travail technique sur mon profil : [https://github.com/AdamaSANE](https://github.com/AdamaSANE)
