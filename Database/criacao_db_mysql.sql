-- Criação do banco de dados e uso
CREATE DATABASE IF NOT EXISTS inlytics_db;
USE inlytics_db;

-- Configurações iniciais (mantidas conforme o dump)
SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET unique_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- Tabela: plan_type (não depende de ninguém)
CREATE TABLE `plan_type` (
  `plan_id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(32) DEFAULT NULL,
  `plan_description` varchar(128) DEFAULT NULL,
  `value` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`plan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: enterprise (depende de plan_type)
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

-- Tabela: customer (depende de enterprise)
CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL COMMENT 'talvez mudar o tamanho',
  `churn` decimal(5,2) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL COMMENT 'M/F',
  `birth_date` date NOT NULL,
  `time_as_client` datetime DEFAULT current_timestamp() COMMENT 'talvez seja necessário separar em time_as_client_start e time_as_client_end',
  `preferred_payment_type` char(3) NOT NULL COMMENT 'CRD DEB PIX VIS',
  `frequent_dispositive` char(3) NOT NULL COMMENT 'COM TEL TBT',
  `satisfaction_score` decimal(5,2) DEFAULT NULL,
  `cupom_used` tinyint(1) DEFAULT 0,
  `complained` tinyint(1) DEFAULT 0,
  `dispositives_num` int(3) DEFAULT NULL COMMENT '0-999',
  `id_enterprise` int(11) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: inlytic_user (depende de enterprise)
CREATE TABLE `inlytic_user` (
  `id_inlytic_user` int(11) NOT NULL AUTO_INCREMENT,
  `id_enterprise` int(11) DEFAULT NULL,
  `worker_name` varchar(32) DEFAULT NULL,
  `sector` varchar(32) DEFAULT NULL,
  `worker_email` varchar(32) DEFAULT NULL,
  `login_password` varchar(16) DEFAULT NULL,
  `photo_url` varchar(255) DEFAULT NULL,  -- Coluna para o link da foto
  PRIMARY KEY (`id_inlytic_user`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `inlytic_user_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Tabela: venda dos produtos 
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

-- Tabela: churn (depende de customer e enterprise)
CREATE TABLE `churn` (
  `id_customer` int(11) NOT NULL,
  `id_enterprise` int(11) NOT NULL,
  `loss_probabilty` decimal(5,2) DEFAULT NULL,
  KEY `id_customer` (`id_customer`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `churn_ibfk_1` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `churn_ibfk_2` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: rfm (depende de customer e enterprise)
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

-- Tabela: seasonality (depende de enterprise)
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

-- Restauração de configurações
SET foreign_key_checks = 1;
SET unique_checks = 1;
