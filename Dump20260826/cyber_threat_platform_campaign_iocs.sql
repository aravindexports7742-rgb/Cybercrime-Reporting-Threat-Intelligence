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
-- Table structure for table `campaign_iocs`
--

DROP TABLE IF EXISTS `campaign_iocs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campaign_iocs` (
  `campaign_id` int NOT NULL,
  `ioc_id` int NOT NULL,
  PRIMARY KEY (`campaign_id`,`ioc_id`),
  KEY `ioc_id` (`ioc_id`),
  CONSTRAINT `campaign_iocs_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`campaign_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `campaign_iocs_ibfk_2` FOREIGN KEY (`ioc_id`) REFERENCES `iocs` (`ioc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campaign_iocs`
--

LOCK TABLES `campaign_iocs` WRITE;
/*!40000 ALTER TABLE `campaign_iocs` DISABLE KEYS */;
INSERT INTO `campaign_iocs` VALUES (56,3),(24,4),(56,6),(81,7),(17,8),(12,9),(28,9),(49,9),(38,10),(55,11),(59,11),(69,12),(14,15),(25,15),(81,15),(62,16),(17,19),(96,19),(7,23),(92,23),(36,24),(19,25),(24,27),(4,28),(41,28),(10,29),(13,29),(93,29),(76,30),(16,31),(82,31),(98,31),(41,32),(12,34),(81,34),(52,35),(29,36),(26,37),(27,37),(21,38),(96,40),(17,42),(56,44),(71,46),(3,47),(34,49),(44,50),(100,51),(4,52),(77,54),(91,54),(16,55),(51,55),(34,56),(14,58),(47,58),(64,59),(5,61),(33,61),(55,62),(26,63),(27,63),(46,64),(54,65),(42,66),(82,67),(27,68),(74,68),(11,69),(26,70),(85,70),(7,72),(11,72),(94,73),(76,75),(1,76),(58,76),(67,76),(82,78),(3,79),(13,80),(45,80),(2,83),(33,83),(94,83),(34,85),(50,86),(39,87),(52,87),(96,88),(22,91),(20,92),(67,93),(84,94),(56,96),(66,98),(49,99),(75,99),(81,99),(93,100);
/*!40000 ALTER TABLE `campaign_iocs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:10
