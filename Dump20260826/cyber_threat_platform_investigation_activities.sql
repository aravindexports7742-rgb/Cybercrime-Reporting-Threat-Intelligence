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
-- Table structure for table `investigation_activities`
--

DROP TABLE IF EXISTS `investigation_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `investigation_activities` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `case_id` int NOT NULL,
  `officer_id` int NOT NULL,
  `action` varchar(255) NOT NULL,
  `result` varchar(255) DEFAULT NULL,
  `activity_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`activity_id`),
  KEY `case_id` (`case_id`),
  KEY `officer_id` (`officer_id`),
  CONSTRAINT `investigation_activities_ibfk_1` FOREIGN KEY (`case_id`) REFERENCES `cases` (`case_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `investigation_activities_ibfk_2` FOREIGN KEY (`officer_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `investigation_activities`
--

LOCK TABLES `investigation_activities` WRITE;
/*!40000 ALTER TABLE `investigation_activities` DISABLE KEYS */;
INSERT INTO `investigation_activities` VALUES (1,61,37,'Financial Trace','Lead inconclusive','2026-06-05 06:39:53'),(2,64,7,'Witness Statement','Under review','2026-04-15 09:03:53'),(3,62,84,'Network Log Analysis','Suspect identified','2026-05-26 10:24:53'),(4,71,25,'Victim Interview','Suspect identified','2026-03-16 22:59:53'),(5,5,15,'Search Warrant Executed','Lead inconclusive','2026-03-30 08:54:53'),(6,34,5,'OSINT Research','Completed successfully','2026-03-02 17:10:53'),(7,56,9,'Digital Forensics','Evidence secured','2026-04-21 09:36:53'),(8,27,32,'Forensic Report Filed','Positive lead found','2026-08-11 00:38:53'),(9,37,95,'ISP Contacted','No new information','2026-07-24 21:05:53'),(10,89,73,'Search Warrant Executed','Forwarded to legal team','2026-05-05 13:07:53'),(11,10,95,'Suspect Arrested','Forwarded to legal team','2026-02-22 08:03:53'),(12,35,50,'Witness Statement','Completed successfully','2026-04-05 02:45:53'),(13,31,50,'Digital Forensics','Evidence secured','2026-04-09 00:59:53'),(14,64,47,'Network Log Analysis','Under review','2026-07-16 09:46:53'),(15,37,47,'Network Log Analysis','Lead inconclusive','2026-04-10 00:50:53'),(16,3,84,'ISP Contacted','Pending response','2026-02-20 06:23:53'),(17,10,80,'Device Seized','Forwarded to legal team','2026-02-08 17:04:53'),(18,96,98,'Victim Interview','Under review','2026-05-19 05:46:53'),(19,77,50,'Search Warrant Executed','Under review','2026-07-17 17:01:53'),(20,96,40,'Financial Trace','Forwarded to legal team','2026-07-29 08:46:53'),(21,70,9,'OSINT Research','Evidence secured','2026-07-12 11:07:53'),(22,99,50,'Digital Forensics','No new information','2026-08-17 17:38:53'),(23,73,92,'Evidence Collected','Under review','2026-03-19 13:42:53'),(24,44,7,'Warrant Obtained','Suspect identified','2026-03-23 14:15:53'),(25,5,25,'Financial Trace','Completed successfully','2026-08-05 21:28:53'),(26,45,7,'Warrant Obtained','Under review','2026-02-16 22:27:53'),(27,56,95,'OSINT Research','Lead inconclusive','2026-04-13 10:33:53'),(28,69,31,'Victim Interview','Suspect identified','2026-04-16 09:13:53'),(29,59,27,'ISP Contacted','Pending response','2026-07-09 05:46:53'),(30,70,27,'Social Media Monitoring','Evidence secured','2026-04-05 12:44:53'),(31,2,98,'Victim Interview','Forwarded to legal team','2026-03-06 21:35:53'),(32,71,40,'Forensic Report Filed','No new information','2026-07-15 06:44:53'),(33,90,71,'Warrant Obtained','Evidence secured','2026-04-11 16:51:53'),(34,30,32,'ISP Contacted','Forwarded to legal team','2026-05-22 22:31:53'),(35,45,40,'Device Seized','Forwarded to legal team','2026-03-24 04:43:53'),(36,53,25,'Suspect Arrested','Under review','2026-02-17 03:56:53'),(37,40,47,'Suspect Arrested','Positive lead found','2026-02-22 11:01:53'),(38,93,5,'ISP Contacted','Evidence secured','2026-06-10 12:00:53'),(39,23,25,'Device Seized','Forwarded to legal team','2026-08-20 13:27:53'),(40,57,73,'ISP Contacted','Under review','2026-04-01 18:10:53'),(41,91,7,'Evidence Collected','Forwarded to legal team','2026-07-18 08:03:53'),(42,51,77,'Digital Forensics','Suspect identified','2026-06-22 03:14:53'),(43,75,37,'Social Media Monitoring','Suspect identified','2026-02-20 09:33:53'),(44,96,50,'Suspect Surveillance','Completed successfully','2026-03-02 13:43:53'),(45,91,80,'Financial Trace','Lead inconclusive','2026-08-16 12:28:53'),(46,75,37,'Victim Interview','Positive lead found','2026-02-10 01:57:53'),(47,24,40,'Forensic Report Filed','No new information','2026-02-10 04:32:53'),(48,68,80,'Forensic Report Filed','Positive lead found','2026-03-16 15:55:53'),(49,46,31,'ISP Contacted','Positive lead found','2026-06-05 18:43:53'),(50,37,32,'ISP Contacted','Suspect identified','2026-07-18 10:36:53'),(51,64,37,'Evidence Collected','Under review','2026-08-03 04:52:53'),(52,67,37,'Suspect Surveillance','Evidence secured','2026-06-01 09:49:53'),(53,75,98,'OSINT Research','Under review','2026-05-16 04:14:53'),(54,90,71,'Suspect Arrested','Evidence secured','2026-02-12 07:49:53'),(55,65,25,'Evidence Collected','Pending response','2026-03-12 18:07:53'),(56,65,80,'Witness Statement','Under review','2026-06-24 05:15:53'),(57,50,40,'Warrant Obtained','No new information','2026-07-28 14:53:53'),(58,14,35,'Warrant Obtained','Suspect identified','2026-06-05 00:41:53'),(59,68,5,'Search Warrant Executed','Lead inconclusive','2026-07-14 00:40:53'),(60,28,80,'Suspect Surveillance','Completed successfully','2026-08-15 05:07:53'),(61,77,35,'Suspect Surveillance','No new information','2026-07-28 13:16:53'),(62,34,80,'Forensic Report Filed','Evidence secured','2026-06-14 11:58:53'),(63,20,10,'Network Log Analysis','Completed successfully','2026-04-28 11:58:53'),(64,6,98,'ISP Contacted','Suspect identified','2026-07-04 18:46:53'),(65,83,29,'ISP Contacted','Completed successfully','2026-03-19 13:10:53'),(66,20,95,'Financial Trace','Positive lead found','2026-05-21 17:22:53'),(67,70,71,'OSINT Research','Lead inconclusive','2026-07-14 11:01:53'),(68,100,95,'Social Media Monitoring','Lead inconclusive','2026-08-12 21:38:53'),(69,5,9,'Suspect Arrested','Lead inconclusive','2026-03-09 14:56:53'),(70,99,5,'Network Log Analysis','Pending response','2026-06-27 23:47:53'),(71,33,10,'Forensic Report Filed','Forwarded to legal team','2026-04-23 16:45:53'),(72,84,15,'Digital Forensics','Under review','2026-04-30 18:20:53'),(73,36,5,'OSINT Research','Suspect identified','2026-04-13 02:58:53'),(74,4,37,'Witness Statement','Evidence secured','2026-08-22 00:36:53'),(75,30,35,'Financial Trace','Lead inconclusive','2026-06-26 20:02:53'),(76,49,84,'Network Log Analysis','Pending response','2026-08-18 19:02:53'),(77,23,12,'Warrant Obtained','Pending response','2026-03-11 08:14:53'),(78,64,37,'ISP Contacted','Suspect identified','2026-05-12 04:43:53'),(79,37,40,'Network Log Analysis','Forwarded to legal team','2026-05-03 19:11:53'),(80,6,84,'Suspect Surveillance','Under review','2026-03-04 05:24:53'),(81,25,31,'Witness Statement','Under review','2026-07-22 22:21:53'),(82,95,12,'Financial Trace','Evidence secured','2026-06-06 09:44:53'),(83,52,98,'Victim Interview','Evidence secured','2026-06-06 07:33:53'),(84,12,32,'Forensic Report Filed','Pending response','2026-05-13 02:51:53'),(85,79,84,'Forensic Report Filed','Lead inconclusive','2026-07-19 06:13:53'),(86,21,15,'OSINT Research','Lead inconclusive','2026-03-23 17:40:53'),(87,26,80,'Digital Forensics','Suspect identified','2026-03-04 11:57:53'),(88,82,95,'Search Warrant Executed','Completed successfully','2026-07-22 19:25:53'),(89,94,50,'Witness Statement','Forwarded to legal team','2026-07-09 23:48:53'),(90,61,12,'Suspect Surveillance','Suspect identified','2026-06-30 10:53:53'),(91,88,5,'Forensic Report Filed','Lead inconclusive','2026-05-13 04:32:53'),(92,71,25,'Search Warrant Executed','Suspect identified','2026-08-10 06:20:53'),(93,28,80,'Evidence Collected','Forwarded to legal team','2026-05-01 04:52:53'),(94,90,7,'Social Media Monitoring','Pending response','2026-02-23 01:54:53'),(95,22,98,'Social Media Monitoring','Under review','2026-04-13 15:23:53'),(96,33,7,'ISP Contacted','No new information','2026-05-02 21:27:53'),(97,35,27,'ISP Contacted','Under review','2026-05-16 13:17:53'),(98,65,37,'ISP Contacted','Positive lead found','2026-07-09 02:51:53'),(99,76,31,'Search Warrant Executed','Lead inconclusive','2026-04-30 06:52:53'),(100,67,80,'Forensic Report Filed','Positive lead found','2026-03-02 19:22:53');
/*!40000 ALTER TABLE `investigation_activities` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:08
