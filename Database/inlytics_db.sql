/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: inlytics
-- ------------------------------------------------------
-- Server version	11.7.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `churn`
--

--DROP TABLE IF EXISTS `churn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `churn` (
  `id_customer` int(11) NOT NULL,
  `id_enterprise` int(11) NOT NULL,
  `loss_probabilty` decimal(5,2) DEFAULT NULL,
  KEY `id_customer` (`id_customer`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `churn_ibfk_1` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `churn_ibfk_2` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `churn`
--

LOCK TABLES `churn` WRITE;
/*!40000 ALTER TABLE `churn` DISABLE KEYS */;
/*!40000 ALTER TABLE `churn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

--DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL COMMENT 'talvez mudar o tamanho',
  `churn` decimal(5,2) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL COMMENT 'M/F',
  `birth_date` date NOT NULL,
  `time_as_client` datetime DEFAULT current_timestamp() COMMENT 'talvez seja necessário separar em time_as_client_start e time_as_client_end, pois: \na gente tem que saber quando o client loga na conta e quando ele desloga da conta',
  `preferred_payment_type` char(3) NOT NULL COMMENT 'como eu pensei: CRD DEB PIX VIS',
  `frequent_dispositive` char(3) NOT NULL COMMENT 'como eu pensei: COM TEL TBT',
  `satisfaction_score` decimal(5,2) DEFAULT NULL,
  `cupom_used` tinyint(1) DEFAULT 0,
  `complained` tinyint(1) DEFAULT 0,
  `dispositives_num` int(3) DEFAULT NULL COMMENT 'isso daqui vai de 0-999, talvez eu tenha que diminuir um pouco',
  `id_enterprise` int(11) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enterprise`
--

--DROP TABLE IF EXISTS `enterprise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `enterprise` (
  `id_enterprise` int(11) NOT NULL AUTO_INCREMENT,
  `enterprise_name` varchar(32) DEFAULT NULL,
  `enterprise_host` char(12) DEFAULT NULL,
  `enterprise_user` varchar(100) DEFAULT NULL COMMENT 'maybe change later',
  `enterprise_pass` varchar(100) DEFAULT NULL COMMENT 'maybe change later',
  `cnpj` char(14) DEFAULT NULL,
  `plan_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_enterprise`),
  KEY `plan_id` (`plan_id`),
  CONSTRAINT `enterprise_ibfk_1` FOREIGN KEY (`plan_id`) REFERENCES `plan_type` (`plan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enterprise`
--

LOCK TABLES `enterprise` WRITE;
/*!40000 ALTER TABLE `enterprise` DISABLE KEYS */;
/*!40000 ALTER TABLE `enterprise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inlytic_user`
--

--DROP TABLE IF EXISTS `inlytic_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `inlytic_user` (
  `id_inlytic_user` int(11) NOT NULL AUTO_INCREMENT,
  `id_enterprise` int(11) DEFAULT NULL,
  `worker_name` varchar(32) DEFAULT NULL,
  `sector` varchar(32) DEFAULT NULL,
  `worker_email` varchar(32) DEFAULT NULL,
  `login_password` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id_inlytic_user`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `inlytic_user_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inlytic_user`
--

LOCK TABLES `inlytic_user` WRITE;
/*!40000 ALTER TABLE `inlytic_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `inlytic_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plan_type`
--

--DROP TABLE IF EXISTS `plan_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `plan_type` (
  `plan_id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(32) DEFAULT NULL,
  `plan_description` varchar(128) DEFAULT NULL,
  `value` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`plan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plan_type`
--

LOCK TABLES `plan_type` WRITE;
/*!40000 ALTER TABLE `plan_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `plan_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rfm`
--

--DROP TABLE IF EXISTS `rfm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rfm` (
  `id_rfm` int(11) NOT NULL AUTO_INCREMENT,
  `recency` int(11) DEFAULT NULL,
  `frequencey` int(11) DEFAULT NULL,
  `monetary` int(11) DEFAULT NULL,
  `customer_classification` varchar(20) DEFAULT NULL,
  `customer_id` int(11) NOT NULL,
  `enterprise_id` int(11) NOT NULL,
  PRIMARY KEY (`id_rfm`),
  KEY `customer_id` (`customer_id`),
  KEY `enterprise_id` (`enterprise_id`),
  CONSTRAINT `rfm_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `rfm_ibfk_2` FOREIGN KEY (`enterprise_id`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rfm`
--

LOCK TABLES `rfm` WRITE;
/*!40000 ALTER TABLE `rfm` DISABLE KEYS */;
/*!40000 ALTER TABLE `rfm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seasonality`
--

--DROP TABLE IF EXISTS `seasonality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonality` (
  `id_seasonality` int(11) NOT NULL AUTO_INCREMENT,
  `id_enterprise` int(11) NOT NULL,
  `holiday_date` date NOT NULL,
  `holiday_description` varchar(128) NOT NULL,
  `holiday_date_end` date NOT NULL,
  `total_products` int(11) NOT NULL,
  PRIMARY KEY (`id_seasonality`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `seasonality_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seasonality`
--

LOCK TABLES `seasonality` WRITE;
/*!40000 ALTER TABLE `seasonality` DISABLE KEYS */;
/*!40000 ALTER TABLE `seasonality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sold_products`
--

--DROP TABLE IF EXISTS `sold_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sold_products` (
  `id_sold_products` int(11) NOT NULL,
  `id_tax` int(11) DEFAULT NULL,
  `id_customer` int(11) DEFAULT NULL,
  `product_name` varchar(32) DEFAULT NULL,
  `product_desc` varchar(128) NOT NULL COMMENT 'dá pra escrever muita coisa com esse tanto',
  `product_price` decimal(5,2) NOT NULL,
  `bill_emission` datetime NOT NULL,
  `id_enterprise` int(11) DEFAULT NULL,
  `id_product` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_sold_products`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `sold_products_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sold_products`
--

LOCK TABLES `sold_products` WRITE;
/*!40000 ALTER TABLE `sold_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `sold_products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-28 14:46:57
