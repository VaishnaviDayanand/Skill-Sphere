-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: training_management_db
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `billing`
--

DROP TABLE IF EXISTS `billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing` (
  `Bill_id` varchar(20) NOT NULL,
  `Sid` varchar(5) NOT NULL,
  `Tid` int NOT NULL,
  `BCrsId` varchar(5) NOT NULL,
  `CPrice` bigint NOT NULL,
  `Discount` float DEFAULT NULL,
  `TotalPrice` bigint NOT NULL,
  PRIMARY KEY (`Bill_id`),
  KEY `Sid_idx` (`Sid`),
  KEY `Tid_idx` (`Tid`),
  KEY `CrsId_idx` (`BCrsId`),
  CONSTRAINT `BCrsId` FOREIGN KEY (`BCrsId`) REFERENCES `coursedetails` (`CrsId`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Sid` FOREIGN KEY (`Sid`) REFERENCES `student` (`Sid`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Tid` FOREIGN KEY (`Tid`) REFERENCES `trainers` (`Tid`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coursedetails`
--

DROP TABLE IF EXISTS `coursedetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coursedetails` (
  `CrsId` varchar(10) NOT NULL,
  `CrsName` varchar(45) NOT NULL,
  `CPrice` float NOT NULL,
  `Duration` float NOT NULL,
  PRIMARY KEY (`CrsId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `Sid` varchar(5) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Gender` varchar(5) NOT NULL,
  `Age` int NOT NULL,
  `MailId` varchar(45) NOT NULL,
  `PhoneNo` bigint NOT NULL,
  `CollegeName` varchar(45) NOT NULL,
  `Branch` varchar(45) NOT NULL,
  `Year` int NOT NULL,
  `Semester` int NOT NULL,
  `Pwd` varchar(45) NOT NULL,
  PRIMARY KEY (`Sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trainers`
--

DROP TABLE IF EXISTS `trainers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainers` (
  `Tid` int NOT NULL,
  `TName` varchar(45) NOT NULL,
  `TGender` varchar(5) NOT NULL,
  `Qualification` varchar(45) NOT NULL,
  `CrsId` varchar(45) NOT NULL,
  `T_exp` float NOT NULL,
  `Rating` float NOT NULL,
  PRIMARY KEY (`Tid`),
  KEY `CrsId_idx` (`CrsId`),
  CONSTRAINT `CrsId` FOREIGN KEY (`CrsId`) REFERENCES `coursedetails` (`CrsId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'training_management_db'
--

--
-- Dumping routines for database 'training_management_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26  9:51:21
