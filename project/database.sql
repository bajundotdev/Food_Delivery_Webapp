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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_items`
--

LOCK TABLES `cart_items` WRITE;
/*!40000 ALTER TABLE `cart_items` DISABLE KEYS */;
INSERT INTO `cart_items` VALUES (1,10,5,1,'2025-05-30 11:31:47',1,'5d96fc79-2a8d-4aa5-9d7f-a7c64817b2e2'),(2,11,5,1,'2025-05-30 11:31:47',1,'f731c91a-ce25-4987-86dc-3439559e00ae'),(3,11,5,2,'2025-05-30 11:46:41',1,'6944b80b-523f-4f97-8413-ac7dd51deb26'),(11,12,5,23,'2025-05-30 13:04:15',1,'6d1d9588-cc6f-446c-829c-9c645e1d62b2'),(12,10,5,24,'2025-05-30 13:59:47',1,'3d0a1dd6-5a22-42d7-aa38-a7eccd47bee5'),(13,11,5,24,'2025-05-30 13:59:47',1,'1a1d8431-ff82-4a17-af67-02b5316b69d2'),(14,12,5,24,'2025-05-30 13:59:47',1,'f9b624ca-2762-4992-8089-e127d8170c2e'),(15,17,5,25,'2025-05-30 13:59:47',1,'21691759-94b9-4c88-b580-14662684a595'),(16,18,5,25,'2025-05-30 13:59:47',1,'68892a95-4b46-474b-b3fc-74962e048363'),(17,19,5,25,'2025-05-30 13:59:47',1,'c3f51cd2-a6b6-4c42-811b-ceb984bc09c1'),(18,10,5,26,'2025-05-30 13:59:47',1,'fdfb8bbd-2503-424f-8c09-3dcd85370c5c'),(20,10,5,27,'2025-05-31 00:28:37',1,'00d82b10-c87c-46d2-abef-ff9ce06042dd');
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
INSERT INTO `delivery_driver` VALUES (1,6,'Scooter','123456789','123-ABC',1,5.00,1,'2025-05-18 07:03:07','2025-05-18 07:03:07');
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
  `packaging_method` varchar(45) DEFAULT NULL,
  `cancellation_notes` varchar(255) DEFAULT NULL,
  `order_confirm` int DEFAULT NULL,
  `shipping_fee` double(8,2) NOT NULL DEFAULT '0.00',
  `packaging_fee` double(8,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`order_id`),
  KEY `order_table_driver_id_foreign` (`driver_id`),
  KEY `order_table_user_id_foreign` (`user_id`),
  KEY `order_table_address_id_foreign` (`address_id`),
  CONSTRAINT `order_table_address_id_foreign` FOREIGN KEY (`address_id`) REFERENCES `user_address` (`address_id`),
  CONSTRAINT `order_table_driver_id_foreign` FOREIGN KEY (`driver_id`) REFERENCES `delivery_driver` (`driver_id`),
  CONSTRAINT `order_table_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `user_table` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_table`
--

LOCK TABLES `order_table` WRITE;
/*!40000 ALTER TABLE `order_table` DISABLE KEYS */;
INSERT INTO `order_table` VALUES (1,5,1,1,'Completed',88.98,'','Credit Card','2025-05-30 11:31:47','2025-05-30 12:14:24','2025-05-30 12:14:24','','52025-05-30 21:31:47','express','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','standard',NULL,1,5.99,2.99),(2,5,1,1,'Cancelled',40.00,'Not successful','Credit Card','2025-05-30 11:46:41','2025-05-30 12:43:45','2025-05-30 12:49:06','','52025-05-30 21:46:41','standard','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','eco_friendly','delayed',1,0.00,0.00),(23,5,1,1,'Cancelled',37.50,'Not successful','Credit Card','2025-05-30 13:04:15','2025-05-30 13:04:15','2025-05-30 13:04:15','','52025-05-30 23:04:15','standard','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','eco_friendly','soafer delay kaayo',1,0.00,0.00),(24,5,NULL,1,'Pending',126.48,'','Credit Card','2025-05-30 13:59:47',NULL,NULL,'','52025-05-30 23:59:47','express','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','standard',NULL,1,5.99,2.99),(25,5,NULL,1,'In Progress',84.22,'','Debit Card','2025-05-30 13:59:47',NULL,NULL,'','52025-05-30 23:59:47','express','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','discreet_confidential',NULL,1,5.99,5.99),(26,5,NULL,1,'Pending',48.98,'','Credit Card','2025-05-30 13:59:47',NULL,NULL,'','52025-05-30 23:59:47','express','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','standard',NULL,1,5.99,2.99),(27,5,NULL,1,'Pending',45.99,'','Credit Card','2025-05-31 00:28:39',NULL,NULL,'','52025-05-31 10:28:37','express','Iglu, 62 Blamey St., Kelvin Grove, Brisbane, Queensland, 4509, Australia','eco_friendly',NULL,1,5.99,0.00);
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
  `deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_table`
--

LOCK TABLES `product_table` WRITE;
/*!40000 ALTER TABLE `product_table` DISABLE KEYS */;
INSERT INTO `product_table` VALUES (1,'Pizza lang','Delicious Pizza promise swear','1',12.99,5.00,'15','chicken-red-curry-black-cup.jpg',1,'2025-05-14 00:12:11','2025-05-14 00:12:11',1),(2,'Burger','Juicy beef burger','1',9.99,100.00,'20','chicken-red-curry-black-cup.jpg',1,'2025-05-17 09:44:44','2025-05-17 09:44:44',1),(3,'Kwazan','Croissant is the new Kwazan','1',2.99,100.00,'20','chicken-red-curry-black-cup.jpg',1,'2025-05-17 09:44:44','2025-05-17 09:44:44',1),(7,'Chicken barbecue','The best barbie ever in Brisbane','1',12.99,100.00,'20','chicken-red-curry-black-cup.jpg',1,'2025-05-17 09:48:21','2025-05-17 09:48:21',1),(8,'basta pagkain','Masarap to pramis','4',500.00,100.00,'10','ace.jpg',1,'2025-05-26 01:54:30','2025-05-26 01:54:30',1),(9,'Streak Frites','A classic French and Belgian dish consisting of a beef steak served with crispy French fries.','1',49.99,100.00,'10','SteakFrites.jpeg',1,'2025-05-26 06:08:51','2025-05-26 06:08:51',1),(10,'Beef Bulgogi','A popular Korean dish consisting of thinly sliced marinated beef, most commonly cooked over a grill or in a pan.','1',40.00,100.00,'10','BeefBulgogi.jpeg',1,'2025-05-26 06:36:55','2025-05-26 06:36:55',0),(11,'Roast Rib','Also known as Prime Rib, it’s a beef cut that’s incredibly succulent with superior taste.','1',40.00,100.00,'10','roastrib.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(12,'Chicken Parmigiana','Pollo alla parmigiana in Italian, but affectionately referred by Aussies as Parma, Parmi or “a schnitty with tomato sauce and cheese”.','1',37.50,100.00,'10','chicken-parmigiana.jpeg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(13,'Scugnizzi','Typically made by frying strips or pieces of pizza dough, which are then often served with fresh ingredients like tomatoes, basil, and rocket.','3',18.00,100.00,'10','scugnizzi.jpg',1,'2025-05-26 06:52:06','2025-05-26 06:52:06',1),(14,'Chicken Biryani','A popular South Asian dish that combines marinated chicken with a flavorful blend of rice, spices, and herbs, often served at celebrations. ','1',37.50,100.00,'10','chicken-biryani.jpeg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(15,'Buffalo Wings','A popular American dish consisting of deep-fried, unbreaded chicken wings (or drumettes) coated in a sauce made with a vinegar-based cayenne pepper hot sauce and melted butter.','1',25.00,100.00,'10','buffalo-wings.jpeg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(16,'Herb French Fries','Garnished or served with fresh herbs, like parsley, coriander, or rosemary.','2',15.00,100.00,'10','fries.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(17,'Humpty Dumpty Burger','Topped with caramelized onions to add a sweet and smoky twist, melted burger cheese, and a runny egg.','3',19.99,100.00,'10','humptydumpty-burger.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(18,'Ham and Cheese Pizza','A popular Italian-American dish consisting of a flatbread base, tomato sauce, melted cheese, and sliced ham.','3',30.75,100.00,'10','pizza.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(19,'Soft Taco','Taco made with a soft tortilla, typically a flour tortilla, instead of a crispy, fried tortilla shell.','3',21.50,100.00,'10','soft-taco.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(20,'Pretzel Sticks','Typically made from a dough similar to traditional pretzels, shaped into long, thin sticks, and often sprinkled with salt.','3',13.90,100.00,'10','pretzel-sticks.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(21,'Fried Calamari','A dish in Mediterranean cuisine, consisting of batter-coated, deep-fried squid (fried for less than two minutes to prevent toughness), which is served plain, with salt and lemon on the side.','3',15.00,100.00,'10','calamari.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(22,'Blueberry Pancake','Made with a standard pancake batter, incorporating fresh or frozen blueberries that are either folded into the batter or placed on top of the pancake while cooking. ','2',22.50,100.00,'10','blueberry-pancake.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(23,'Matcha Green Tea Ice Cream','Ice cream infused with matcha powder, a fine, bright green powder made from ground green tea leaves.','2',26.00,100.00,'10','matcha-icecream.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(24,'Tiramisu','A variation of the classic Italian tiramisu dessert, featuring a chocolate twist.','2',28.00,100.00,'10','tiramisu.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(25,'Lemon Iced Tea','Refreshing beverage made by combining black tea, lemon, and ice.','4',15.00,100.00,'10','lemon-icedtea.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(26,'Cola','Carbonated soft drink known for its distinct sweet and fizzy taste.','4',15.00,100.00,'10','cola.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0),(27,'Wine','Alcoholic beverage primarily made from the fermented juice of grapes.','4',17.00,100.00,'10','wine.jpg',1,'2025-05-26 06:42:06','2025-05-26 06:42:06',0);
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
INSERT INTO `user_address` VALUES (1,5,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(6,8,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(7,6,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(8,6,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42');
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
INSERT INTO `user_table` VALUES (5,'Jamizan Angkol','jamizan@foodah.com','+6112345678','scrypt:32768:8:1$647LYonyJ2Oqp0Pk$bf637d2b606ae72736552e4394c9aacfc47df9a0525be467668d087811bfc5d21d2ce6a0f2974b15bb93b9db1f99e451c61f66fc0058f7e027458ff9578e42fb','zoro.jpg','Customer',1,1,'2025-05-13 23:20:58','2025-05-13 23:20:58','2025-05-13 23:20:58'),(6,'Tomasino Bakero','tomasen@foodah.com','+61999888777','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','zoro.jpg','Delivery Driver',1,1,'2025-05-13 23:21:42','2025-05-13 23:21:42','2025-05-13 23:21:42'),(8,'admin','admin@foodah.com','610000000','scrypt:32768:8:1$5MGTu6VX7giaiyo8$e61caf5df9874a6fd84fd7d3015738b2e4b129a94a0e6b72461787ed6e1a088eefafc86eb06e84560e8d92aafbfabc885891f881353910a5b480786ace021e3b','zoro.jpg','Admin',1,1,'2025-05-17 04:16:20','2025-05-17 04:16:20','2025-05-17 04:16:20');
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

-- Dump completed on 2025-05-31 12:22:15
