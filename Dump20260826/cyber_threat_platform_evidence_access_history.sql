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
-- Table structure for table `evidence_access_history`
--

DROP TABLE IF EXISTS `evidence_access_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evidence_access_history` (
  `access_id` int NOT NULL AUTO_INCREMENT,
  `evidence_id` int NOT NULL,
  `user_id` int NOT NULL,
  `access_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `access_type` enum('View','Download','Analyze') NOT NULL DEFAULT 'View',
  PRIMARY KEY (`access_id`),
  KEY `evidence_id` (`evidence_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `evidence_access_history_ibfk_1` FOREIGN KEY (`evidence_id`) REFERENCES `evidence` (`evidence_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `evidence_access_history_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evidence_access_history`
--

LOCK TABLES `evidence_access_history` WRITE;
/*!40000 ALTER TABLE `evidence_access_history` DISABLE KEYS */;
INSERT INTO `evidence_access_history` VALUES (1,89,46,'2026-06-14 21:41:53','Analyze'),(2,77,36,'2026-05-05 04:44:53','Download'),(3,7,76,'2026-07-09 09:22:53','Download'),(4,23,19,'2026-07-12 11:36:53','Download'),(5,23,53,'2026-05-16 21:46:53','Analyze'),(6,23,43,'2026-07-27 07:54:53','Download'),(7,83,83,'2026-07-30 12:20:53','View'),(8,69,2,'2026-07-07 02:07:53','Analyze'),(9,43,59,'2026-06-27 22:33:53','Download'),(10,80,96,'2026-03-30 18:02:53','Analyze'),(11,43,98,'2026-04-26 14:41:53','Download'),(12,87,41,'2026-06-16 07:30:53','Download'),(13,20,59,'2026-06-22 20:48:53','View'),(14,92,65,'2026-08-19 08:32:53','View'),(15,69,13,'2026-03-06 12:08:53','Download'),(16,49,28,'2026-06-04 08:00:53','Analyze'),(17,90,51,'2026-08-06 14:31:53','Analyze'),(18,66,13,'2026-04-29 06:01:53','Analyze'),(19,55,11,'2026-04-19 03:45:53','Download'),(20,33,52,'2026-08-22 10:52:53','View'),(21,88,85,'2026-06-06 23:51:53','Download'),(22,17,20,'2026-07-11 18:37:53','Download'),(23,38,93,'2026-04-22 23:11:53','Download'),(24,75,46,'2026-04-24 08:43:53','Analyze'),(25,87,22,'2026-04-06 14:45:53','Analyze'),(26,10,94,'2026-04-05 06:47:53','View'),(27,35,35,'2026-04-21 17:55:53','Analyze'),(28,23,98,'2026-06-15 02:16:53','View'),(29,44,24,'2026-07-25 00:57:53','Analyze'),(30,56,18,'2026-03-19 01:55:53','View'),(31,74,95,'2026-05-26 22:57:53','View'),(32,32,31,'2026-06-24 04:38:53','Download'),(33,44,43,'2026-03-03 09:24:53','Download'),(34,89,92,'2026-07-14 11:45:53','Download'),(35,17,86,'2026-03-10 22:43:53','Analyze'),(36,81,37,'2026-08-20 13:49:53','Analyze'),(37,40,77,'2026-05-21 17:55:53','Download'),(38,45,51,'2026-04-23 08:35:53','Analyze'),(39,11,92,'2026-04-20 19:28:53','Analyze'),(40,98,93,'2026-03-22 02:56:53','Download'),(41,37,13,'2026-03-17 09:26:53','Analyze'),(42,19,47,'2026-06-20 11:00:53','Analyze'),(43,43,25,'2026-03-19 13:14:53','Analyze'),(44,56,51,'2026-03-28 02:02:53','View'),(45,25,44,'2026-04-26 23:06:53','Download'),(46,93,21,'2026-06-09 19:28:53','Download'),(47,21,22,'2026-04-10 02:07:53','Download'),(48,43,32,'2026-03-19 19:50:53','Analyze'),(49,13,67,'2026-07-11 11:39:53','Analyze'),(50,96,7,'2026-03-31 21:06:53','Analyze'),(51,91,90,'2026-06-18 15:45:53','Analyze'),(52,66,78,'2026-04-03 12:39:53','View'),(53,96,10,'2026-05-24 22:10:53','View'),(54,72,89,'2026-03-04 02:25:53','Download'),(55,68,77,'2026-08-09 16:06:53','Download'),(56,51,47,'2026-03-14 07:03:53','Analyze'),(57,26,29,'2026-05-15 05:12:53','View'),(58,36,18,'2026-06-25 02:50:53','Download'),(59,54,78,'2026-05-09 15:22:53','View'),(60,37,82,'2026-06-18 08:18:53','Download'),(61,80,22,'2026-04-08 06:38:53','View'),(62,65,11,'2026-08-21 10:24:53','View'),(63,82,88,'2026-06-11 09:22:53','Download'),(64,76,23,'2026-03-11 09:54:53','Analyze'),(65,14,29,'2026-07-28 17:32:53','Analyze'),(66,15,42,'2026-03-08 17:30:53','Analyze'),(67,24,13,'2026-08-03 04:41:53','View'),(68,66,77,'2026-06-02 17:32:53','Download'),(69,91,89,'2026-06-26 23:06:53','View'),(70,20,5,'2026-07-03 03:51:53','Download'),(71,24,83,'2026-08-11 20:45:53','Download'),(72,95,57,'2026-06-05 18:52:53','Download'),(73,60,31,'2026-06-16 07:56:53','Download'),(74,75,19,'2026-06-09 11:38:53','Analyze'),(75,17,69,'2026-03-10 10:35:53','Analyze'),(76,86,32,'2026-04-07 00:00:53','Analyze'),(77,95,2,'2026-03-04 08:45:53','View'),(78,41,46,'2026-08-23 23:20:53','Download'),(79,28,49,'2026-06-27 03:06:53','View'),(80,41,14,'2026-06-05 15:53:53','View'),(81,80,43,'2026-04-22 20:32:53','Download'),(82,50,60,'2026-05-10 08:27:53','View'),(83,95,35,'2026-04-19 09:57:53','Download'),(84,49,63,'2026-04-07 12:59:53','Download'),(85,83,18,'2026-08-12 15:38:53','View'),(86,92,79,'2026-03-15 08:19:53','Download'),(87,37,14,'2026-06-09 01:43:53','View'),(88,89,82,'2026-06-23 19:34:53','Analyze'),(89,13,62,'2026-03-26 14:53:53','Download'),(90,58,4,'2026-07-23 04:08:53','Analyze'),(91,44,80,'2026-06-15 06:14:53','Download'),(92,29,7,'2026-05-17 23:26:53','Analyze'),(93,63,6,'2026-08-20 18:38:53','Analyze'),(94,92,27,'2026-08-03 22:07:53','Download'),(95,95,93,'2026-08-13 23:40:53','Download'),(96,26,35,'2026-07-19 09:56:53','View'),(97,25,59,'2026-08-22 13:46:53','Download'),(98,66,86,'2026-03-06 21:12:53','View'),(99,75,12,'2026-07-09 04:01:53','Analyze'),(100,55,30,'2026-07-23 22:25:53','View');
/*!40000 ALTER TABLE `evidence_access_history` ENABLE KEYS */;
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
