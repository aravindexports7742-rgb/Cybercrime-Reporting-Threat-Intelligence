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
-- Table structure for table `iocs`
--

DROP TABLE IF EXISTS `iocs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iocs` (
  `ioc_id` int NOT NULL AUTO_INCREMENT,
  `ioc_type` enum('IP','Domain','URL','Hash','Email') NOT NULL,
  `ioc_value` varchar(255) NOT NULL,
  `category_id` int DEFAULT NULL,
  `source_id` int DEFAULT NULL,
  `risk_level` enum('Low','Medium','High','Critical') NOT NULL DEFAULT 'Low',
  `first_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ioc_id`),
  UNIQUE KEY `uq_ioc_type_value` (`ioc_type`,`ioc_value`),
  KEY `category_id` (`category_id`),
  KEY `source_id` (`source_id`),
  KEY `idx_iocs_risk` (`risk_level`),
  CONSTRAINT `iocs_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `threat_categories` (`category_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `iocs_ibfk_2` FOREIGN KEY (`source_id`) REFERENCES `threat_sources` (`source_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iocs`
--

LOCK TABLES `iocs` WRITE;
/*!40000 ALTER TABLE `iocs` DISABLE KEYS */;
INSERT INTO `iocs` VALUES (1,'Email','attacker50651@disposable.io',17,14,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(2,'Email','attacker59184@guerrillamail.com',5,22,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(3,'Email','attacker23284@tempmail.com',13,63,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(4,'Domain','hack1139.top',8,27,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(5,'URL','http://fake1147.top/csg4ofdtrc85',20,27,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(6,'Hash','229946840d48a5672a0f71b290411ca4',17,21,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(7,'Email','attacker26605@mailnull.com',15,26,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(8,'Domain','scam1049.top',13,32,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(9,'Email','attacker64351@mailnull.com',10,74,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(10,'IP','74.165.225.236',10,45,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(11,'Hash','aa2776186be6bae8db4cdd97227de501',13,23,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(12,'Domain','dark7080.top',2,85,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(13,'Email','attacker12522@mailnull.com',4,31,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(14,'URL','http://fake4783.com/z0hr9t9cd1lq',15,27,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(15,'Hash','2dcdacf3f639e476145ae372c4d3b3d5',3,10,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(16,'Hash','f1f29f659a3b6234f3ad85182c5f8b96',19,96,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(17,'Domain','crypto619.com',15,15,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(18,'URL','http://scam7943.top/cti8f34gadkt',2,22,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(19,'IP','174.69.39.113',1,23,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(20,'IP','229.172.136.56',10,90,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(21,'Email','attacker84019@tempmail.com',2,89,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(22,'Hash','ecb711ca44ef077299f371207a1eb880',4,77,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(23,'IP','198.96.196.52',7,48,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(24,'Domain','phish263.top',3,2,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(25,'Domain','phish3614.com',6,93,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(26,'IP','107.131.27.209',19,42,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(27,'Email','attacker27148@mailnull.com',9,16,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(28,'Domain','phish5843.xyz',6,2,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(29,'URL','http://evil6377.net/qc3xnchkv9dt',12,22,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(30,'IP','154.83.251.162',2,87,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(31,'URL','http://dark5210.top/ca6qs0szaa1e',7,95,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(32,'Domain','threat1301.com',20,48,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(33,'URL','http://hack2485.top/hb7v80lkx1s9',NULL,37,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(34,'Domain','ransom5616.net',16,70,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(35,'Domain','hack9963.top',14,42,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(36,'Hash','a0de0c98123e6f795ddca3041d84597d',NULL,1,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(37,'Hash','7a12efd356ded7127ba5c2b31f889d97',5,25,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(38,'Domain','hack2058.com',6,76,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(39,'Domain','fake1281.top',10,40,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(40,'Domain','hack6948.net',13,32,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(41,'URL','http://threat7345.net/j2c9ogps0132',3,98,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(42,'Hash','08191bb49f5c98d2e49cbbf4c555e7b8',5,98,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(43,'Email','attacker70412@disposable.io',11,94,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(44,'URL','http://crypto7597.xyz/qnvceqfgas0r',9,51,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(45,'Hash','257e4cebed7edc51ae18892919aa688b',17,40,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(46,'Hash','04b8b716f2cf9a51f0e247b25607d7f9',4,16,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(47,'Email','attacker21282@disposable.io',9,33,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(48,'Email','attacker92947@mailnull.com',NULL,89,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(49,'IP','167.98.237.109',7,32,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(50,'IP','236.208.92.162',3,90,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(51,'URL','http://threat7463.net/jv84a1x7ov6s',16,55,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(52,'Hash','2fdd10fa78416a62dbcc34edea633921',15,89,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(53,'Email','attacker69888@mailnull.com',12,40,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(54,'IP','28.162.146.199',1,19,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(55,'Domain','crypto5048.com',6,63,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(56,'IP','18.198.178.107',14,54,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(57,'Hash','98c14e9e5c6d2de40057918fa155e6aa',6,23,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(58,'Domain','dark3245.top',6,65,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(59,'Hash','acbe892be576c216db5ea32f9158c175',12,28,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(60,'Domain','evil2994.net',15,53,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(61,'Email','attacker14313@disposable.io',5,38,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(62,'Hash','8fac37b52a89d6438132e7dae47f057f',18,36,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(63,'URL','http://evil9596.net/rydc1au9dsav',15,63,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(64,'URL','http://threat7037.xyz/n6937xncmldq',2,93,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(65,'IP','155.31.222.136',15,90,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(66,'URL','http://scam7786.online/og983amb3lpv',2,95,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(67,'URL','http://crypto7801.com/0khfsu4se2ky',11,60,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(68,'Hash','d9dce95084a5310d3d2122edaf55b21e',18,62,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(69,'Domain','hack2793.com',18,56,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(70,'Domain','ransom6284.xyz',7,93,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(71,'Hash','bd392861c8520904e56d6f543c632e39',18,86,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(72,'Email','attacker83041@mailnull.com',5,89,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(73,'Domain','threat9842.com',NULL,44,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(74,'Hash','d3a40eb39e8a0f0e218d3d9ccd2cb0be',NULL,83,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(75,'Domain','hack4245.com',8,12,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(76,'IP','88.189.151.240',16,96,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(77,'Email','attacker48201@disposable.io',19,49,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(78,'URL','http://evil9668.online/gnp127exvda4',19,19,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(79,'Domain','scam7468.net',13,37,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(80,'IP','154.81.79.129',18,36,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(81,'Domain','scam4776.top',4,43,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(82,'Domain','hack862.net',17,94,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(83,'URL','http://dark354.online/oprmoc0k7ztd',19,97,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(84,'URL','http://scam2682.online/ezkfh00a0uy9',20,49,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(85,'Domain','evil1574.xyz',17,23,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(86,'IP','251.131.166.87',12,56,'Medium','2026-08-26 12:19:53','2026-08-26 12:19:53'),(87,'Hash','009d0cbc2a6feeff64ad4843cb62a416',7,5,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(88,'Domain','crypto8006.xyz',13,23,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(89,'IP','200.118.221.210',NULL,49,'High','2026-08-26 12:19:53','2026-08-26 12:19:53'),(90,'Hash','c0bf11a5d7bab41a9ea62e7ac7738d4a',1,2,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(91,'IP','22.31.125.165',14,29,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(92,'Email','attacker75102@mailnull.com',15,89,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(93,'Email','attacker23737@mailnull.com',17,83,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(94,'URL','http://threat2052.com/lz5tozo32tc4',11,92,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(95,'Domain','phish2961.online',6,1,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(96,'URL','http://phish642.net/uxdj1dek8g9x',7,39,'Low','2026-08-26 12:19:53','2026-08-26 12:19:53'),(97,'Email','attacker38457@mailnull.com',20,74,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(98,'URL','http://fake5770.online/thd3igk38vhm',20,94,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(99,'IP','141.65.66.98',NULL,21,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53'),(100,'Hash','57486e95a611133d75285a00cad77078',5,33,'Critical','2026-08-26 12:19:53','2026-08-26 12:19:53');
/*!40000 ALTER TABLE `iocs` ENABLE KEYS */;
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
