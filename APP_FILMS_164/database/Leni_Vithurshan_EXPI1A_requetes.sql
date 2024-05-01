-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.30 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour lenimoras_vithurshan_expi1a_gestion_visiteur
DROP DATABASE IF EXISTS `lenimoras_vithurshan_expi1a_gestion_visiteur`;
CREATE DATABASE IF NOT EXISTS `lenimoras_vithurshan_expi1a_gestion_visiteur` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `lenimoras_vithurshan_expi1a_gestion_visiteur`;

-- Listage de la structure de table lenimoras_vithurshan_expi1a_gestion_visiteur. t_annulation
DROP TABLE IF EXISTS `t_annulation`;
CREATE TABLE IF NOT EXISTS `t_annulation` (
  `ID_Annulation` int NOT NULL,
  `Date_d_Annulation` date DEFAULT NULL,
  `Motif_de_l_Annulation` varchar(255) DEFAULT NULL,
  `ID_Visite` int DEFAULT NULL,
  PRIMARY KEY (`ID_Annulation`),
  KEY `ID_Visite` (`ID_Visite`),
  CONSTRAINT `t_annulation_ibfk_1` FOREIGN KEY (`ID_Visite`) REFERENCES `t_visite` (`ID_Visite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table lenimoras_vithurshan_expi1a_gestion_visiteur.t_annulation : ~3 rows (environ)
INSERT INTO `t_annulation` (`ID_Annulation`, `Date_d_Annulation`, `Motif_de_l_Annulation`, `ID_Visite`) VALUES
	(1, '2024-03-04', 'Urgent meeting came up', 4),
	(2, '2024-03-06', 'Visitor fell ill', 6),
	(3, '2024-03-09', 'Unforeseen circumstances', 9);

-- Listage de la structure de table lenimoras_vithurshan_expi1a_gestion_visiteur. t_personnecontact
DROP TABLE IF EXISTS `t_personnecontact`;
CREATE TABLE IF NOT EXISTS `t_personnecontact` (
  `ID_PersonneContact` int NOT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  `Numero_de_Telephone_Interne` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_PersonneContact`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table lenimoras_vithurshan_expi1a_gestion_visiteur.t_personnecontact : ~10 rows (environ)
INSERT INTO `t_personnecontact` (`ID_PersonneContact`, `Nom`, `Numero_de_Telephone_Interne`) VALUES
	(1, 'Johnson', '1234'),
	(2, 'Smith', '5678'),
	(3, 'Williams', '9101'),
	(4, 'Brown', '1121'),
	(5, 'Davis', '3141'),
	(6, 'Miller', '5161'),
	(7, 'Wilson', '7181'),
	(8, 'Moore', '9202'),
	(9, 'Taylor', '2232'),
	(10, 'Anderson', '4242');

-- Listage de la structure de table lenimoras_vithurshan_expi1a_gestion_visiteur. t_societe
DROP TABLE IF EXISTS `t_societe`;
CREATE TABLE IF NOT EXISTS `t_societe` (
  `ID_Societe` int NOT NULL,
  `Nom_de_la_Societe` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_Societe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table lenimoras_vithurshan_expi1a_gestion_visiteur.t_societe : ~10 rows (environ)
INSERT INTO `t_societe` (`ID_Societe`, `Nom_de_la_Societe`) VALUES
	(1, 'ABC Company'),
	(2, 'XYZ Corporation'),
	(3, 'LMN Enterprises'),
	(4, '123 Industries'),
	(5, 'PQR Ltd'),
	(6, 'EFG Group'),
	(7, 'UVW Inc'),
	(8, 'RST Co'),
	(9, 'GHI Ltd'),
	(10, 'JKL Enterprises');

-- Listage de la structure de table lenimoras_vithurshan_expi1a_gestion_visiteur. t_visite
DROP TABLE IF EXISTS `t_visite`;
CREATE TABLE IF NOT EXISTS `t_visite` (
  `ID_Visite` int NOT NULL,
  `Date_de_Visite` date DEFAULT NULL,
  `Heure_d_Arrivee_Prevue` time DEFAULT NULL,
  `Heure_d_Arrivee_Reelle` time DEFAULT NULL,
  `Duree` int DEFAULT NULL,
  `Heure_de_Depart` time DEFAULT NULL,
  `Motif_de_Visite` varchar(255) DEFAULT NULL,
  `Frequence_de_visites` varchar(50) DEFAULT NULL,
  `Nom_du_Batiment` varchar(255) DEFAULT NULL,
  `ID_Visiteur` int DEFAULT NULL,
  `ID_PersonneContact` int DEFAULT NULL,
  PRIMARY KEY (`ID_Visite`),
  KEY `ID_Visiteur` (`ID_Visiteur`),
  KEY `ID_PersonneContact` (`ID_PersonneContact`),
  CONSTRAINT `t_visite_ibfk_1` FOREIGN KEY (`ID_Visiteur`) REFERENCES `t_visiteur` (`ID_Visiteur`),
  CONSTRAINT `t_visite_ibfk_2` FOREIGN KEY (`ID_PersonneContact`) REFERENCES `t_personnecontact` (`ID_PersonneContact`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table lenimoras_vithurshan_expi1a_gestion_visiteur.t_visite : ~10 rows (environ)
INSERT INTO `t_visite` (`ID_Visite`, `Date_de_Visite`, `Heure_d_Arrivee_Prevue`, `Heure_d_Arrivee_Reelle`, `Duree`, `Heure_de_Depart`, `Motif_de_Visite`, `Frequence_de_visites`, `Nom_du_Batiment`, `ID_Visiteur`, `ID_PersonneContact`) VALUES
	(1, '2024-03-01', '08:00:00', '08:15:00', 60, '09:15:00', 'Meeting', 'Mensuel', 'Building A', 1, 1),
	(2, '2024-03-02', '10:30:00', '10:45:00', 45, '11:30:00', 'Interview', 'Ponctuel', 'Building B', 2, 2),
	(3, '2024-03-03', '09:00:00', '09:10:00', 30, '09:40:00', 'Training', 'Hebdomadaire', 'Building C', 3, 3),
	(4, '2024-03-04', '13:45:00', NULL, NULL, NULL, 'Presentation', 'Bimensuel', 'Building D', 4, 4),
	(5, '2024-03-05', '11:15:00', '11:30:00', 60, '12:30:00', 'Consultation', 'Trimestriel', 'Building E', 5, 5),
	(6, '2024-03-06', '14:00:00', NULL, NULL, NULL, 'Audit', 'Mensuel', 'Building F', 6, 6),
	(7, '2024-03-07', '10:00:00', '10:20:00', 40, '11:00:00', 'Discussion', 'Ponctuel', 'Building G', 7, 7),
	(8, '2024-03-08', '08:30:00', '08:45:00', 60, '09:45:00', 'Training', 'Hebdomadaire', 'Building H', 8, 8),
	(9, '2024-03-09', '12:00:00', NULL, NULL, NULL, 'Meeting', 'Mensuel', 'Building I', 9, 9),
	(10, '2024-03-10', '09:45:00', '10:00:00', 30, '10:30:00', 'Interview', 'Ponctuel', 'Building J', 10, 10);

-- Listage de la structure de table lenimoras_vithurshan_expi1a_gestion_visiteur. t_visiteur
DROP TABLE IF EXISTS `t_visiteur`;
CREATE TABLE IF NOT EXISTS `t_visiteur` (
  `ID_Visiteur` int NOT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  `Prenom` varchar(255) DEFAULT NULL,
  `Adresse` varchar(255) DEFAULT NULL,
  `Date_de_Naissance` date DEFAULT NULL,
  `Numero_de_Telephone` varchar(20) DEFAULT NULL,
  `ID_Societe` int DEFAULT NULL,
  `Le_Visiteur_se_deplace_en_Vehicule_Personnel` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`ID_Visiteur`),
  KEY `ID_Societe` (`ID_Societe`),
  CONSTRAINT `t_visiteur_ibfk_1` FOREIGN KEY (`ID_Societe`) REFERENCES `t_societe` (`ID_Societe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table lenimoras_vithurshan_expi1a_gestion_visiteur.t_visiteur : ~10 rows (environ)
INSERT INTO `t_visiteur` (`ID_Visiteur`, `Nom`, `Prenom`, `Adresse`, `Date_de_Naissance`, `Numero_de_Telephone`, `ID_Societe`, `Le_Visiteur_se_deplace_en_Vehicule_Personnel`) VALUES
	(1, 'Doe', 'John', '10 Rue de Lausanne, 1001 Lausanne', '1990-05-15', '076-123-456', 1, 'non'),
	(2, 'Smith', 'Emily', '15 Avenue de Mont-Blanc, 1202 Genève', '1988-09-20', '077-987-654', 2, 'oui'),
	(3, 'Johnson', 'Michael', '5 Rue du Rhône, 3000 Bern', '1995-02-10', '078-555-123', 3, 'non'),
	(4, 'Williams', 'Sarah', '8 Quai des Bergues, 1800 Vevey', '1985-11-25', '079-777-888', 1, 'oui'),
	(5, 'Brown', 'Jessica', '3 Rue du Marché, 74200 Thonon-les-Bains, France', '1992-07-12', '076-111-222', 4, 'non'),
	(6, 'Davis', 'David', '18 Rue du Stand, 1820 Montreux', '1998-03-30', '077-999-888', 2, 'oui'),
	(7, 'Miller', 'Jennifer', '25 Rue du Rhône, 1003 Lausanne', '1980-12-05', '078-444-555', 5, 'non'),
	(8, 'Wilson', 'James', '7 Rue du Mont-Blanc, 1202 Genève', '1991-08-18', '079-333-222', 3, 'oui'),
	(9, 'Moore', 'Amy', '12 Rue du Cendrier, 1004 Lausanne', '1987-04-22', '076-666-777', 2, 'non'),
	(10, 'Taylor', 'Robert', '30 Quai Gustave-Ador, 1207 Genève', '1993-10-07', '077-888-999', 4, 'oui');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
