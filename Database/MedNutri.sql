CREATE DATABASE  IF NOT EXISTS `mednutri` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mednutri`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mednutri
-- ------------------------------------------------------
-- Server version	8.4.0

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
-- Table structure for table `adherence_records`
--

DROP TABLE IF EXISTS `adherence_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adherence_records` (
  `ARid` varchar(20) NOT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `nid` varchar(20) DEFAULT NULL,
  `mid` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ARid`),
  KEY `pid` (`pid`),
  KEY `mid` (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adherence_records`
--

LOCK TABLES `adherence_records` WRITE;
/*!40000 ALTER TABLE `adherence_records` DISABLE KEYS */;
INSERT INTO `adherence_records` VALUES ('adherence4216','patient4032',NULL,'reminder8246','2025-04-27','2025-04-27 10:24:14'),('adherence9545','patient6432','plan7307',NULL,'2025-04-27','2025-04-27 10:22:06');
/*!40000 ALTER TABLE `adherence_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medication_reminder`
--

DROP TABLE IF EXISTS `medication_reminder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medication_reminder` (
  `mid` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `reminder` json NOT NULL,
  `pid` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `approved` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`mid`),
  UNIQUE KEY `mid_UNIQUE` (`mid`),
  KEY `pid_idx` (`pid`),
  CONSTRAINT `patientid` FOREIGN KEY (`pid`) REFERENCES `patients` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medication_reminder`
--

LOCK TABLES `medication_reminder` WRITE;
/*!40000 ALTER TABLE `medication_reminder` DISABLE KEYS */;
INSERT INTO `medication_reminder` VALUES ('reminder8246','patient4032Reminder','\"{\\\"Dolo 650\\\": {\\\"Timing\\\": [\\\"Afternoon\\\"], \\\"meal_timing\\\": \\\"Before\\\"}, \\\"Paracetamol\\\": {\\\"Timing\\\": [\\\"Afternoon\\\"], \\\"meal_timing\\\": \\\"After\\\"}}\"','patient4032','2025-04-27',0);
/*!40000 ALTER TABLE `medication_reminder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nutrition_plan`
--

DROP TABLE IF EXISTS `nutrition_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutrition_plan` (
  `nid` varchar(20) NOT NULL,
  `plan_name` varchar(100) NOT NULL,
  `plan` json NOT NULL,
  `pid` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `approved` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`nid`),
  UNIQUE KEY `nid_UNIQUE` (`nid`),
  KEY `pid_idx` (`pid`),
  CONSTRAINT `pid` FOREIGN KEY (`pid`) REFERENCES `patients` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nutrition_plan`
--

LOCK TABLES `nutrition_plan` WRITE;
/*!40000 ALTER TABLE `nutrition_plan` DISABLE KEYS */;
INSERT INTO `nutrition_plan` VALUES ('plan7307','Weight Loss','\"{\\\"meal_plan\\\": {\\\"day\\\": \\\"Single Day\\\", \\\"breakfast\\\": {\\\"name\\\": \\\"Oatmeal with Berries and Nuts\\\", \\\"description\\\": \\\"1/2 cup rolled oats cooked with water, 1/2 cup mixed berries, 1/4 cup chopped almonds.\\\", \\\"calories\\\": 350, \\\"protein\\\": 12, \\\"carbs\\\": 50, \\\"fat\\\": 15}, \\\"lunch\\\": {\\\"name\\\": \\\"Grilled Chicken Salad\\\", \\\"description\\\": \\\"4oz grilled chicken breast, 2 cups mixed greens, 1/2 cup mixed vegetables (cucumber, bell peppers, tomatoes), 2 tbsp light vinaigrette dressing.\\\", \\\"calories\\\": 400, \\\"protein\\\": 35, \\\"carbs\\\": 20, \\\"fat\\\": 20}, \\\"dinner\\\": {\\\"name\\\": \\\"Baked Salmon with Roasted Vegetables\\\", \\\"description\\\": \\\"4oz baked salmon, 1 cup roasted vegetables (broccoli, carrots, zucchini) seasoned with herbs and spices.\\\", \\\"calories\\\": 450, \\\"protein\\\": 30, \\\"carbs\\\": 30, \\\"fat\\\": 25}, \\\"snacks\\\": {\\\"0\\\": {\\\"name\\\": \\\"Apple with Peanut Butter\\\", \\\"description\\\": \\\"1 medium apple sliced, 2 tbsp natural peanut butter.\\\", \\\"calories\\\": 200, \\\"protein\\\": 7, \\\"carbs\\\": 20, \\\"fat\\\": 12}, \\\"1\\\": {\\\"name\\\": \\\"Greek Yogurt with Berries\\\", \\\"description\\\": \\\"1 cup non-fat Greek yogurt, 1/2 cup berries.\\\", \\\"calories\\\": 150, \\\"protein\\\": 20, \\\"carbs\\\": 15, \\\"fat\\\": 0}}, \\\"total_calories\\\": 1550, \\\"total_protein\\\": 104, \\\"total_carbs\\\": 135, \\\"total_fat\\\": 72}}\"','patient6432','2025-04-27',0);
/*!40000 ALTER TABLE `nutrition_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `pid` varchar(20) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Mobile` varchar(15) NOT NULL,
  `Age` int NOT NULL,
  `Gender` varchar(10) NOT NULL,
  PRIMARY KEY (`pid`),
  UNIQUE KEY `pid_UNIQUE` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('patient1213','Tirth Patel','1111111112',21,'male'),('patient1234','Tirth Patel','9408410672',21,'Male'),('patient1503','Vishakha','8347964513',22,'Female'),('patient1802','Tirth','7634679856',21,'Male'),('patient1963','Dipak','9978013396',21,'Male'),('patient2134','Dipak Patel','9408410672',21,'Male'),('patient2634','Yash Patel','9408410672',21,'Male'),('patient2807','Patel Tirth','9408410672',21,'male'),('patient2884','Tirth','8574964578',21,'Male'),('patient3530','Tirth','456789234',21,'Male'),('patient4032','Yash','9408410672',21,'Male'),('patient4626','Tirth','123456789',21,'Male'),('patient4701','Umang Rao','9173030225',21,'Male'),('patient5131','Tirth','223344556677',21,'Male'),('patient5642','Tirth','859674126',21,'Male'),('patient5749','Tirth Patel','1111111111',21,'male'),('patient6138','Tirth','6677881234',21,'Male'),('patient6432','Tirth','9408410672',21,'Male'),('patient6482','Dipak','8347964512',21,'Male'),('patient6630','Tirth','2267892345',21,'Male'),('patient7233','Dipak','9408410672',21,'Male'),('patient7610','Tirth','8347964512',21,'Male'),('patient8297','Tirth','2345678910',21,'Male'),('patient8969','Tirth','9978013396',21,'Male'),('patient9039','Tirth','987654321',45,'Male'),('patient9380','Dhara Dave','123456780',21,'male');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` enum('admin','doctor','patient') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-27 16:45:02
