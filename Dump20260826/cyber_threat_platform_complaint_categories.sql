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
-- Table structure for table `complaint_categories`
--

DROP TABLE IF EXISTS `complaint_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint_categories`
--

LOCK TABLES `complaint_categories` WRITE;
/*!40000 ALTER TABLE `complaint_categories` DISABLE KEYS */;
INSERT INTO `complaint_categories` VALUES (1,'Online Abuse',NULL),(2,'Financial Fraud',NULL),(3,'Phishing',NULL),(5,'Ransomware','Malicious software encrypting victim data for ransom'),(6,'Online Fraud','Financial fraud conducted over the internet'),(7,'Identity Theft','Unauthorized use of another person identity'),(8,'Cyberbullying','Harassment and bullying through digital channels'),(9,'Data Breach','Unauthorized access to confidential data'),(10,'Hacking','Unauthorized intrusion into computer systems'),(11,'Malware','Malicious software infection on devices'),(12,'Vishing','Voice phishing via phone calls'),(13,'Smishing','SMS-based phishing attacks'),(14,'Credit Card Fraud','Unauthorized use of credit/debit card information'),(15,'Dark Web Activity','Illegal activities on dark web marketplaces'),(16,'Social Engineering','Psychological manipulation to gain access'),(17,'Crypto Fraud','Cryptocurrency-based scams and theft'),(18,'SIM Swapping','Illegitimate transfer of phone number to attacker SIM'),(19,'Business Email Compromise','Email fraud targeting business organizations'),(20,'Child Safety Online','Online exploitation or harm of minors'),(21,'IP Theft','Theft of patents, trade secrets, or copyrighted content'),(22,'Sextortion','Blackmail using intimate images'),(23,'DoS/DDoS Attack','Denial of service attack on systems or networks');
/*!40000 ALTER TABLE `complaint_categories` ENABLE KEYS */;
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
