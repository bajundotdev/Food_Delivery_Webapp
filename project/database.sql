CREATE DATABASE  IF NOT EXISTS `foodah_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `foodah_database`;
-- MySQL dump 10.13  Distrib 8.0.42, for macos15 (arm64)
--
-- Host: localhost    Database: foodah_database
-- ------------------------------------------------------
-- Server version	9.3.0

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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_items`
--

LOCK TABLES `cart_items` WRITE;
/*!40000 ALTER TABLE `cart_items` DISABLE KEYS */;
INSERT INTO `cart_items` VALUES (1,1,5,2,'2025-05-20 08:16:05',1,NULL),(2,2,5,2,'2025-05-20 08:16:14',2,NULL),(3,7,5,NULL,'2025-05-20 08:16:20',1,NULL),(4,3,9,3,'2025-05-20 08:17:02',1,NULL),(7,7,10,9,'2025-05-23 13:26:46',1,'9a6e21cb-8cd4-48eb-ad71-929b4bfad5f1'),(8,7,10,9,'2025-05-23 13:42:38',1,'144d7e68-9a33-47be-8351-1298b131cf68'),(18,3,10,9,'2025-05-24 03:42:12',2,'111a7261-9357-4fc4-81fa-9d90f3a6838f');
/*!40000 ALTER TABLE `cart_items` ENABLE KEYS */;
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
  `is_available` tinyint(1) NOT NULL,
  `driver_rating` decimal(8,2) NOT NULL,
  `total_deliveries` int NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  PRIMARY KEY (`driver_id`),
  KEY `delivery_driver_user_id_foreign` (`user_id`),
  CONSTRAINT `delivery_driver_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `user_table` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_driver`
--

LOCK TABLES `delivery_driver` WRITE;
/*!40000 ALTER TABLE `delivery_driver` DISABLE KEYS */;
INSERT INTO `delivery_driver` VALUES (1,6,'Scooter','123456789','123-ABC',0,5.00,1,'2025-05-18 07:03:07','2025-05-18 07:03:07');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_table`
--

LOCK TABLES `order_table` WRITE;
/*!40000 ALTER TABLE `order_table` DISABLE KEYS */;
INSERT INTO `order_table` VALUES (2,5,1,1,'Completed',12.99,'Success','Cash','2025-05-20 08:35:48','2025-05-20 08:35:48',NULL,'Fast delivery, Eco Mode','RF:0012345',NULL,NULL),(3,10,1,1,'Ready',12.99,'Success','Credit Card','2025-05-20 10:25:49','2025-05-20 10:25:49',NULL,'Delayed','RF:999999',NULL,NULL),(4,10,NULL,2,'Pending',20.99,'Success','Debit Card','2025-05-22 13:47:07',NULL,NULL,NULL,'102025-05-22 23:47:07',NULL,NULL),(5,10,NULL,2,'Pending',20.99,'Success','Debit Card','2025-05-22 13:47:47',NULL,NULL,NULL,'102025-05-22 23:47:47',NULL,NULL),(8,10,NULL,2,'Pending',31.96,'','Cash','2025-05-24 00:24:34',NULL,NULL,'Hungry na po','102025-05-24 10:24:34',NULL,'White House, Block 10, Small County, District of Col, Washington, 4000, USA'),(9,10,NULL,2,'Pending',5.98,'','Cash','2025-05-24 03:42:12',NULL,NULL,'pakibalot an lang po','102025-05-24 13:42:12',NULL,'White House, Block 10, Small County, District of Col, Washington, 4000, USA');
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
  `deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  KEY `product_table_ownser_id_foreign` (`restaurant_id`),
  CONSTRAINT `product_table_ownser_id_foreign` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_table`
--

LOCK TABLES `product_table` WRITE;
/*!40000 ALTER TABLE `product_table` DISABLE KEYS */;
INSERT INTO `product_table` VALUES (1,'Pizza lang','Delicious Pizza promise swear','Main Dish',12.99,5.00,'15','https://media.istockphoto.com/id/1561032358/photo/mouthwatering-oven-baked-pizzas-adorned-with-assorted-meats-pepperoni-and-cheese-and-a.jpg?s=612x612&w=is&k=20&c=dCUZqn3KX9pxoPChOrbZrriEGW605FChZmZsnmug30s=',1,'2025-05-14 00:12:11','2025-05-14 00:12:11',1,1),(2,'Burger','Juicy beef burger','Main',9.99,100.00,'20','https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?q=80&w=3464&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',1,'2025-05-17 09:44:44','2025-05-17 09:44:44',1,1),(3,'Kwazan','Croissant is the new Kwazan','Main',2.99,100.00,'20','https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?q=80&w=3464&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',1,'2025-05-17 09:44:44','2025-05-17 09:44:44',1,0),(7,'Chicken barbecue','The best barbie ever in Brisbane','Main',12.99,100.00,'20','https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?q=80&w=3464&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',1,'2025-05-17 09:48:21','2025-05-17 09:48:21',2,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_address`
--

