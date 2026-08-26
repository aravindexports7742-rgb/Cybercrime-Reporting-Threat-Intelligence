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
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `permission_id` int NOT NULL AUTO_INCREMENT,
  `permission_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`permission_id`),
  UNIQUE KEY `permission_name` (`permission_name`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (1,'view_complaints','Read all complaints'),(2,'create_complaint','Submit a new complaint'),(3,'edit_complaint','Modify an existing complaint'),(4,'delete_complaint','Remove a complaint'),(5,'assign_case','Assign a case to an officer'),(6,'close_case','Mark a case as closed'),(7,'view_evidence','View uploaded evidence'),(8,'upload_evidence','Upload new evidence files'),(9,'manage_iocs','Create/edit IOC entries'),(10,'view_iocs','Read IOC data'),(11,'view_threat_feeds','Access threat feed data'),(12,'manage_incidents','Create and manage incidents'),(13,'view_incidents','Read incident details'),(14,'run_playbook','Execute a response playbook'),(15,'manage_users','Create and edit users'),(16,'view_audit_logs','Access system audit logs'),(17,'manage_roles','Assign roles to users'),(18,'view_reports','View generated reports'),(19,'export_data','Export platform data'),(20,'system_config','Modify platform configuration'),(21,'manage_campaigns','Handle threat campaigns'),(22,'view_campaigns','Read campaign data'),(23,'manage_playbooks','Create and edit playbooks'),(24,'coordinate_agency','Communicate with external agencies'),(25,'view_suspects','Read suspect profiles'),(26,'manage_suspects','Create/edit suspect records'),(27,'view_analytics','Access analytical dashboards'),(28,'manage_notifications','Send/manage notifications'),(29,'view_login_history','Read login history logs'),(30,'system_health_check','Check system component health');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
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
