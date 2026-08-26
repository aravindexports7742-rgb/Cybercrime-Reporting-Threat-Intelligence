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
-- Table structure for table `threat_sources`
--

DROP TABLE IF EXISTS `threat_sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threat_sources` (
  `source_id` int NOT NULL AUTO_INCREMENT,
  `source_name` varchar(150) NOT NULL,
  `source_type` varchar(100) DEFAULT NULL,
  `reliability_rating` enum('Low','Medium','High') DEFAULT 'Medium',
  PRIMARY KEY (`source_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threat_sources`
--

LOCK TABLES `threat_sources` WRITE;
/*!40000 ALTER TABLE `threat_sources` DISABLE KEYS */;
INSERT INTO `threat_sources` VALUES (1,'CERT-In Daily Feed','Government Feed','High'),(2,'AlienVault OTX','Open Source Feed','High'),(3,'Shodan Exposure Monitor','Scan Feed','Medium'),(4,'VirusTotal API','Commercial Feed','High'),(5,'Abuse.ch MalwareBazaar','Open Source Feed','High'),(6,'SpamHaus','Email Reputation','High'),(7,'PhishTank','Phishing Feed','High'),(8,'ThreatConnect','Commercial Feed','Medium'),(9,'Mandiant Threat Intel','Commercial Feed','High'),(10,'CrowdStrike Falcon Intel','Commercial Feed','High'),(11,'Recorded Future','Commercial Feed','High'),(12,'IBM X-Force Exchange','Commercial Feed','Medium'),(13,'US-CERT Alerts','Government Feed','High'),(14,'ShadowServer','Nonprofit Feed','Medium'),(15,'DarkOwl Vision','Dark Web Monitor','Medium'),(16,'Kaspersky TIP','Commercial Feed','High'),(17,'Palo Alto Unit42','Commercial Feed','High'),(18,'Check Point Research','Commercial Feed','Medium'),(19,'Anomali STIX/TAXII','STIX/TAXII Feed','Medium'),(20,'Internal Honeypot Logs','Internal Sensor','Medium'),(21,'ThreatSource_0001','Commercial Feed','Medium'),(22,'ThreatSource_0002','Internal Sensor','Low'),(23,'ThreatSource_0003','Open Source Feed','High'),(24,'ThreatSource_0004','Internal Sensor','Low'),(25,'ThreatSource_0005','Open Source Feed','Medium'),(26,'ThreatSource_0006','Commercial Feed','Low'),(27,'ThreatSource_0007','Internal Sensor','Medium'),(28,'ThreatSource_0008','Open Source Feed','High'),(29,'ThreatSource_0009','Internal Sensor','Medium'),(30,'ThreatSource_0010','Dark Web Monitor','High'),(31,'ThreatSource_0011','Open Source Feed','Medium'),(32,'ThreatSource_0012','Open Source Feed','Medium'),(33,'ThreatSource_0013','Dark Web Monitor','Low'),(34,'ThreatSource_0014','Dark Web Monitor','Low'),(35,'ThreatSource_0015','Internal Sensor','Medium'),(36,'ThreatSource_0016','Dark Web Monitor','Medium'),(37,'ThreatSource_0017','Open Source Feed','Low'),(38,'ThreatSource_0018','Open Source Feed','High'),(39,'ThreatSource_0019','Commercial Feed','Medium'),(40,'ThreatSource_0020','Commercial Feed','Low'),(41,'ThreatSource_0021','Government Feed','Low'),(42,'ThreatSource_0022','Commercial Feed','Medium'),(43,'ThreatSource_0023','Dark Web Monitor','High'),(44,'ThreatSource_0024','Commercial Feed','Low'),(45,'ThreatSource_0025','Internal Sensor','Medium'),(46,'ThreatSource_0026','Commercial Feed','Low'),(47,'ThreatSource_0027','Open Source Feed','Medium'),(48,'ThreatSource_0028','Dark Web Monitor','Low'),(49,'ThreatSource_0029','Government Feed','Low'),(50,'ThreatSource_0030','Dark Web Monitor','Medium'),(51,'ThreatSource_0031','Government Feed','Medium'),(52,'ThreatSource_0032','Open Source Feed','Low'),(53,'ThreatSource_0033','Commercial Feed','Low'),(54,'ThreatSource_0034','Internal Sensor','High'),(55,'ThreatSource_0035','Commercial Feed','Medium'),(56,'ThreatSource_0036','Internal Sensor','High'),(57,'ThreatSource_0037','Dark Web Monitor','Low'),(58,'ThreatSource_0038','Government Feed','Low'),(59,'ThreatSource_0039','Government Feed','Medium'),(60,'ThreatSource_0040','Internal Sensor','Medium'),(61,'ThreatSource_0041','Open Source Feed','Medium'),(62,'ThreatSource_0042','Open Source Feed','Medium'),(63,'ThreatSource_0043','Commercial Feed','Low'),(64,'ThreatSource_0044','Government Feed','High'),(65,'ThreatSource_0045','Internal Sensor','High'),(66,'ThreatSource_0046','Open Source Feed','Low'),(67,'ThreatSource_0047','Internal Sensor','High'),(68,'ThreatSource_0048','Commercial Feed','Medium'),(69,'ThreatSource_0049','Internal Sensor','Medium'),(70,'ThreatSource_0050','Dark Web Monitor','Low'),(71,'ThreatSource_0051','Internal Sensor','Low'),(72,'ThreatSource_0052','Commercial Feed','Medium'),(73,'ThreatSource_0053','Internal Sensor','Low'),(74,'ThreatSource_0054','Commercial Feed','High'),(75,'ThreatSource_0055','Dark Web Monitor','High'),(76,'ThreatSource_0056','Dark Web Monitor','Low'),(77,'ThreatSource_0057','Open Source Feed','Medium'),(78,'ThreatSource_0058','Internal Sensor','Medium'),(79,'ThreatSource_0059','Commercial Feed','Low'),(80,'ThreatSource_0060','Open Source Feed','Medium'),(81,'ThreatSource_0061','Government Feed','High'),(82,'ThreatSource_0062','Government Feed','High'),(83,'ThreatSource_0063','Dark Web Monitor','Medium'),(84,'ThreatSource_0064','Commercial Feed','High'),(85,'ThreatSource_0065','Internal Sensor','Medium'),(86,'ThreatSource_0066','Open Source Feed','Low'),(87,'ThreatSource_0067','Internal Sensor','High'),(88,'ThreatSource_0068','Open Source Feed','Medium'),(89,'ThreatSource_0069','Open Source Feed','Medium'),(90,'ThreatSource_0070','Open Source Feed','Low'),(91,'ThreatSource_0071','Internal Sensor','Medium'),(92,'ThreatSource_0072','Dark Web Monitor','Low'),(93,'ThreatSource_0073','Internal Sensor','High'),(94,'ThreatSource_0074','Government Feed','High'),(95,'ThreatSource_0075','Government Feed','High'),(96,'ThreatSource_0076','Government Feed','High'),(97,'ThreatSource_0077','Dark Web Monitor','Medium'),(98,'ThreatSource_0078','Commercial Feed','High'),(99,'ThreatSource_0079','Government Feed','Medium'),(100,'ThreatSource_0080','Commercial Feed','Medium');
/*!40000 ALTER TABLE `threat_sources` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 16:07:09
