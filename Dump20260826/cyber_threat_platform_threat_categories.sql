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
-- Table structure for table `threat_categories`
--

DROP TABLE IF EXISTS `threat_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threat_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threat_categories`
--

LOCK TABLES `threat_categories` WRITE;
/*!40000 ALTER TABLE `threat_categories` DISABLE KEYS */;
INSERT INTO `threat_categories` VALUES (1,'Phishing','Credential harvesting via fake sites or emails'),(2,'Ransomware','Malware encrypting data and demanding ransom'),(3,'APT','Advanced Persistent Threat actor activity'),(4,'Botnet','Network of compromised machines'),(5,'Credential Theft','Stealing login credentials'),(6,'Data Exfiltration','Unauthorized data transfer out of network'),(7,'Exploit Kit','Automated exploitation framework'),(8,'Keylogger','Software capturing keystrokes'),(9,'Rootkit','Stealthy malware achieving persistent access'),(10,'Spyware','Software covertly monitoring user activity'),(11,'Trojan','Malware disguised as legitimate software'),(12,'Worm','Self-replicating malware spreading via networks'),(13,'Zero Day','Exploitation of previously unknown vulnerability'),(14,'Supply Chain','Attack via compromised third-party software'),(15,'Insider Threat','Malicious activity from within the organization'),(16,'DDoS','Distributed Denial of Service attack'),(17,'SQL Injection','Database attack via malicious SQL queries'),(18,'Cross-Site Scripting','XSS vulnerability exploitation'),(19,'Man in the Middle','Intercepting communications between two parties'),(20,'Cryptojacking','Unauthorized use of computing resources for mining');
/*!40000 ALTER TABLE `threat_categories` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:04
