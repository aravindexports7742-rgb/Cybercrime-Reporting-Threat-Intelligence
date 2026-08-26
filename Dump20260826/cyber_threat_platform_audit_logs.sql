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
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `log_id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(150) NOT NULL,
  `resource` varchar(100) DEFAULT NULL,
  `resource_id` varchar(50) DEFAULT NULL,
  `event_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  `result` enum('Success','Failure') NOT NULL DEFAULT 'Success',
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  KEY `idx_audit_event_time` (`event_time`),
  CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,3,'Complaint Submission','complaints','CYB-2026-000001','2026-08-25 11:00:43',NULL,'Success'),(2,18,'VIEW_REPORT','cases','300','2026-07-05 11:33:54','117.217.228.65','Failure'),(3,36,'EXPORT_DATA','incidents','997','2026-07-26 03:51:54','201.12.83.118','Failure'),(4,97,'ASSIGN_CASE','evidence','572','2026-06-16 15:59:54','190.102.192.90','Success'),(5,13,'VIEW_COMPLAINT','incidents','361','2026-06-08 18:32:54','207.214.247.59','Failure'),(6,73,'UPDATE_COMPLAINT','cases','655','2026-07-06 01:40:54','128.163.47.194','Failure'),(7,10,'CREATE_IOC','playbooks','360','2026-07-13 21:22:54','93.193.40.246','Success'),(8,80,'LOGIN','cases','195','2026-06-13 02:21:54','130.179.164.144','Failure'),(9,91,'CREATE_INCIDENT','reports','183','2026-07-06 16:35:54','20.50.23.24','Failure'),(10,35,'CREATE_CASE','incidents','546','2026-07-12 00:11:54','236.98.26.217','Failure'),(11,99,'RESOLVE_INCIDENT','cases','332','2026-07-28 21:27:54','11.62.140.40','Failure'),(12,18,'RUN_PLAYBOOK','evidence','854','2026-05-30 05:04:54','225.57.112.166','Success'),(13,66,'LOGIN','iocs','250','2026-08-23 16:49:54','215.112.106.143','Success'),(14,64,'ASSIGN_CASE','reports','595','2026-07-05 15:43:54','228.230.250.100','Failure'),(15,58,'EXPORT_DATA','iocs','442','2026-07-10 00:22:54','237.239.60.82','Failure'),(16,39,'CREATE_CASE','incidents','881','2026-05-29 04:29:54','138.148.32.25','Failure'),(17,45,'VIEW_REPORT','cases','827','2026-06-10 04:33:54','90.183.179.166','Success'),(18,90,'CREATE_IOC','audit_logs','857','2026-08-19 21:40:54','113.127.151.112','Success'),(19,93,'LOGIN','reports','460','2026-06-15 16:16:54','230.88.122.223','Success'),(20,34,'EXPORT_DATA','cases','978','2026-07-21 18:03:54','243.229.186.8','Failure'),(21,78,'CREATE_CASE','campaigns','221','2026-06-02 22:00:54','138.178.172.78','Failure'),(22,27,'RESOLVE_INCIDENT','reports','969','2026-07-05 07:30:54','139.250.174.151','Failure'),(23,1,'MANAGE_CAMPAIGN','complaints','730','2026-07-11 18:12:54','199.250.18.158','Success'),(24,44,'DELETE_USER','users','751','2026-08-02 04:41:54','199.194.253.46','Success'),(25,18,'RUN_PLAYBOOK','cases','340','2026-08-15 08:54:54','147.179.242.176','Failure'),(26,64,'UPDATE_USER','playbooks','142','2026-07-14 07:13:54','80.90.45.182','Failure'),(27,32,'RUN_PLAYBOOK','cases','189','2026-07-24 00:07:54','59.89.252.166','Success'),(28,92,'ACCESS_AUDIT_LOG','cases','537','2026-07-25 11:23:54','156.15.251.143','Success'),(29,36,'EXPORT_DATA','cases','173','2026-08-25 20:19:54','2.83.98.79','Success'),(30,74,'RESOLVE_INCIDENT','incidents','880','2026-08-18 07:07:54','163.158.127.47','Success'),(31,95,'UPDATE_COMPLAINT','users','615','2026-07-09 18:08:54','229.112.180.217','Success'),(32,38,'CREATE_CASE','playbooks','32','2026-06-08 10:20:54','138.227.245.204','Success'),(33,73,'DELETE_IOC','cases','358','2026-05-31 06:42:54','133.42.230.26','Failure'),(34,9,'MANAGE_CAMPAIGN','users','628','2026-07-13 21:20:54','169.140.212.100','Failure'),(35,57,'CREATE_INCIDENT','cases','347','2026-07-26 01:10:54','62.245.209.126','Success'),(36,56,'LOGOUT','incidents','61','2026-06-25 14:34:54','194.214.151.26','Success'),(37,22,'VIEW_REPORT','reports','577','2026-06-13 13:45:54','134.100.193.140','Success'),(38,47,'VIEW_REPORT','users','459','2026-08-01 02:39:54','110.103.111.97','Success'),(39,11,'LOGIN','playbooks','107','2026-07-15 18:49:54','157.99.78.128','Failure'),(40,97,'LOGOUT','reports','852','2026-08-21 06:14:54','79.228.150.192','Success'),(41,17,'VIEW_REPORT','complaints','548','2026-08-23 11:00:54','99.48.90.247','Success'),(42,36,'DELETE_USER','reports','537','2026-08-03 19:56:54','175.178.11.234','Success'),(43,51,'ACCESS_AUDIT_LOG','users','914','2026-07-28 13:59:54','19.182.52.127','Success'),(44,75,'MANAGE_CAMPAIGN','complaints','47','2026-07-09 05:22:54','177.29.236.75','Success'),(45,29,'VIEW_REPORT','users','400','2026-07-28 00:21:54','215.102.11.40','Success'),(46,87,'VIEW_EVIDENCE','audit_logs','685','2026-07-23 22:36:54','147.181.221.231','Failure'),(47,12,'CREATE_IOC','campaigns','707','2026-08-24 22:27:54','106.96.71.216','Success'),(48,100,'RUN_PLAYBOOK','iocs','615','2026-08-24 15:35:54','102.10.178.197','Failure'),(49,62,'VIEW_EVIDENCE','cases','653','2026-08-12 09:09:54','231.202.125.18','Success'),(50,45,'VIEW_REPORT','users','967','2026-07-24 14:34:54','239.177.101.73','Failure'),(51,47,'RESOLVE_INCIDENT','iocs','112','2026-08-10 23:27:54','227.226.51.244','Success'),(52,72,'RUN_PLAYBOOK','evidence','131','2026-06-21 10:49:54','123.27.28.59','Success'),(53,46,'ASSIGN_CASE','cases','781','2026-05-30 10:04:54','112.157.94.113','Success'),(54,79,'MANAGE_CAMPAIGN','complaints','679','2026-06-23 05:30:54','54.185.81.12','Success'),(55,68,'VIEW_REPORT','iocs','944','2026-08-04 00:50:54','52.230.164.15','Failure'),(56,30,'CREATE_CASE','iocs','518','2026-08-18 05:08:54','161.49.85.169','Failure'),(57,18,'ACCESS_AUDIT_LOG','cases','864','2026-07-25 16:46:54','74.142.41.37','Failure'),(58,33,'UPDATE_COMPLAINT','cases','420','2026-06-20 19:18:54','159.184.43.186','Failure'),(59,19,'LOGOUT','users','924','2026-08-12 15:05:54','2.97.0.145','Success'),(60,46,'RESOLVE_INCIDENT','cases','878','2026-07-28 16:17:54','145.139.18.6','Failure'),(61,75,'UPDATE_USER','iocs','703','2026-06-08 23:51:54','234.191.60.175','Failure'),(62,99,'CREATE_IOC','incidents','652','2026-06-28 20:21:54','231.39.116.138','Failure'),(63,25,'CREATE_CASE','iocs','653','2026-08-04 00:03:54','226.41.94.190','Success'),(64,78,'DELETE_IOC','users','44','2026-06-28 22:34:54','226.138.218.59','Failure'),(65,62,'EXPORT_DATA','evidence','965','2026-07-05 22:23:54','107.117.187.116','Failure'),(66,46,'ACCESS_AUDIT_LOG','incidents','346','2026-07-15 14:54:54','35.185.135.53','Success'),(67,15,'UPLOAD_EVIDENCE','audit_logs','200','2026-06-02 16:56:54','231.118.140.221','Failure'),(68,19,'DELETE_IOC','evidence','403','2026-08-07 21:13:54','139.166.115.77','Failure'),(69,26,'UPLOAD_EVIDENCE','evidence','346','2026-06-17 06:37:54','99.239.132.111','Success'),(70,79,'LOGIN','evidence','396','2026-06-14 15:08:54','70.251.190.175','Success'),(71,17,'UPDATE_USER','audit_logs','801','2026-08-01 07:53:54','82.119.62.223','Success'),(72,96,'RUN_PLAYBOOK','incidents','626','2026-06-08 19:32:54','161.224.9.174','Success'),(73,NULL,'VIEW_COMPLAINT','cases','22','2026-08-25 10:58:54','219.23.80.239','Failure'),(74,10,'CREATE_CASE','evidence','315','2026-08-18 00:40:54','233.80.149.232','Failure'),(75,94,'VIEW_REPORT','users','297','2026-07-19 08:28:54','144.40.230.226','Success'),(76,82,'DELETE_USER','cases','546','2026-06-07 23:09:54','144.141.160.121','Failure'),(77,48,'VIEW_EVIDENCE','cases','680','2026-08-07 22:13:54','194.10.34.226','Failure'),(78,94,'UPDATE_USER','playbooks','175','2026-08-23 17:35:54','253.209.92.239','Failure'),(79,81,'RESOLVE_INCIDENT','users','459','2026-08-23 20:37:54','146.88.226.87','Success'),(80,19,'VIEW_COMPLAINT','users','139','2026-06-08 02:36:54','101.234.38.29','Success'),(81,16,'VIEW_REPORT','iocs','729','2026-08-16 00:41:54','252.204.126.5','Failure'),(82,93,'EXPORT_DATA','iocs','197','2026-06-22 03:46:54','232.234.6.126','Failure'),(83,93,'LOGOUT','evidence','718','2026-07-18 03:51:54','111.86.10.70','Failure'),(84,22,'VIEW_COMPLAINT','incidents','565','2026-08-22 07:24:54','251.237.159.3','Success'),(85,71,'UPDATE_USER','evidence','927','2026-06-26 23:55:54','10.177.172.70','Failure'),(86,84,'EXPORT_DATA','reports','875','2026-07-02 22:34:54','88.33.241.89','Failure'),(87,67,'UPLOAD_EVIDENCE','playbooks','289','2026-07-23 09:21:54','116.235.171.22','Failure'),(88,41,'UPDATE_COMPLAINT','complaints','831','2026-08-10 09:04:54','20.45.95.17','Success'),(89,75,'VIEW_EVIDENCE','cases','885','2026-08-17 11:33:54','4.188.206.88','Success'),(90,68,'RESOLVE_INCIDENT','playbooks','647','2026-07-14 15:13:54','157.31.14.181','Success'),(91,10,'VIEW_COMPLAINT','users','94','2026-08-15 11:52:54','203.175.59.54','Success'),(92,60,'VIEW_COMPLAINT','campaigns','329','2026-06-06 20:07:54','122.209.50.182','Failure'),(93,88,'ASSIGN_CASE','playbooks','295','2026-05-31 17:24:54','221.15.113.48','Success'),(94,43,'ASSIGN_CASE','evidence','270','2026-08-07 18:43:54','250.48.179.32','Success'),(95,9,'ASSIGN_CASE','incidents','775','2026-07-28 06:54:54','163.214.151.76','Failure'),(96,38,'DELETE_IOC','evidence','437','2026-07-25 00:32:54','62.135.1.168','Failure'),(97,47,'ASSIGN_CASE','cases','64','2026-08-17 20:57:54','232.187.15.159','Failure'),(98,43,'ACCESS_AUDIT_LOG','complaints','763','2026-06-01 09:59:54','151.197.234.235','Failure'),(99,54,'MANAGE_CAMPAIGN','cases','583','2026-07-23 12:26:54','82.115.91.191','Failure'),(100,19,'RUN_PLAYBOOK','iocs','782','2026-06-25 01:45:54','191.48.58.151','Success'),(101,24,'EXPORT_DATA','campaigns','477','2026-06-28 01:20:54','204.216.241.249','Failure');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
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
