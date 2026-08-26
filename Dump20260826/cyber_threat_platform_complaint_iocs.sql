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
-- Table structure for table `complaint_iocs`
--

DROP TABLE IF EXISTS `complaint_iocs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint_iocs` (
  `complaint_id` int NOT NULL,
  `ioc_id` int NOT NULL,
  PRIMARY KEY (`complaint_id`,`ioc_id`),
  KEY `ioc_id` (`ioc_id`),
  CONSTRAINT `complaint_iocs_ibfk_1` FOREIGN KEY (`complaint_id`) REFERENCES `complaints` (`complaint_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `complaint_iocs_ibfk_2` FOREIGN KEY (`ioc_id`) REFERENCES `iocs` (`ioc_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint_iocs`
--

LOCK TABLES `complaint_iocs` WRITE;
/*!40000 ALTER TABLE `complaint_iocs` DISABLE KEYS */;
INSERT INTO `complaint_iocs` VALUES (87,1),(102,2),(56,3),(38,4),(13,8),(12,9),(42,9),(15,10),(57,15),(69,15),(25,16),(9,17),(60,17),(79,17),(25,18),(38,18),(21,20),(68,23),(77,23),(102,24),(44,25),(105,25),(62,26),(93,26),(60,27),(30,28),(24,29),(62,32),(44,33),(90,33),(29,34),(39,34),(22,35),(84,35),(97,35),(69,36),(83,37),(12,38),(43,38),(55,38),(92,38),(69,39),(60,40),(103,40),(14,41),(44,41),(63,41),(102,41),(52,44),(16,45),(18,47),(15,48),(15,49),(39,49),(38,51),(98,51),(30,52),(52,52),(101,53),(15,55),(27,57),(33,57),(100,57),(53,58),(18,61),(84,61),(96,61),(18,62),(67,63),(30,64),(71,65),(22,66),(83,66),(20,67),(76,67),(60,68),(84,69),(26,71),(34,71),(37,72),(6,73),(104,73),(50,74),(68,74),(101,77),(87,78),(55,81),(56,84),(67,84),(99,84),(17,85),(85,86),(93,88),(41,89),(7,90),(96,93),(19,94),(89,94),(84,97),(54,100);
/*!40000 ALTER TABLE `complaint_iocs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:07
