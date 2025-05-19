DROP DATABASE IF EXISTS Inlytics;
CREATE DATABASE Inlytics;

USE Inlytics;


CREATE TABLE `plan_type` (
  `plan_id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(32) DEFAULT NULL,
  `plan_description` varchar(128) DEFAULT NULL,
  `value` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`plan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



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



CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `churn` decimal(5,2) DEFAULT NULL,
  `gender` char(6) DEFAULT NULL,
  `tenure` decimal(3,1) DEFAULT NULL,
  `preferred_payment_type` varchar(30) DEFAULT NULL,
  `frequent_dispositive` varchar(32) DEFAULT NULL,
  `satisfaction_score` decimal(5,2) DEFAULT NULL,
  `marital_status` varchar(32) DEFAULT NULL,
  `cupom_used` int(3) DEFAULT 0,
  `complained` int(3) DEFAULT 0,
  `dispositives_num` int(3) DEFAULT NULL,
  `id_enterprise` int(11) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `churn` (
  `id_customer` int(11) NOT NULL,
  `id_enterprise` int(11) NOT NULL,
  `loss_probabilty` decimal(5,2) DEFAULT NULL,
  KEY `id_customer` (`id_customer`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `churn_ibfk_1` FOREIGN KEY (`id_customer`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `churn_ibfk_2` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `inlytic_user` (
  `id_inlytic_user` int(11) NOT NULL AUTO_INCREMENT,
  `id_enterprise` int(11) DEFAULT NULL,
  `worker_name` varchar(32) DEFAULT NULL,
  `sector` varchar(32) DEFAULT NULL,
  `worker_email` varchar(32) DEFAULT NULL,
  `login_password` varchar(255) DEFAULT NULL,
  `photo_url` varchar(255) DEFAULT NULL,  -- Coluna para o link da foto
  PRIMARY KEY (`id_inlytic_user`),
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `inlytic_user_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `rfm` (
  `id_rfm` int(11) NOT NULL AUTO_INCREMENT,
  `recency` int(11) DEFAULT NULL,
  `frequencey` int(11) DEFAULT NULL,
  `monetary` int(11) DEFAULT NULL,
  `customer_classification` varchar(20) DEFAULT NULL,
  `customer_id` int(11) NOT NULL,
  `enterprise_id` int(11) NOT NULL,
  `r_score` int(11) NOT NULL,
  `f_score` int(11) NOT NULL,
  `m_score` int(11) NOT NULL,
  PRIMARY KEY (`id_rfm`),
  KEY `customer_id` (`customer_id`),
  KEY `enterprise_id` (`enterprise_id`),
  CONSTRAINT `rfm_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `rfm_ibfk_2` FOREIGN KEY (`enterprise_id`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;






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


CREATE TABLE `sold_products` (
  `id_sold_products` int(11) NOT NULL,
  `invoice` int(11) DEFAULT NULL,
  `id_customer` int(11) DEFAULT NULL,
  `product_desc` varchar(128) NOT NULL,
  `product_price` decimal(10,2) NOT NULL,
  `stock_code` varchar(20) NOT NULL,
  `invoice_date` datetime,
  `quantity` int(10) NOT NULL,
  `country` varchar(32) DEFAULT NULL,
  `id_enterprise` int(11) DEFAULT NULL,
  KEY `id_enterprise` (`id_enterprise`),
  CONSTRAINT `sold_products_ibfk_1` FOREIGN KEY (`id_enterprise`) REFERENCES `enterprise` (`id_enterprise`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;





