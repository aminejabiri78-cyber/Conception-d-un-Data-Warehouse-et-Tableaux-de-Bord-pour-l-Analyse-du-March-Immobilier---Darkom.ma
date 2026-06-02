CREATE SCHEMA IF NOT EXISTS schema_clean_darkom;

CREATE TABLE IF NOT EXISTS schema_clean_darkom.darkom_clean (

    annonce_id VARCHAR(100) PRIMARY KEY,

    date_publication TIMESTAMP,

    titre TEXT,

    prix NUMERIC(14,2),

    surface NUMERIC(10,2),

    nb_chambres INTEGER,

    nb_salles_bain INTEGER,

    etage INTEGER,

    annee_construction INTEGER,

    quartier VARCHAR(255),

    type_bien VARCHAR(100),

    transaction VARCHAR(100),

    ville VARCHAR(100),

    prix_m2 NUMERIC(14,2),

    age_bien INTEGER,

    categorie_prix VARCHAR(50),

    categorie_surface VARCHAR(50),

    annee_publication INTEGER,

    mois_publication INTEGER,

    trimestre_publication INTEGER

);