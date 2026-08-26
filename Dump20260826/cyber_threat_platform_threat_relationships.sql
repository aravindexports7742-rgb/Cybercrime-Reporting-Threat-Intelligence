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
-- Table structure for table `threat_relationships`
--

DROP TABLE IF EXISTS `threat_relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threat_relationships` (
  `relationship_id` int NOT NULL AUTO_INCREMENT,
  `ioc_id_a` int NOT NULL,
  `ioc_id_b` int NOT NULL,
  `relationship_type` varchar(100) DEFAULT NULL,
  `confidence_level` enum('Low','Medium','High') NOT NULL DEFAULT 'Medium',
  PRIMARY KEY (`relationship_id`),
  KEY `ioc_id_a` (`ioc_id_a`),
  KEY `ioc_id_b` (`ioc_id_b`),
  CONSTRAINT `threat_relationships_ibfk_1` FOREIGN KEY (`ioc_id_a`) REFERENCES `iocs` (`ioc_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `threat_relationships_ibfk_2` FOREIGN KEY (`ioc_id_b`) REFERENCES `iocs` (`ioc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threat_relationships`
--

LOCK TABLES `threat_relationships` WRITE;
/*!40000 ALTER TABLE `threat_relationships` DISABLE KEYS */;
INSERT INTO `threat_relationships` VALUES (1,91,73,'communicates_with','Low'),(2,40,22,'drops','Low'),(3,53,92,'c2_for','Medium'),(4,87,29,'communicates_with','Medium'),(5,91,89,'observed_with','High'),(6,35,98,'associated_with','High'),(7,8,46,'hosted_on','High'),(8,55,62,'drops','Medium'),(9,67,6,'linked_campaign','High'),(10,90,100,'belongs_to','Low'),(11,33,23,'belongs_to','Low'),(12,63,30,'linked_campaign','High'),(13,55,69,'c2_for','Low'),(14,95,58,'drops','Low'),(15,8,85,'associated_with','Low'),(16,21,49,'observed_with','Medium'),(17,51,17,'communicates_with','High'),(18,36,51,'belongs_to','Low'),(19,75,68,'observed_with','Medium'),(20,44,39,'resolves_to','Medium'),(21,19,64,'communicates_with','Low'),(22,46,65,'belongs_to','Low'),(23,26,87,'belongs_to','Low'),(24,11,23,'observed_with','High'),(25,40,47,'belongs_to','Low'),(26,63,20,'drops','Low'),(27,94,58,'resolves_to','Low'),(28,72,19,'drops','Low'),(29,52,45,'associated_with','Low'),(30,28,74,'belongs_to','Medium'),(31,68,45,'drops','High'),(32,73,19,'c2_for','Low'),(33,77,91,'redirects_to','High'),(34,25,80,'linked_campaign','Medium'),(35,88,2,'communicates_with','Low'),(36,42,74,'linked_campaign','Medium'),(37,93,30,'drops','Low'),(38,35,63,'communicates_with','Low'),(39,85,39,'c2_for','Low'),(40,3,53,'c2_for','Medium'),(41,39,7,'hosted_on','Medium'),(42,34,77,'resolves_to','High'),(43,51,21,'linked_campaign','Low'),(44,29,12,'c2_for','Low'),(45,18,7,'linked_campaign','High'),(46,26,96,'observed_with','High'),(47,77,97,'hosted_on','Low'),(48,45,27,'redirects_to','Medium'),(49,29,93,'redirects_to','High'),(50,13,49,'c2_for','Medium'),(51,59,8,'resolves_to','Medium'),(52,27,80,'redirects_to','High'),(53,100,49,'linked_campaign','Medium'),(54,58,19,'observed_with','High'),(55,32,7,'hosted_on','Medium'),(56,94,49,'hosted_on','Medium'),(57,40,9,'drops','High'),(58,93,74,'belongs_to','Medium'),(59,91,95,'communicates_with','Low'),(60,65,32,'communicates_with','Medium'),(61,31,60,'observed_with','Medium'),(62,48,83,'associated_with','High'),(63,50,39,'belongs_to','High'),(64,81,23,'associated_with','Low'),(65,18,78,'observed_with','High'),(66,43,16,'communicates_with','Medium'),(67,8,70,'redirects_to','Medium'),(68,58,3,'c2_for','High'),(69,69,10,'hosted_on','High'),(70,26,28,'observed_with','High'),(71,76,27,'c2_for','Medium'),(72,33,26,'resolves_to','Medium'),(73,18,92,'associated_with','High'),(74,61,20,'c2_for','Medium'),(75,2,1,'redirects_to','High'),(76,2,20,'associated_with','Low'),(77,50,25,'observed_with','High'),(78,99,57,'hosted_on','Low'),(79,82,19,'hosted_on','High'),(80,90,1,'linked_campaign','Low'),(81,26,94,'resolves_to','Medium'),(82,51,12,'belongs_to','Medium'),(83,71,45,'associated_with','Medium'),(84,11,30,'hosted_on','High'),(85,1,60,'redirects_to','High'),(86,66,63,'drops','Medium'),(87,66,81,'observed_with','Low'),(88,27,30,'communicates_with','Medium'),(89,70,31,'c2_for','High'),(90,85,65,'belongs_to','Low'),(91,66,48,'c2_for','High'),(92,35,42,'redirects_to','Medium'),(93,51,86,'c2_for','Medium'),(94,79,10,'resolves_to','High'),(95,9,99,'belongs_to','Low'),(96,97,66,'linked_campaign','Medium'),(97,12,78,'observed_with','Medium'),(98,62,28,'observed_with','High'),(99,26,20,'belongs_to','Low'),(100,71,53,'resolves_to','Medium');
/*!40000 ALTER TABLE `threat_relationships` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:05
