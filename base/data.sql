CREATE DATABASE  IF NOT EXISTS `jugadores` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `jugadores`;
-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: jugadores
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.20-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `jugador`
--

DROP TABLE IF EXISTS `jugador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jugador` (
  `idjugador` int(11) NOT NULL AUTO_INCREMENT,
  `apodo` varchar(45) DEFAULT NULL,
  `nombre` varchar(70) DEFAULT NULL,
  `mundiales` int(11) DEFAULT NULL,
  `copas` int(11) DEFAULT NULL,
  `goles` int(11) DEFAULT NULL,
  `historia` longtext,
  `url_img` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`idjugador`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jugador`
--

LOCK TABLES `jugador` WRITE;
/*!40000 ALTER TABLE `jugador` DISABLE KEYS */;
INSERT INTO `jugador` VALUES (13,'lorenzo','Edson Arantes do Nascimento',9,4,200,'conocido mundialmente como Pelé, es un exfutbolista brasileño.\nEs considerado por muchos jugadores y exjugadores,\ndiversos organismos deportivos, periodistas y la prensa en general,\n y gran parte de los admiradores del fútbol, como el «mejor futbolista de la historia',NULL),(14,'Pirlo','Andrea Pirlo',6,5,170,'Andrea Pirlo es un futbolista italiano. \nSe desempeña en la posición de centrocampista \ny su actual equipo es el New York City de la \nMajor League Soccer de Estados Unidos.',NULL);
/*!40000 ALTER TABLE `jugador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `premios`
--

DROP TABLE IF EXISTS `premios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `premios` (
  `idpremios` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(200) DEFAULT NULL,
  `idjugador` int(11) NOT NULL,
  PRIMARY KEY (`idpremios`),
  KEY `fk_premios_jugador_idx` (`idjugador`),
  CONSTRAINT `fk_premios_jugador` FOREIGN KEY (`idjugador`) REFERENCES `jugador` (`idjugador`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `premios`
--

LOCK TABLES `premios` WRITE;
/*!40000 ALTER TABLE `premios` DISABLE KEYS */;
/*!40000 ALTER TABLE `premios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vista`
--

DROP TABLE IF EXISTS `vista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vista` (
  `idvista` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(95) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idvista`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vista`
--

LOCK TABLES `vista` WRITE;
/*!40000 ALTER TABLE `vista` DISABLE KEYS */;
INSERT INTO `vista` VALUES (15,'Historia','historia'),(16,'Mundiales Ganados','mundiales'),(17,'Copas Ganadas','copas'),(18,'Goles con su camiseta','goles'),(19,'Premios recividos','premios');
/*!40000 ALTER TABLE `vista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vista_jugador`
--

DROP TABLE IF EXISTS `vista_jugador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vista_jugador` (
  `idvista` int(11) NOT NULL AUTO_INCREMENT,
  `idjugador` int(11) NOT NULL,
  `estado` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`idvista`,`idjugador`),
  KEY `fk_vista_has_jugador_jugador1_idx` (`idjugador`),
  KEY `fk_vista_has_jugador_vista1_idx` (`idvista`),
  CONSTRAINT `fk_vista_has_jugador_jugador1` FOREIGN KEY (`idjugador`) REFERENCES `jugador` (`idjugador`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_vista_has_jugador_vista1` FOREIGN KEY (`idvista`) REFERENCES `vista` (`idvista`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vista_jugador`
--

LOCK TABLES `vista_jugador` WRITE;
/*!40000 ALTER TABLE `vista_jugador` DISABLE KEYS */;
INSERT INTO `vista_jugador` VALUES (15,13,1),(15,14,1),(16,13,1),(16,14,1),(17,13,1),(17,14,1),(18,13,1),(18,14,1),(19,13,1),(19,14,1);
/*!40000 ALTER TABLE `vista_jugador` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-01-19 16:20:33