LOCK TABLES `user_address` WRITE;
/*!40000 ALTER TABLE `user_address` DISABLE KEYS */;
INSERT INTO `user_address` VALUES (1,5,'Iglu','62 Blamey St.','Kelvin Grove','Brisbane','Queensland','4509','Australia','2025-05-18 07:07:42','2025-05-18 07:07:42'),(2,10,'White House','Block 10','Small County','District of Col','Washington','4000','USA','2025-05-22 13:35:00','2025-05-22 13:35:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_table`
--

LOCK TABLES `user_table` WRITE;
/*!40000 ALTER TABLE `user_table` DISABLE KEYS */;
INSERT INTO `user_table` VALUES (1,'Junnie Boy','junnie@foodah.com','+61000111222','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','https://plus.unsplash.com/premium_photo-1664536392896-cd1743f9c02c?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D','Admin',1,1,'2025-05-13 23:18:20','2025-05-13 23:18:20','2025-05-13 23:18:20'),(5,'Jamizan Angkol','jamizan@foodah.com','+6112345678','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','https://plus.unsplash.com/premium_photo-1664536392896-cd1743f9c02c?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D','Customer',1,1,'2025-05-13 23:20:58','2025-05-13 23:20:58','2025-05-13 23:20:58'),(6,'Tomasino Bakero','tomasen@foodah.com','+61999888777','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','https://plus.unsplash.com/premium_photo-1664536392896-cd1743f9c02c?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D','Delivery Driver',1,1,'2025-05-13 23:21:42','2025-05-13 23:21:42','2025-05-13 23:21:42'),(7,'Adriano Restoranto','adrian@foodah.com','+61987654321','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','https://plus.unsplash.com/premium_photo-1664536392896-cd1743f9c02c?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D','Restaurant Manager',1,1,'2025-05-14 00:06:07','2025-05-14 00:06:07','2025-05-14 00:06:07'),(8,'admin','admin@foodah.com','610000000','scrypt:32768:8:1$YcqQ4nZrNWFI4aPw$e34f526ca6df6329d656ff1ea66bc59cae91a2dbd0272bfc80d4617da1af201e57e8e148245f53ca642b6cf4ce1c45ef904d4be4c83940bb7a384e83e8cb84cd','https://plus.unsplash.com/premium_photo-1664536392896-cd1743f9c02c?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D','Admin',1,1,'2025-05-17 04:16:20','2025-05-17 04:16:20','2025-05-17 04:16:20'),(9,'Tony Chopper','tony@foodah.com','09777968166','scrypt:32768:8:1$zRIKWVTmKGvdqHYm$1d2fb305042d1ed8d4914692321486a3aacab3ecdc7cb03345bc0a4c886c2b257f3de9818b3883e9a87673e2c91892fdf241673daffb5d790c8580c69061542f','user.jpg','Customer',1,1,'2025-05-20 02:28:16','2025-05-20 02:28:16','2025-05-20 02:28:16'),(10,'Nico Robin','robin@foodah.com','+6123564578','scrypt:32768:8:1$t5z5WXMfLPqUbocC$f6dc23b40a45944bbe5050054fe86ca474a566b1e53d6a1d6aa903d9cdebce21c85bce30f257d98d442d8ce1b1e82fe4cb96ac17f7ca0262a48ca5ac24ab20e0','user.jpg','Customer',1,1,'2025-05-20 06:23:36','2025-05-20 06:23:36','2025-05-20 06:23:36');
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

-- Dump completed on 2025-05-24 13:48:52
