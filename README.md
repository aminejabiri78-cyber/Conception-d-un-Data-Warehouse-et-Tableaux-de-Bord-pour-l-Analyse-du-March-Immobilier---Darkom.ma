#  CONCEPTION-D-UN-DAT — Darkom Annonces

Projet de conception d'un **entrepôt de données** et d'un **tableau de bord Power BI** à partir des annonces immobilières du site [Darkom.ma](https://darkom.ma).

---

##  Structure du projet

```
CONCEPTION-D-UN-DAT/
│
├── data/
│   └── raw/
│       └── darkom-annonces.csv       # Données brutes extraites de Darkom
│
├── logs/
│   └── app.log                       # Journaux d'exécution
│
├── powerbi/
│   └── dash_darkom.pbix              # Tableau de bord Power BI
│
├── sql/
│   ├── clean.sql                     # Nettoyage des données
│   ├── staging.sql                   # Tables de staging
│   └── star_schema.sql               # Modèle en étoile (Data Warehouse)
│
├── src/
│   ├── extract.py                    # Extraction des données (scraping)
│   ├── clean.py                      # Nettoyage et transformation
│   ├── staging.py                    # Chargement en staging
│   ├── load_db.py                    # Chargement dans la base de données
│   ├── warhouse.py                   # Construction de l'entrepôt
│   ├── logger.py                     # Configuration des logs
│   ├── clean.ipynb                   # Notebook d'exploration nettoyage
│  
│                          # Utilitaires partagés
├── .env                              # Variables d'environnement (non versionné)
├── .gitignore
├── main.py                           # Point d'entrée principal
└── requirements.txt                  # Dépendances Python
```

---
##  Pipeline de données

```
Darkom.ma
    │
    ▼
[extract.py]  ──►  data/raw/darkom-annonces.csv
    │
    ▼
[clean.py / clean.sql]  ──►  Données nettoyées
    │
    ▼
[staging.py / staging.sql]  ──►  Tables de staging (DB)
    │
    ▼
[warhouse.py / star_schema.sql]  ──►  Entrepôt de données (schéma en étoile)
    │
    ▼
[dash_darkom.pbix]  ──►  Tableau de bord Power BI
```

---

##  Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/conception-d-un-dat.git
cd conception-d-un-dat
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=darkom_db
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
```

---

##  Utilisation

Lancer le pipeline complet :

```bash
python main.py
```

Ou exécuter les étapes individuellement :

```bash
python src/extract.py     # Extraction
python src/clean.py       # Nettoyage
python src/staging.py     # Staging
python src/warhouse.py    # Entrepôt
```

---

##  Tableau de bord Power BI

Ouvrir le fichier `powerbi/dash_darkom.pbix` avec **Power BI Desktop** pour visualiser :

- Distribution des annonces par ville / région
- Évolution des prix au m²
- Types de biens les plus fréquents
- Filtres dynamiques par superficie, prix, type

---

##  Technologies utilisées

| Outil | Usage |
|---|---|
| Python 3.x | Extraction, transformation, chargement |
| PostgreSQL / SQLite | Stockage et entrepôt de données |
| SQL | Nettoyage, staging, modèle en étoile |
| Power BI | Visualisation et tableaux de bord |
| Jupyter Notebook | Exploration et prototypage |

---

##  Logs

Les logs d'exécution sont enregistrés dans `logs/app.log`. Ils tracent chaque étape du pipeline (succès, erreurs, nombre de lignes traitées).

---

##  Contribution

Les contributions sont les bienvenues. Merci de créer une branche dédiée et de soumettre une *pull request* documentée.

---

##  Licence

Ce projet est à usage académique et éducatif.
