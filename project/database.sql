CREATE DATABASE  IF NOT EXISTS `foodah_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `foodah_database`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: foodah_database
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `cart_items`
--

DROP TABLE IF EXISTS `cart_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_items` (
  `cart_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `order_id` bigint DEFAULT NULL,
  `created_at` timestamp NOT NULL,
  `quantity` int NOT NULL,
  `temp_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `cart_items_product_id_foreign` (`product_id`),
  KEY `cart_items_user_id_foreign` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_items`
--

LOCK TABLES `cart_items` WRITE;
/*!40000 ALTER TABLE `cart_items` DISABLE KEYS */;
INSERT INTO `cart_items` VALUES (34,9,26,NULL,'2025-05-27 09:33:11',2,'89192993-2bc3-4cb6-bbf0-c209a3bf53c6'),(35,10,26,NULL,'2025-05-27 09:33:11',1,'71e5ae44-2610-4808-a7ca-50d12997f7a1'),(36,11,26,NULL,'2025-05-27 09:33:11',1,'5f213b1b-8aa1-4414-a254-0e2b2a678d5d'),(39,11,5,14,'2025-05-27 10:53:52',1,'28810145-1c4f-4992-8ce3-02efa6e8d333'),(40,9,5,14,'2025-05-27 10:53:52',1,'30f89dcf-7f30-4211-b9ab-da40ceb40c0b'),(41,16,5,14,'2025-05-27 10:53:52',1,'771bbca0-e0d3-4283-b113-0363c0fa6e92'),(48,10,27,15,'2025-05-27 12:02:30',2,'c2769e22-5bad-4186-be24-e826ced0c56b'),(49,14,27,15,'2025-05-27 12:02:30',1,'53ea9c86-44d2-48ae-a543-51b8b5be4179'),(50,9,5,16,'2025-05-27 12:02:30',1,'90f5ce4e-2a37-4f8a-bc07-429de4c745d6'),(51,10,5,16,'2025-05-27 12:02:30',1,'fcd5559e-30f3-4da0-aaef-94d4ba196388'),(52,11,5,16,'2025-05-27 12:02:30',1,'c1899724-83ce-4a89-97b8-03e43502b3bc');
/*!40000 ALTER TABLE `cart_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Main Dish'),(2,'Dessert'),(3,'Snack'),(4,'Beverage'),(6,'Indigenous');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_driver`
--

DROP TABLE IF EXISTS `delivery_driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_driver` (
  `driver_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `vehicle_type` varchar(255) NOT NULL,
  `license_number` varchar(255) NOT NULL,
  `vehicle_plate` varchar(255) NOT NULL,
  `is_available` tinyint(1) NOT NULL DEFAULT '1',
  `driver_rating` decimal(8,2) NOT NULL,
  `total_deliveries` int NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  PRIMARY KEY (`driver_id`),
  KEY `delivery_driver_user_id_foreign` (`user_id`),
  CONSTRAINT `delivery_driver_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `user_table` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_driver`
--

LOCK TABLES `delivery_driver` WRITE;
/*!40000 ALTER TABLE `delivery_driver` DISABLE KEYS */;
INSERT INTO `delivery_driver` VALUES (1,6,'Scooter','123456789','123-ABC',0,5.00,1,'2025-05-18 07:03:07','2025-05-18 07:03:07'),(2,18,'Bicycle','88877-AAA','Not applicable',1,5.00,0,'2025-05-24 12:42:42','2025-05-24 12:42:42'),(3,23,'Carloo','888AAA888AAA','XXX123',1,5.00,0,'2025-05-25 01:24:46','2025-05-25 01:24:46'),(4,24,'4x4','PH12345','1234ABC',0,5.00,0,'2025-05-25 02:44:16','2025-05-25 02:44:16');
/*!40000 ALTER TABLE `delivery_driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_table`
--

DROP TABLE IF EXISTS `order_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_table` (
  `order_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `driver_id` bigint unsigned DEFAULT NULL,
  `address_id` bigint unsigned DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  `total_price` decimal(8,2) NOT NULL,
  `payment_status` varchar(255) NOT NULL,
  `payment_method` varchar(255) NOT NULL,
  `placed_at` timestamp NOT NULL,
  `delivered_at` timestamp NULL DEFAULT NULL,
  `canceled_at` timestamp NULL DEFAULT NULL,
  `notes` text,
  `payment_invoice` varchar(45) DEFAULT NULL,
  `delivery_option` varchar(45) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `order_table_driver_id_foreign` (`driver_id`),
  KEY `order_table_user_id_foreign` (`user_id`),
  KEY `order_table_address_id_foreign` (`address_id`),
  CONSTRAINT `order_table_address_id_foreign` FOREIGN KEY (`address_id`) REFERENCES `user_address` (`address_id`),
  CONSTRAINT `order_table_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `delivery_driver` (`driver_id`),
  CONSTRAINT `order_table_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `user_table` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_table`
--

LOCK TABLES `order_table` WRITE;
/*!40000 ALTER TABLE `order_table` DISABLE KEYS */;
INSERT INTO `order_table` VALUES (14,5,1,1,'Completed',104.99,'','Credit Card','2025-05-27 10:53:52','2025-05-27 15:28:02','2025-05-27 15:28:02','','52025-05-27 20:53:52',NULL,'Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia'),(15,27,2,10,'Completed',117.50,'','Credit Card','2025-05-27 12:02:30',NULL,NULL,'','272025-05-27 22:02:30',NULL,'12, Kelvin, Grove, Brisbane, QLD, 4059, Australia'),(16,5,NULL,1,'Pending',129.99,'','Credit Card','2025-05-27 12:02:30',NULL,NULL,'','52025-05-27 22:02:30',NULL,'Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia');
/*!40000 ALTER TABLE `order_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_table`
--

DROP TABLE IF EXISTS `product_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_table` (
  `product_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `category` varchar(255) NOT NULL,
  `price` decimal(8,2) NOT NULL,
  `food_rating` decimal(8,2) NOT NULL,
  `prep_time_est` varchar(255) NOT NULL,
  `food_image_url` text NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  `restaurant_id` bigint unsigned DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`product_id`),
  KEY `product_table_ownser_id_foreign` (`restaurant_id`),
  CONSTRAINT `product_table_ownser_id_foreign` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_table`
--

LOCK TABLES `product_table` WRITE;
/*!40000 ALTER TABLE `product_table` DISABLE KEYS */;
INSERT INTO `product_table` VALUES (1,'Pizza lang','Delicious Pizza promise swear','1',12.99,5.00,'15','chicken-red-curry-black-cup.jpg',1,'2025-05-14 00:12:11','2025-05-14 00:12:11',1,1),(2,'Burger','Juicy beef burger','1',9.99,100.00,'20','chicken-red-curry-black-cup.jpg',1,'2025-05-17 09:44:44','2025-05-17 09:44:44',1,1),(3,'Kwazan','Croissant is the new Kwazan','1',2.99,100.00,'20','chicken-red-curry-black-cup.jpg',1,'2025-05-17 09:44:44','2025-05-17 09:44:44',1,1),(7,'Chicken barbecue','The best barbie ever in Brisbane','1',12.99,100.00,'20','chicken-red-curry-black-cup.jpg',1,'2025-05-17 09:48:21','2025-05-17 09:48:21',2,1),(8,'basta pagkain','Masarap to pramis','4',500.00,100.00,'10','ace.jpg',1,'2025-05-26 01:54:30','2025-05-26 01:54:30',1,1),(9,'Streak Frites','A classic French and Belgian dish consisting of a beef steak served with crispy French fries.','1',49.99,100.00,'10','SteakFrites.jpeg',1,'2025-05-26 06:08:51','2025-05-26 06:08:51',1,0),(10,'Beef Bulgogi','A popular Korean dish consisting of thinly sliced marinated beef, most commonly cooked over a grill or in a pan.','1',40.00,100.00,'10','BeefBulgogi.jpeg',1,'2025-05-26 06:36:55','2025-05-26 06:36:55',1,0),(11,'Roast Rib','Also known as Prime Rib, it’s a beef cut that’s incredibly succulent with superior taste.','1',40.00,100.00,'10','roastrib.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(12,'Chicken Parmigiana','Pollo alla parmigiana in Italian, but affectionately referred by Aussies as Parma, Parmi or “a schnitty with tomato sauce and cheese”.','1',37.50,100.00,'10','chicken-parmigiana.jpeg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(13,'Scugnizzi','Typically made by frying strips or pieces of pizza dough, which are then often served with fresh ingredients like tomatoes, basil, and rocket.','3',18.00,100.00,'10','scugnizzi.jpg',1,'2025-05-26 06:52:06','2025-05-26 06:52:06',1,1),(14,'Chicken Biryani','A popular South Asian dish that combines marinated chicken with a flavorful blend of rice, spices, and herbs, often served at celebrations. ','1',37.50,100.00,'10','chicken-biryani.jpeg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(15,'Buffalo Wings','A popular American dish consisting of deep-fried, unbreaded chicken wings (or drumettes) coated in a sauce made with a vinegar-based cayenne pepper hot sauce and melted butter.','1',25.00,100.00,'10','buffalo-wings.jpeg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(16,'Herb French Fries','Garnished or served with fresh herbs, like parsley, coriander, or rosemary.','2',15.00,100.00,'10','fries.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(17,'Humpty Dumpty Burger','Topped with caramelized onions to add a sweet and smoky twist, melted burger cheese, and a runny egg.','3',19.99,100.00,'10','humptydumpty-burger.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(18,'Ham and Cheese Pizza','A popular Italian-American dish consisting of a flatbread base, tomato sauce, melted cheese, and sliced ham.','3',30.75,100.00,'10','pizza.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(19,'Soft Taco','Taco made with a soft tortilla, typically a flour tortilla, instead of a crispy, fried tortilla shell.','3',21.50,100.00,'10','soft-taco.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(20,'Pretzel Sticks','Typically made from a dough similar to traditional pretzels, shaped into long, thin sticks, and often sprinkled with salt.','3',13.90,100.00,'10','pretzel-sticks.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(21,'Fried Calamari','A dish in Mediterranean cuisine, consisting of batter-coated, deep-fried squid (fried for less than two minutes to prevent toughness), which is served plain, with salt and lemon on the side.','3',15.00,100.00,'10','calamari.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(22,'Blueberry Pancake','Made with a standard pancake batter, incorporating fresh or frozen blueberries that are either folded into the batter or placed on top of the pancake while cooking. ','2',22.50,100.00,'10','blueberry-pancake.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(23,'Matcha Green Tea Ice Cream','Ice cream infused with matcha powder, a fine, bright green powder made from ground green tea leaves.','2',26.00,100.00,'10','matcha-icecream.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(24,'Tiramisu','A variation of the classic Italian tiramisu dessert, featuring a chocolate twist.','2',28.00,100.00,'10','tiramisu.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(25,'Lemon Iced Tea','Refreshing beverage made by combining black tea, lemon, and ice.','4',15.00,100.00,'10','lemon-icedtea.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(26,'Cola','Carbonated soft drink known for its distinct sweet and fizzy taste.','4',15.00,100.00,'10','cola.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0),(27,'Wine','Alcoholic beverage primarily made from the fermented juice of grapes.','4',17.00,100.00,'10','wine.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',1,0);
/*!40000 ALTER TABLE `product_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `restaurant_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `owner_id` bigint unsigned NOT NULL,
  `restaurant_name` varchar(45) NOT NULL,
  `is_indigenous` tinyint NOT NULL,
  `address` varchar(45) NOT NULL,
  `is_active` tinyint NOT NULL,
  `created_at` varchar(45) NOT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `website` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `image_url` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `restaurant_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `user_table` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (1,7,'Kapehan ni Adreyan',1,'Etivac, Phils',1,'2025-05-14 10:08:56',NULL,NULL,NULL,NULL,NULL),(2,7,'Manokan ni Adriyan',0,'South Brisbane, Queensland',1,'2025-05-17 19:47:58',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_address`
--

DROP TABLE IF EXISTS `user_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_address` (
  `address_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `label` varchar(255) NOT NULL,
  `address_line1` varchar(255) NOT NULL,
  `address_line2` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `postal_code` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `user_address_user_id_foreign` (`user_id`),
  CONSTRAINT `user_address_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `user_table` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_address`
--

LOCK TABLES `user_address` WRITE;
/*!40000 ALTER TABLE `user_address` DISABLE KEYS */;
INSERT INTO `user_address` VALUES (1,5,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(2,10,'White House','Block 10','Small County','District of Col','Washington','4000','USA','2025-05-22 13:35:00','2025-05-22 13:35:00'),(3,22,'56','Baratie','East Blue','Sabaodi','Grandline','5000','Albasta','2025-05-25 01:23:57','2025-05-25 01:23:57'),(4,23,'No Label','Blake Street','Red Mountain','Big Apple City','Arizona','6000','Biringan','2025-05-25 01:24:46','2025-05-25 01:24:46'),(5,24,'502','Butuan City','Butuan City','Butuan','ADN','8600','Philippines','2025-05-25 02:44:16','2025-05-25 02:44:16'),(6,8,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(7,6,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(8,25,'123','Kelvin','Grove','Brisbane','QLD','4059','Australia','2025-05-27 08:43:16','2025-05-27 08:43:16'),(9,26,'123','Kelvin','Grove','Brisbane','QLD','4059','Australia','2025-05-27 08:51:14','2025-05-27 08:51:14'),(10,27,'12','Kelvin','Grove','Brisbane','QLD','4059','Australia','2025-05-27 12:02:30','2025-05-27 12:02:30');
/*!40000 ALTER TABLE `user_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_table`
--

DROP TABLE IF EXISTS `user_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_table` (
  `user_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `profile_picture_url` text NOT NULL,
  `user_type` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  `last_login` timestamp NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_table`
--

LOCK TABLES `user_table` WRITE;
/*!40000 ALTER TABLE `user_table` DISABLE KEYS */;
INSERT INTO `user_table` VALUES (1,'Junnie Boy','junnie@foodah.com','+61000111222','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','zoro.jpg','Admin',1,1,'2025-05-13 23:18:20','2025-05-13 23:18:20','2025-05-13 23:18:20'),(5,'Jamizan Angkol','jamizan@foodah.com','+6112345678','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','zoro.jpg','Customer',1,1,'2025-05-13 23:20:58','2025-05-13 23:20:58','2025-05-13 23:20:58'),(6,'Tomasino Bakero','tomasen@foodah.com','+61999888777','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','zoro.jpg','Delivery Driver',1,1,'2025-05-13 23:21:42','2025-05-13 23:21:42','2025-05-13 23:21:42'),(7,'Adriano Restoranto','adrian@foodah.com','+61987654321','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','zoro.jpg','Restaurant Manager',1,1,'2025-05-14 00:06:07','2025-05-14 00:06:07','2025-05-14 00:06:07'),(8,'admin','admin@foodah.com','610000000','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','zoro.jpg','Admin',1,1,'2025-05-17 04:16:20','2025-05-17 04:16:20','2025-05-17 04:16:20'),(9,'Tony Chopper','tony@foodah.com','09777968166','scrypt:32768:8:1$zRIKWVTmKGvdqHYm$1d2fb305042d1ed8d4914692321486a3aacab3ecdc7cb03345bc0a4c886c2b257f3de9818b3883e9a87673e2c91892fdf241673daffb5d790c8580c69061542f','zoro.jpg','Customer',1,1,'2025-05-20 02:28:16','2025-05-20 02:28:16','2025-05-20 02:28:16'),(10,'Nico Robin Chan','robin@foodah.com','+6155522266','scrypt:32768:8:1$t5z5WXMfLPqUbocC$f6dc23b40a45944bbe5050054fe86ca474a566b1e53d6a1d6aa903d9cdebce21c85bce30f257d98d442d8ce1b1e82fe4cb96ac17f7ca0262a48ca5ac24ab20e0','zoro.jpg','Customer',1,1,'2025-05-20 06:23:36','2025-05-20 06:23:36','2025-05-20 06:23:36'),(18,'Roronoa Zoro','zoro@foodah.com','+6155566677','scrypt:32768:8:1$wvs1rBa3yiJLn78t$b66e12a2b880dd1a81d49d7ac79ed081dbf61fbc6d690bd556443311991f4c718a5b30f7ec1e264928617b961c5d1f29e7738ebe63dacb395902e519c10734db','zoro.jpg','Delivery Driver',1,1,'2025-05-24 12:42:42','2025-05-24 12:42:42','2025-05-24 12:42:42'),(22,'Vinsmoke Sanji','sanji@foodah.com','+6399988887','scrypt:32768:8:1$ulZiglADiDd330Fq$233c8da365c49bb47ff2ac56978c543b296d38995ed4b6e62f7a9db3644f59a1fb7cdf16c5c5b04c5f53e296f388d9a0c84034664e1d18e73b5c0c8db0f2a07f','zoro.jpg','Customer',1,1,'2025-05-25 01:23:57','2025-05-25 01:23:57','2025-05-25 01:23:57'),(23,'Boy Panda','boypanda@foodah.com','+999888899','scrypt:32768:8:1$tkNwE5jBdqkVzWjZ$5940fd2f2dfac3c64e08e098d8496b757d7f6298b44b673f0a8995b050cb192a3db80bd6f24eb83608b76b0245cfbaa27180be36d962795374152afdaa09f064','zoro.jpg','Delivery Driver',1,1,'2025-05-25 01:24:46','2025-05-25 01:24:46','2025-05-25 01:24:46'),(24,'Lilo and Stitch','liloandstitch@gmail.com','123456789','scrypt:32768:8:1$mnSyop8DFRbo5qcj$d975b77bab3c9ff2f7abf770bc86130372fe267a917576db7ad3444c2bd1a6cc14ea2aa9c9a41f047443f52f94ba6c99233cf1b83a3865ab9b8f58d22f9a7506','zoro.jpg','Delivery Driver',1,1,'2025-05-25 02:44:16','2025-05-25 02:44:16','2025-05-25 02:44:16'),(25,'Wano Kuni','wanokuni@foodah.com','1234567890','scrypt:32768:8:1$aAFKwXSTeOnmL4nt$8f2e4cac0548f9ef69565dd60468754481585864976243a23f743751e2e0d6b343aacc9cd93b8a91140c7cdfcfbde46a2e9068120802b9de709c6b87961e357c','blank_profile.png','Customer',1,1,'2025-05-27 08:43:16','2025-05-27 08:43:16','2025-05-27 08:43:16'),(26,'Luffytaro','luffytaro@foodah.com','12345461631','scrypt:32768:8:1$9Qr1VrsYZyye3RR3$907c293d987af40cc3db0c39721cae0f1d9d18fbf61f2cbdbef30916ce5e75fc4f3b6f3547529061be495fb3aed9b62b4686597362618e803fdff75f55341508','download.jpg','Customer',1,1,'2025-05-27 08:51:14','2025-05-27 08:51:14','2025-05-27 08:51:14'),(27,'Adrian Abubakhar','abubakhar@foodah.com','12345','scrypt:32768:8:1$j0O3oOtwINrTqn11$bcf98a1ffd8a54afb36903e724ceb2a839453fc0a8fda333efabcc7c40d3b5a31465ca1746185a367cc0378af2de8ec20a952abfc4b7aef39fa893f48340be1d','blank_profile.png','Customer',1,1,'2025-05-27 12:02:30','2025-05-27 12:02:30','2025-05-27 12:02:30');
/*!40000 ALTER TABLE `user_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `users`
--

DROP TABLE IF EXISTS `users`;
/*!50001 DROP VIEW IF EXISTS `users`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `users` AS SELECT 
 1 AS `user_id`,
 1 AS `fullname`,
 1 AS `email`,
 1 AS `phone_number`,
 1 AS `password_hash`,
 1 AS `profile_picture_url`,
 1 AS `user_type`,
 1 AS `is_active`,
 1 AS `is_verified`,
 1 AS `created_at`,
 1 AS `updated_at`,
 1 AS `last_login`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `users_view`
--

DROP TABLE IF EXISTS `users_view`;
/*!50001 DROP VIEW IF EXISTS `users_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `users_view` AS SELECT 
 1 AS `user_id`,
 1 AS `fullname`,
 1 AS `email`,
 1 AS `phone_number`,
 1 AS `password_hash`,
 1 AS `profile_picture_url`,
 1 AS `user_type`,
 1 AS `is_active`,
 1 AS `is_verified`,
 1 AS `created_at`,
 1 AS `updated_at`,
 1 AS `last_login`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `users`
--

/*!50001 DROP VIEW IF EXISTS `users`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `users` AS select `user_table`.`user_id` AS `user_id`,`user_table`.`fullname` AS `fullname`,`user_table`.`email` AS `email`,`user_table`.`phone_number` AS `phone_number`,`user_table`.`password_hash` AS `password_hash`,`user_table`.`profile_picture_url` AS `profile_picture_url`,`user_table`.`user_type` AS `user_type`,`user_table`.`is_active` AS `is_active`,`user_table`.`is_verified` AS `is_verified`,`user_table`.`created_at` AS `created_at`,`user_table`.`updated_at` AS `updated_at`,`user_table`.`last_login` AS `last_login` from `user_table` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `users_view`
--

/*!50001 DROP VIEW IF EXISTS `users_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `users_view` AS select `user_table`.`user_id` AS `user_id`,`user_table`.`fullname` AS `fullname`,`user_table`.`email` AS `email`,`user_table`.`phone_number` AS `phone_number`,`user_table`.`password_hash` AS `password_hash`,`user_table`.`profile_picture_url` AS `profile_picture_url`,`user_table`.`user_type` AS `user_type`,`user_table`.`is_active` AS `is_active`,`user_table`.`is_verified` AS `is_verified`,`user_table`.`created_at` AS `created_at`,`user_table`.`updated_at` AS `updated_at`,`user_table`.`last_login` AS `last_login` from `user_table` limit 0,2 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-28  8:54:56
