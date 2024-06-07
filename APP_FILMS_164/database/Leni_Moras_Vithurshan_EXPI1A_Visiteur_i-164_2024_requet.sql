-- table t_visiteur:
SELECT * FROM t_visiteur;
SELECT * FROM t_visiteur WHERE ID_Visiteur = 1;
SELECT * FROM t_visiteur ORDER BY ID_Visiteur DESC;
SELECT * FROM t_visiteur ORDER BY ID_Visiteur DESC;
INSERT INTO t_visiteur (Nom, Prenom, Adresse, Date_de_Naissance, Numero_de_Telephone, Le_Visiteur_se_deplace_en_Vehicule_Personnel)
VALUES ('Dupont', 'Jean', '123 rue de Paris', '1990-01-01', '0123456789', true);
UPDATE t_visiteur
SET Nom = 'Martin', Prenom = 'Lucie', Adresse = '456 avenue de la Liberté', Date_de_Naissance = '1992-02-02', Numero_de_Telephone = '9876543210', Le_Visiteur_se_deplace_en_Vehicule_Personnel = false
WHERE ID_Visiteur = 1;
DELETE FROM t_visiteur WHERE ID_Visiteur = 1;


-- table t_ societe
SELECT * FROM t_societe;
SELECT * FROM t_societe WHERE ID_Societe = 1;
SELECT * FROM t_societe ORDER BY ID_Societe DESC;
INSERT INTO t_societe (Nom_de_la_Societe)
VALUES ('Nom de la Nouvelle Société');
UPDATE t_societe
SET Nom_de_la_Societe = 'Nouveau Nom de la Société'
WHERE ID_Societe = 1;
SELECT ID_Societe, Nom_de_la_Societe FROM t_societe WHERE ID_Societe = 1;
DELETE FROM t_societe WHERE ID_Societe = 1;
SELECT t_visiteur_societe.ID_visiteur_societe, t_visiteur.Nom, t_visiteur.Prenom, t_societe.Nom_de_la_Societe
FROM t_visiteur_societe
INNER JOIN t_visiteur ON t_visiteur_societe.FK_visiteur = t_visiteur.ID_Visiteur
INNER JOIN t_societe ON t_visiteur_societe.FK_societe = t_societe.ID_Societe
WHERE FK_societe = 1;


-- table t_visiteur_societe
-- Requête pour récupérer les détails de tous les visiteurs et concaténer les noms des sociétés associées à chaque visiteur
SELECT
    t_visiteur.ID_Visiteur,
    t_visiteur.Nom,
    t_visiteur.Prenom,
    t_visiteur.Adresse,
    t_visiteur.Date_de_Naissance,
    t_visiteur.Numero_de_Telephone,
    t_visiteur.Le_Visiteur_se_deplace_en_Vehicule_Personnel,
    GROUP_CONCAT(t_societe.Nom_de_la_Societe) as Societes
FROM t_visiteur_societe
RIGHT JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
LEFT JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
GROUP BY t_visiteur.ID_Visiteur;

-- Affiche les détails d'un visiteur spécifique et les sociétés associées à ce visiteur.
SELECT
    t_visiteur.ID_Visiteur,
    t_visiteur.Nom,
    t_visiteur.Prenom,
    t_visiteur.Adresse,
    t_visiteur.Date_de_Naissance,
    t_visiteur.Numero_de_Telephone,
    t_visiteur.Le_Visiteur_se_deplace_en_Vehicule_Personnel,
    GROUP_CONCAT(t_societe.Nom_de_la_Societe) as Societes
FROM t_visiteur_societe
RIGHT JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
LEFT JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
WHERE t_visiteur.ID_Visiteur = 1
GROUP BY t_visiteur.ID_Visiteur;

-- Sélectionne les sociétés qui ne sont pas encore associées à un visiteur spécifique.
SELECT ID_Societe, Nom_de_la_Societe
FROM t_societe
WHERE ID_Societe NOT IN (
    SELECT ID_Societe
    FROM t_visiteur_societe
    INNER JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
    INNER JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
    WHERE ID_Visiteur = 1
);

-- Sélectionne les sociétés déjà associées à un visiteur spécifique.
SELECT ID_Visiteur, ID_Societe, Nom_de_la_Societe
FROM t_visiteur_societe
INNER JOIN t_visiteur ON t_visiteur.ID_Visiteur = t_visiteur_societe.FK_visiteur
INNER JOIN t_societe ON t_societe.ID_Societe = t_visiteur_societe.FK_societe
WHERE ID_Visiteur = 1;

