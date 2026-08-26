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
-- Table structure for table `playbook_steps`
--

DROP TABLE IF EXISTS `playbook_steps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playbook_steps` (
  `step_id` int NOT NULL AUTO_INCREMENT,
  `playbook_id` int NOT NULL,
  `step_order` int NOT NULL,
  `step_description` varchar(255) NOT NULL,
  PRIMARY KEY (`step_id`),
  UNIQUE KEY `uq_playbook_step_order` (`playbook_id`,`step_order`),
  CONSTRAINT `playbook_steps_ibfk_1` FOREIGN KEY (`playbook_id`) REFERENCES `playbooks` (`playbook_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playbook_steps`
--

LOCK TABLES `playbook_steps` WRITE;
/*!40000 ALTER TABLE `playbook_steps` DISABLE KEYS */;
INSERT INTO `playbook_steps` VALUES (1,75,1,'Identify and isolate affected systems from the network.'),(2,22,1,'Identify and isolate affected systems from the network.'),(3,91,1,'Identify and isolate affected systems from the network.'),(4,89,1,'Identify and isolate affected systems from the network.'),(5,63,1,'Identify and isolate affected systems from the network.'),(6,98,1,'Identify and isolate affected systems from the network.'),(7,38,1,'Identify and isolate affected systems from the network.'),(8,29,1,'Identify and isolate affected systems from the network.'),(9,67,1,'Identify and isolate affected systems from the network.'),(10,14,1,'Identify and isolate affected systems from the network.'),(11,12,1,'Identify and isolate affected systems from the network.'),(12,94,1,'Identify and isolate affected systems from the network.'),(13,78,1,'Identify and isolate affected systems from the network.'),(14,77,1,'Identify and isolate affected systems from the network.'),(15,47,1,'Identify and isolate affected systems from the network.'),(16,31,1,'Identify and isolate affected systems from the network.'),(17,86,1,'Identify and isolate affected systems from the network.'),(18,64,1,'Identify and isolate affected systems from the network.'),(19,90,1,'Identify and isolate affected systems from the network.'),(20,56,1,'Identify and isolate affected systems from the network.'),(21,54,1,'Identify and isolate affected systems from the network.'),(22,8,1,'Identify and isolate affected systems from the network.'),(23,82,1,'Identify and isolate affected systems from the network.'),(24,14,2,'Notify the Incident Response team and management.'),(25,99,1,'Identify and isolate affected systems from the network.'),(26,36,1,'Identify and isolate affected systems from the network.'),(27,93,1,'Identify and isolate affected systems from the network.'),(28,94,2,'Notify the Incident Response team and management.'),(29,36,2,'Notify the Incident Response team and management.'),(30,33,1,'Identify and isolate affected systems from the network.'),(31,82,2,'Notify the Incident Response team and management.'),(32,66,1,'Identify and isolate affected systems from the network.'),(33,43,1,'Identify and isolate affected systems from the network.'),(34,54,2,'Notify the Incident Response team and management.'),(35,86,2,'Notify the Incident Response team and management.'),(36,33,2,'Notify the Incident Response team and management.'),(37,46,1,'Identify and isolate affected systems from the network.'),(38,11,1,'Identify and isolate affected systems from the network.'),(39,2,1,'Identify and isolate affected systems from the network.'),(40,13,1,'Identify and isolate affected systems from the network.'),(41,92,1,'Identify and isolate affected systems from the network.'),(42,63,2,'Notify the Incident Response team and management.'),(43,32,1,'Identify and isolate affected systems from the network.'),(44,75,2,'Notify the Incident Response team and management.'),(45,64,2,'Notify the Incident Response team and management.'),(46,29,2,'Notify the Incident Response team and management.'),(47,76,1,'Identify and isolate affected systems from the network.'),(48,56,2,'Notify the Incident Response team and management.'),(49,86,3,'Preserve evidence: take memory dumps and disk images.'),(50,35,1,'Identify and isolate affected systems from the network.'),(51,14,3,'Preserve evidence: take memory dumps and disk images.'),(52,100,1,'Identify and isolate affected systems from the network.'),(53,91,2,'Notify the Incident Response team and management.'),(54,63,3,'Preserve evidence: take memory dumps and disk images.'),(55,72,1,'Identify and isolate affected systems from the network.'),(56,78,2,'Notify the Incident Response team and management.'),(57,73,1,'Identify and isolate affected systems from the network.'),(58,49,1,'Identify and isolate affected systems from the network.'),(59,78,3,'Preserve evidence: take memory dumps and disk images.'),(60,67,2,'Notify the Incident Response team and management.'),(61,86,4,'Analyse threat indicators using sandbox tools.'),(62,49,2,'Notify the Incident Response team and management.'),(63,6,1,'Identify and isolate affected systems from the network.'),(64,78,4,'Analyse threat indicators using sandbox tools.'),(65,14,4,'Analyse threat indicators using sandbox tools.'),(66,76,2,'Notify the Incident Response team and management.'),(67,83,1,'Identify and isolate affected systems from the network.'),(68,13,2,'Notify the Incident Response team and management.'),(69,74,1,'Identify and isolate affected systems from the network.'),(70,13,3,'Preserve evidence: take memory dumps and disk images.'),(71,16,1,'Identify and isolate affected systems from the network.'),(72,98,2,'Notify the Incident Response team and management.'),(73,31,2,'Notify the Incident Response team and management.'),(74,47,2,'Notify the Incident Response team and management.'),(75,75,3,'Preserve evidence: take memory dumps and disk images.'),(76,87,1,'Identify and isolate affected systems from the network.'),(77,91,3,'Preserve evidence: take memory dumps and disk images.'),(78,78,5,'Block identified IOCs at firewall and endpoint level.'),(79,54,3,'Preserve evidence: take memory dumps and disk images.'),(80,51,1,'Identify and isolate affected systems from the network.'),(81,92,2,'Notify the Incident Response team and management.'),(82,96,1,'Identify and isolate affected systems from the network.'),(83,6,2,'Notify the Incident Response team and management.'),(84,45,1,'Identify and isolate affected systems from the network.'),(85,83,2,'Notify the Incident Response team and management.'),(86,57,1,'Identify and isolate affected systems from the network.'),(87,59,1,'Identify and isolate affected systems from the network.'),(88,74,2,'Notify the Incident Response team and management.'),(89,67,3,'Preserve evidence: take memory dumps and disk images.'),(90,5,1,'Identify and isolate affected systems from the network.'),(91,52,1,'Identify and isolate affected systems from the network.'),(92,81,1,'Identify and isolate affected systems from the network.'),(93,96,2,'Notify the Incident Response team and management.'),(94,100,2,'Notify the Incident Response team and management.'),(95,56,3,'Preserve evidence: take memory dumps and disk images.'),(96,86,5,'Block identified IOCs at firewall and endpoint level.'),(97,4,1,'Identify and isolate affected systems from the network.'),(98,28,1,'Identify and isolate affected systems from the network.'),(99,73,2,'Notify the Incident Response team and management.'),(100,24,1,'Identify and isolate affected systems from the network.');
/*!40000 ALTER TABLE `playbook_steps` ENABLE KEYS */;
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
