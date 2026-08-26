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
-- Table structure for table `incident_activities`
--

DROP TABLE IF EXISTS `incident_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incident_activities` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `incident_id` int NOT NULL,
  `performed_by` int DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `activity_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`activity_id`),
  KEY `incident_id` (`incident_id`),
  KEY `performed_by` (`performed_by`),
  CONSTRAINT `incident_activities_ibfk_1` FOREIGN KEY (`incident_id`) REFERENCES `incidents` (`incident_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `incident_activities_ibfk_2` FOREIGN KEY (`performed_by`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incident_activities`
--

LOCK TABLES `incident_activities` WRITE;
/*!40000 ALTER TABLE `incident_activities` DISABLE KEYS */;
INSERT INTO `incident_activities` VALUES (1,41,76,'System Reimaged','2026-05-20 23:24:54'),(2,71,43,'Initial Triage','2026-08-26 01:20:54'),(3,98,83,'Containment Action','2026-07-31 19:27:54'),(4,92,63,'Firewall Rule Updated','2026-06-28 23:16:54'),(5,10,47,'Incident Detected','2026-08-10 20:50:54'),(6,83,26,'Case Closed','2026-06-10 14:56:54'),(7,94,76,'Malware Quarantined','2026-06-01 02:30:54'),(8,27,52,'Containment Action','2026-08-04 02:57:54'),(9,34,6,'Password Reset','2026-07-16 02:39:54'),(10,28,87,'Alert Triggered','2026-07-11 13:17:54'),(11,11,69,'Network Isolated','2026-07-26 07:14:54'),(12,11,51,'Initial Triage','2026-05-25 07:39:54'),(13,75,78,'Case Closed','2026-07-22 00:50:54'),(14,88,8,'Scope Assessment','2026-04-30 12:27:54'),(15,8,74,'Password Reset','2026-08-21 09:59:54'),(16,86,20,'Initial Triage','2026-06-09 12:39:54'),(17,96,30,'System Reimaged','2026-05-26 09:58:54'),(18,5,89,'Containment Action','2026-07-03 00:18:54'),(19,45,89,'Containment Action','2026-05-25 15:32:54'),(20,90,78,'Alert Triggered','2026-05-17 05:43:54'),(21,97,71,'Patch Applied','2026-06-21 18:25:54'),(22,77,48,'Forensic Copy Made','2026-08-20 00:43:54'),(23,17,15,'Forensic Copy Made','2026-04-28 23:02:54'),(24,61,48,'Forensic Copy Made','2026-08-03 03:47:54'),(25,65,24,'Patch Applied','2026-07-06 06:36:54'),(26,12,37,'Incident Detected','2026-07-05 06:18:54'),(27,34,22,'Initial Triage','2026-07-22 03:50:54'),(28,68,16,'Malware Quarantined','2026-08-14 05:05:54'),(29,21,58,'Malware Quarantined','2026-07-29 09:40:54'),(30,12,63,'Management Escalated','2026-06-09 21:42:54'),(31,34,16,'Patch Applied','2026-07-14 18:55:54'),(32,17,72,'Incident Detected','2026-07-14 01:59:54'),(33,69,79,'Initial Triage','2026-06-27 12:48:54'),(34,55,45,'Management Escalated','2026-08-04 14:55:54'),(35,94,56,'Incident Detected','2026-06-02 18:14:54'),(36,100,11,'System Reimaged','2026-07-13 10:06:54'),(37,61,44,'Malware Quarantined','2026-07-19 02:31:54'),(38,47,85,'User Notified','2026-06-28 12:10:54'),(39,95,81,'Initial Triage','2026-06-08 00:43:54'),(40,57,70,'Forensic Copy Made','2026-08-24 02:44:54'),(41,61,11,'Scope Assessment','2026-07-08 19:11:54'),(42,87,88,'Firewall Rule Updated','2026-08-11 08:54:54'),(43,58,15,'Alert Triggered','2026-06-14 03:08:54'),(44,35,97,'Forensic Copy Made','2026-05-23 23:44:54'),(45,29,98,'Forensic Copy Made','2026-07-29 22:22:54'),(46,68,40,'Malware Quarantined','2026-05-20 00:39:54'),(47,6,23,'Case Closed','2026-05-30 15:31:54'),(48,5,77,'System Reimaged','2026-06-18 18:54:54'),(49,60,56,'Password Reset','2026-05-21 22:01:54'),(50,76,82,'Case Closed','2026-05-07 06:54:54'),(51,12,1,'System Reimaged','2026-05-12 01:31:54'),(52,10,21,'Initial Triage','2026-05-31 08:55:54'),(53,54,21,'Network Isolated','2026-07-03 23:07:54'),(54,5,18,'Patch Applied','2026-07-29 07:40:54'),(55,95,38,'Alert Triggered','2026-06-10 17:33:54'),(56,29,6,'Malware Quarantined','2026-06-09 05:09:54'),(57,49,14,'Password Reset','2026-05-31 09:56:54'),(58,21,89,'Patch Applied','2026-05-04 15:55:54'),(59,43,41,'Firewall Rule Updated','2026-08-02 06:50:54'),(60,86,61,'Firewall Rule Updated','2026-07-27 06:49:54'),(61,7,10,'Malware Quarantined','2026-08-10 03:15:54'),(62,27,12,'Patch Applied','2026-06-27 22:04:54'),(63,84,88,'Password Reset','2026-07-27 06:50:54'),(64,80,17,'Alert Triggered','2026-05-15 16:26:54'),(65,63,82,'Scope Assessment','2026-06-27 13:15:54'),(66,18,89,'Incident Detected','2026-05-30 14:53:54'),(67,2,94,'Firewall Rule Updated','2026-07-08 09:29:54'),(68,34,35,'Case Closed','2026-05-26 19:12:54'),(69,7,100,'Patch Applied','2026-06-04 18:34:54'),(70,27,79,'Password Reset','2026-05-12 13:16:54'),(71,13,55,'Firewall Rule Updated','2026-05-12 12:30:54'),(72,31,2,'Network Isolated','2026-05-26 19:39:54'),(73,36,79,'Network Isolated','2026-05-18 09:13:54'),(74,25,35,'Forensic Copy Made','2026-05-12 17:31:54'),(75,9,61,'Initial Triage','2026-07-10 22:37:54'),(76,67,66,'Case Closed','2026-07-25 21:06:54'),(77,97,51,'Malware Quarantined','2026-06-04 14:15:54'),(78,79,58,'Password Reset','2026-05-22 04:31:54'),(79,97,92,'Containment Action','2026-05-29 21:58:54'),(80,76,54,'Containment Action','2026-06-15 03:41:54'),(81,28,96,'Initial Triage','2026-08-07 20:01:54'),(82,27,25,'Case Closed','2026-07-09 17:56:54'),(83,7,50,'Containment Action','2026-04-27 14:09:54'),(84,49,16,'Containment Action','2026-06-26 13:51:54'),(85,71,50,'Initial Triage','2026-05-22 14:11:54'),(86,25,88,'Containment Action','2026-05-09 00:03:54'),(87,5,27,'Incident Detected','2026-05-10 05:42:54'),(88,30,66,'Patch Applied','2026-08-25 03:56:54'),(89,20,41,'Management Escalated','2026-05-06 19:54:54'),(90,32,8,'Case Closed','2026-08-05 00:38:54'),(91,33,83,'Firewall Rule Updated','2026-06-23 01:46:54'),(92,86,30,'Firewall Rule Updated','2026-04-29 20:38:54'),(93,38,44,'Password Reset','2026-08-03 20:22:54'),(94,87,3,'User Notified','2026-08-18 02:05:54'),(95,46,12,'Scope Assessment','2026-08-07 03:41:54'),(96,74,63,'Forensic Copy Made','2026-08-10 16:07:54'),(97,73,13,'Password Reset','2026-06-14 15:21:54'),(98,19,89,'Firewall Rule Updated','2026-05-13 19:22:54'),(99,64,69,'Scope Assessment','2026-07-10 15:17:54'),(100,23,14,'Alert Triggered','2026-07-14 20:15:54');
/*!40000 ALTER TABLE `incident_activities` ENABLE KEYS */;
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
