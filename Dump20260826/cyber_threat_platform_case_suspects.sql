-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: cyber_threat_platform
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `case_suspects`
--

DROP TABLE IF EXISTS `case_suspects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `case_suspects` (
  `case_id` int NOT NULL,
  `suspect_id` int NOT NULL,
  PRIMARY KEY (`case_id`,`suspect_id`),
  KEY `suspect_id` (`suspect_id`),
  CONSTRAINT `case_suspects_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `cases` (`case_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `case_suspects_ibfk_2` FOREIGN KEY (`suspect_id`) REFERENCES `suspects` (`suspect_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_suspects`
--

LOCK TABLES `case_suspects` WRITE;
/*!40000 ALTER TABLE `case_suspects` DISABLE KEYS */;
INSERT INTO `case_suspects` VALUES (3,1),(41,3),(20,5),(21,5),(43,6),(71,6),(81,6),(88,6),(57,7),(23,9),(97,9),(4,11),(22,12),(48,12),(25,13),(26,13),(60,14),(15,15),(25,15),(92,15),(96,16),(20,17),(53,18),(56,18),(6,19),(48,21),(2,22),(54,22),(87,23),(93,24),(29,25),(1,26),(70,27),(32,28),(96,28),(63,29),(1,31),(69,31),(28,32),(30,35),(45,35),(19,36),(49,36),(51,37),(87,37),(23,38),(38,39),(13,42),(74,42),(44,43),(100,43),(88,44),(31,48),(48,50),(74,52),(9,54),(96,54),(100,55),(6,56),(46,56),(59,57),(18,58),(22,59),(58,59),(23,60),(69,61),(95,61),(12,63),(81,63),(13,64),(36,64),(61,64),(53,65),(19,68),(46,69),(3,72),(20,73),(77,74),(87,75),(42,76),(38,79),(48,79),(93,79),(91,80),(92,81),(95,81),(46,83),(33,84),(37,88),(2,89),(43,93),(7,95),(29,95),(99,95),(100,96),(32,97),(22,98),(51,98),(26,100),(63,100);
/*!40000 ALTER TABLE `case_suspects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:09
