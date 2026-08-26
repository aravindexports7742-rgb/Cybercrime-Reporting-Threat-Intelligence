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
-- Table structure for table `login_history`
--

DROP TABLE IF EXISTS `login_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_history` (
  `login_id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `event_type` enum('Login Success','Login Failed','Logout') NOT NULL,
  `event_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`login_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `login_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_history`
--

LOCK TABLES `login_history` WRITE;
/*!40000 ALTER TABLE `login_history` DISABLE KEYS */;
INSERT INTO `login_history` VALUES (1,4,'Login Success','2026-08-25 10:50:56',NULL),(2,2,'Login Success','2026-08-25 10:51:35',NULL),(3,3,'Login Success','2026-08-25 10:51:55',NULL),(4,3,'Login Success','2026-08-25 11:00:10',NULL),(5,2,'Login Success','2026-08-25 11:01:22',NULL),(6,1,'Login Success','2026-08-25 11:01:47',NULL),(7,5,'Login Success','2026-08-25 11:02:45',NULL),(8,5,'Login Success','2026-08-25 11:23:04',NULL),(9,3,'Login Success','2026-08-25 11:27:07',NULL),(10,2,'Login Success','2026-08-25 11:27:26',NULL),(11,4,'Login Success','2026-08-25 11:27:55',NULL),(12,2,'Login Success','2026-08-26 06:22:16',NULL),(13,5,'Login Success','2026-08-26 06:22:42',NULL),(14,90,'Login Failed','2026-06-30 08:10:54','189.192.98.108'),(15,18,'Login Success','2026-07-16 23:24:54','162.38.102.94'),(16,3,'Login Failed','2026-06-03 07:10:54','152.242.47.56'),(17,51,'Login Success','2026-07-06 21:10:54','70.86.50.6'),(18,13,'Login Failed','2026-08-06 02:26:54','245.218.140.72'),(19,27,'Login Success','2026-06-24 16:33:54','128.110.111.243'),(20,82,'Login Failed','2026-06-02 10:57:54','247.27.17.244'),(21,80,'Logout','2026-06-25 17:01:54','37.60.132.242'),(22,13,'Login Success','2026-07-03 21:19:54','245.78.161.41'),(23,92,'Logout','2026-07-17 14:40:54','110.156.31.154'),(24,62,'Logout','2026-07-21 01:33:54','96.206.176.222'),(25,62,'Login Failed','2026-06-14 21:15:54','5.114.94.107'),(26,31,'Login Success','2026-07-15 14:05:54','233.223.231.81'),(27,16,'Login Failed','2026-07-21 18:58:54','148.203.84.179'),(28,9,'Login Success','2026-07-15 15:43:54','249.233.58.182'),(29,83,'Logout','2026-07-27 04:48:54','145.120.227.5'),(30,77,'Logout','2026-08-13 23:31:54','38.159.82.21'),(31,44,'Login Failed','2026-06-27 16:22:54','229.242.245.187'),(32,37,'Login Success','2026-06-29 23:30:54','50.202.197.71'),(33,60,'Login Success','2026-07-11 10:49:54','64.57.162.1'),(34,80,'Login Failed','2026-06-07 20:44:54','38.200.69.245'),(35,77,'Login Failed','2026-07-16 16:23:54','138.51.210.208'),(36,17,'Login Success','2026-06-10 17:12:54','76.187.15.189'),(37,9,'Logout','2026-06-23 03:04:54','203.96.108.180'),(38,3,'Login Failed','2026-07-24 06:10:54','76.6.7.167'),(39,17,'Login Failed','2026-08-16 00:50:54','199.232.254.38'),(40,85,'Logout','2026-07-08 19:09:54','153.113.194.81'),(41,53,'Login Failed','2026-06-29 04:07:54','181.155.116.73'),(42,82,'Logout','2026-08-10 02:18:54','32.13.222.84'),(43,67,'Login Failed','2026-07-10 07:59:54','213.184.96.141'),(44,18,'Logout','2026-07-01 15:59:54','102.45.83.157'),(45,96,'Login Success','2026-06-05 02:59:54','145.193.145.11'),(46,41,'Login Success','2026-08-09 21:15:54','238.17.35.39'),(47,53,'Logout','2026-08-05 14:04:54','24.193.92.249'),(48,98,'Login Failed','2026-08-15 22:58:54','193.17.126.103'),(49,52,'Login Success','2026-06-19 22:38:54','203.101.177.40'),(50,67,'Login Success','2026-07-30 22:09:54','30.195.233.223'),(51,35,'Login Success','2026-07-27 10:38:54','175.142.6.14'),(52,17,'Logout','2026-07-28 21:17:54','11.56.194.60'),(53,68,'Login Success','2026-06-23 01:59:54','100.193.162.172'),(54,55,'Login Success','2026-06-22 02:48:54','7.171.182.179'),(55,70,'Logout','2026-08-18 11:07:54','151.9.53.59'),(56,81,'Login Failed','2026-08-26 00:35:54','21.148.225.95'),(57,41,'Login Success','2026-07-07 06:10:54','138.1.234.161'),(58,89,'Logout','2026-07-21 03:44:54','96.130.99.41'),(59,10,'Logout','2026-07-25 02:07:54','84.229.66.101'),(60,59,'Logout','2026-07-20 22:18:54','115.154.247.167'),(61,23,'Logout','2026-07-06 06:08:54','29.10.99.206'),(62,53,'Logout','2026-07-31 05:31:54','146.188.191.77'),(63,48,'Logout','2026-07-29 17:27:54','78.92.118.14'),(64,17,'Logout','2026-07-27 17:23:54','227.215.64.56'),(65,41,'Login Success','2026-07-18 12:06:54','213.46.220.86'),(66,12,'Login Failed','2026-07-07 12:59:54','118.251.100.155'),(67,91,'Login Success','2026-06-24 20:44:54','153.73.203.253'),(68,23,'Login Success','2026-08-16 17:13:54','227.0.218.8'),(69,8,'Login Success','2026-08-25 03:20:54','1.77.113.98'),(70,63,'Logout','2026-08-06 09:16:54','95.55.165.49'),(71,76,'Logout','2026-07-10 10:02:54','107.167.5.77'),(72,97,'Login Success','2026-08-11 03:10:54','68.116.238.239'),(73,12,'Login Success','2026-06-05 12:36:54','203.7.225.239'),(74,94,'Login Success','2026-08-25 09:14:54','186.60.116.223'),(75,81,'Logout','2026-06-16 04:02:54','6.179.144.123'),(76,34,'Logout','2026-05-30 08:06:54','17.101.173.97'),(77,18,'Login Success','2026-06-23 22:26:54','120.105.44.250'),(78,3,'Logout','2026-08-20 15:15:54','246.197.224.72'),(79,58,'Login Failed','2026-06-26 05:28:54','69.6.171.70'),(80,9,'Login Success','2026-05-29 21:28:54','1.254.166.12'),(81,74,'Login Failed','2026-06-15 13:48:54','203.59.183.218'),(82,89,'Login Success','2026-07-21 01:14:54','154.94.116.211'),(83,94,'Logout','2026-08-06 00:37:54','231.95.185.142'),(84,52,'Login Success','2026-07-15 12:39:54','89.104.44.149'),(85,56,'Login Failed','2026-06-28 00:30:54','75.37.208.173'),(86,91,'Login Failed','2026-05-31 18:53:54','93.246.110.23'),(87,88,'Login Failed','2026-08-09 01:20:54','92.165.119.116'),(88,91,'Logout','2026-05-31 06:23:54','11.87.129.236'),(89,14,'Login Success','2026-06-11 01:45:54','162.212.190.41'),(90,75,'Login Success','2026-07-30 13:54:54','21.210.107.226'),(91,57,'Logout','2026-06-18 10:46:54','27.147.1.66'),(92,67,'Logout','2026-08-04 13:05:54','176.181.201.86'),(93,11,'Login Success','2026-07-15 12:26:54','205.95.140.240'),(94,55,'Logout','2026-06-03 00:05:54','148.89.191.105'),(95,48,'Login Success','2026-07-28 15:38:54','117.39.213.178'),(96,91,'Login Success','2026-08-25 19:28:54','28.126.36.235'),(97,39,'Logout','2026-07-18 04:31:54','104.77.211.54'),(98,52,'Logout','2026-08-14 06:18:54','5.7.75.31'),(99,12,'Login Success','2026-05-31 10:15:54','65.115.243.31'),(100,76,'Login Failed','2026-06-03 00:19:54','179.152.76.88'),(101,2,'Login Success','2026-08-26 06:53:11',NULL),(102,4,'Login Success','2026-08-26 06:54:09',NULL),(103,4,'Login Success','2026-08-26 07:11:55',NULL),(104,2,'Login Success','2026-08-26 09:32:41',NULL),(105,2,'Login Success','2026-08-26 09:37:22',NULL),(106,4,'Login Success','2026-08-26 09:45:10',NULL),(107,1,'Login Success','2026-08-26 09:47:30',NULL),(108,5,'Login Success','2026-08-26 09:47:48',NULL),(109,2,'Login Success','2026-08-26 09:48:26',NULL);
/*!40000 ALTER TABLE `login_history` ENABLE KEYS */;
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