-- Supprime une association existante entre un visiteur et une société.
DELETE FROM t_visiteur_societe
WHERE FK_societe = ID_Societe AND FK_visiteur = ID_Visiteur;


-- Insère une nouvelle association entre un visiteur et une société.
INSERT INTO t_visiteur_societe (FK_societe, FK_visiteur)
VALUES (ID_Societe, ID_Visiteur);



-- table visite:
-- Affiche toutes les visites en ordre ascendant ou descendant

SELECT * FROM t_visite ORDER BY ID_Visite ASC;

-- Affiche les détails d'une visite spécifique par son ID
SELECT * FROM t_visite WHERE ID_Visite = 1;


-- Sélectionne toutes les visites dans la table t_visite, triées par ID de manière descendante
SELECT * FROM t_visite ORDER BY ID_Visite DESC;

-- Insère une nouvelle visite dans la table t_visite
-- Remplacez les valeurs entre guillemets par les valeurs appropriées
INSERT INTO t_visite (
    Date_de_Visite,
    Heure_d_Arrivee_Prevue,
    Heure_d_Arrivee_Reelle,
    Duree,
    Heure_de_Depart,
    Motif_de_Visite,
    Frequence_de_visites,
    Nom_du_Batiment
) VALUES (
    '2024-06-07',      -- Date de la visite
    '10:00:00',        -- Heure d'arrivée prévue
    '10:15:00',        -- Heure d'arrivée réelle
    '2:00:00',         -- Durée de la visite
    '12:15:00',        -- Heure de départ
    'Motif',           -- Motif de la visite
    'Hebdomadaire',    -- Fréquence des visites
    'Bâtiment A'       -- Nom du bâtiment
);

-- Met à jour les détails d'une visite existante
-- Remplacez les valeurs entre guillemets par les valeurs appropriées
-- et remplacez `1` par l'ID de la visite à mettre à jour
UPDATE t_visite
SET
    Date_de_Visite = '2024-06-08',
    Heure_d_Arrivee_Prevue = '11:00:00',
    Heure_d_Arrivee_Reelle = '11:15:00',
    Duree = '1:30:00',
    Heure_de_Depart = '12:45:00',
    Motif_de_Visite = 'Réunion',
    Frequence_de_visites = 'Mensuelle',
    Nom_du_Batiment = 'Bâtiment B'
WHERE
    ID_Visite = 1;  -- ID de la visite à mettre à jour
-- Supprime les enregistrements d'annulation de visite liés à un visiteur spécifique
-- Remplacez `1` par l'ID du visiteur
DELETE FROM t_annulation_visite
WHERE
    FK_visite IN (
        SELECT
            ID_Visite
        FROM
            t_visite
        WHERE
            ID_Visite IN (
                SELECT
                    FK_visite
                FROM
                    t_visiteur_visite
                WHERE
                    FK_visiteur = 1  -- ID du visiteur
            )
    );
-- Supprime les enregistrements de contact de visite liés à un visiteur spécifique
-- Remplacez `1` par l'ID du visiteur
DELETE FROM t_visite_contact
WHERE
    FK_visite IN (
        SELECT
            ID_Visite
        FROM
            t_visite
        WHERE
            ID_Visite IN (
                SELECT
                    FK_visite
                FROM
                    t_visiteur_visite
                WHERE
                    FK_visiteur = 1  -- ID du visiteur
            )
    );
-- Sélectionne les sociétés attribuées à un visiteur spécifique
-- Remplacez `1` par l'ID du visiteur
SELECT
    t_visiteur_societe.ID_visiteur_societe,
    t_visiteur.Nom,
    t_visiteur.Prenom,
    t_visiteur.ID_Visiteur,
    t_visiteur.Adresse,
    t_societe.Nom_de_la_Societe
FROM
    t_visiteur_societe
INNER JOIN
    t_visiteur ON t_visiteur_societe.FK_visiteur = t_visiteur.ID_Visiteur
INNER JOIN
    t_societe ON t_visiteur_societe.FK_societe = t_societe.ID_Societe
WHERE
    FK_visiteur = 1;  -- ID du visiteur
