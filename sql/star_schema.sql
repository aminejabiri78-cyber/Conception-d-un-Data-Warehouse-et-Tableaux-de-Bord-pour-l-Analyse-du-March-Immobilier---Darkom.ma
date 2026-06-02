CREATE SCHEMA IF NOT EXISTS star_schema_darkom;

-- DIM DATE
CREATE TABLE IF NOT EXISTS star_schema_darkom.dim_date (
    date_id SERIAL PRIMARY KEY,
    date_publication DATE,
    annee_publication INTEGER,
    mois_publication INTEGER,
    trimestre_publication INTEGER
);

-- DIM LOCATION
CREATE TABLE IF NOT EXISTS star_schema_darkom.dim_location (
    location_id SERIAL PRIMARY KEY,
    ville VARCHAR(100),
    quartier VARCHAR(255)
);

-- DIM PROPERTY
CREATE TABLE IF NOT EXISTS star_schema_darkom.dim_property (
    property_id SERIAL PRIMARY KEY,
    titre TEXT,
    type_bien VARCHAR(100),
    transaction VARCHAR(100),
    categorie_prix VARCHAR(50),
    categorie_surface VARCHAR(50),
    annee_construction INTEGER
);

-- FACT TABLE
CREATE TABLE IF NOT EXISTS star_schema_darkom.fact_darkom_listings (
    fact_id SERIAL PRIMARY KEY,

    annonce_id VARCHAR(100),

    -- foreign keys
    date_id INTEGER REFERENCES star_schema_darkom.dim_date(date_id),
    location_id INTEGER REFERENCES star_schema_darkom.dim_location(location_id),
    property_id INTEGER REFERENCES star_schema_darkom.dim_property(property_id),

    -- measures
    prix NUMERIC(14,2),
    surface NUMERIC(10,2),
    prix_m2 NUMERIC(14,2),
    age_bien INTEGER,

    nb_chambres INTEGER,
    nb_salles_bain INTEGER,
    etage INTEGER
);