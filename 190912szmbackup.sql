-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: szlukamate$default
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.16.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add post',7,'add_post'),(20,'Can change post',7,'change_post'),(21,'Can delete post',7,'delete_post'),(22,'Can add comment',8,'add_comment'),(23,'Can change comment',8,'change_comment'),(24,'Can delete comment',8,'delete_comment'),(25,'Can add tbl doc_details',9,'add_tbldoc_details'),(26,'Can change tbl doc_details',9,'change_tbldoc_details'),(27,'Can delete tbl doc_details',9,'delete_tbldoc_details'),(28,'Can add tbl product',10,'add_tblproduct'),(29,'Can change tbl product',10,'change_tblproduct'),(30,'Can delete tbl product',10,'delete_tblproduct'),(31,'Can add tbl doc',11,'add_tbldoc'),(32,'Can change tbl doc',11,'change_tbldoc'),(33,'Can delete tbl doc',11,'delete_tbldoc'),(34,'Can add tbl doc',12,'add_tbldoc'),(35,'Can change tbl doc',12,'change_tbldoc'),(36,'Can delete tbl doc',12,'delete_tbldoc'),(37,'Can add tbl doc_details',13,'add_tbldoc_details'),(38,'Can change tbl doc_details',13,'change_tbldoc_details'),(39,'Can delete tbl doc_details',13,'delete_tbldoc_details'),(40,'Can add tbl product',14,'add_tblproduct'),(41,'Can change tbl product',14,'change_tblproduct'),(42,'Can delete tbl product',14,'delete_tblproduct'),(43,'Can add tbl doc_kind',15,'add_tbldoc_kind'),(44,'Can change tbl doc_kind',15,'change_tbldoc_kind'),(45,'Can delete tbl doc_kind',15,'delete_tbldoc_kind'),(46,'Can add tbl companies',16,'add_tblcompanies'),(47,'Can change tbl companies',16,'change_tblcompanies'),(48,'Can delete tbl companies',16,'delete_tblcompanies'),(49,'Can add tbl contacts',17,'add_tblcontacts'),(50,'Can change tbl contacts',17,'change_tblcontacts'),(51,'Can delete tbl contacts',17,'delete_tblcontacts'),(52,'Can add tbl issue',18,'add_tblissue'),(53,'Can change tbl issue',18,'change_tblissue'),(54,'Can delete tbl issue',18,'delete_tblissue');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `subscriptiontext_tblauth_user` text,
  `emailbodytext_tblauth_user` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$1CI2zMgGEmBC$EZSMhvGjTetCWK5AftJBM0GIVhE/sNi/nfKxkQDNhNY=','2019-09-09 20:00:12.765660',1,'szlukamate','Mate','Szluka','szluka.mate@gmail.com',1,1,'2018-11-02 21:48:04.683828','Sales Engineer\r\n+36309680-469\r\nszluka.mate@gmail.com','data1\n\nHerewith we are sending our quotation attached.\n\nPlease do not hesitate to ask any question.\nIt will be a pleasure to serve you at any time again.\n\nYours respectfully:\n\nMate Szluka\nSales Engineer\n\n6726 Szeged, Akácfa u. 16.\nHungary\n\nTel.: x Mob.:(+36)30/9680-469\nSzluka.Mate@gmail.com\nwww.x.hu\n'),(3,'pbkdf2_sha256$36000$fBK7P9yKbYST$NxLXdiX7FNisBZyf3F6VphHV2hnixqKT7SoGeqlwtnI=','2019-02-05 17:30:33.598559',0,'gipszjakab','Jakab','Gipsz','q@q.hu',1,1,'2019-02-05 17:21:58.000000',NULL,NULL);
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,3,10);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_comment`
--

DROP TABLE IF EXISTS `blog_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(200) NOT NULL,
  `text` longtext NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `approved_comment` tinyint(1) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_comment_post_id_580e96ef_fk_blog_post_id` (`post_id`),
  CONSTRAINT `blog_comment_post_id_580e96ef_fk_blog_post_id` FOREIGN KEY (`post_id`) REFERENCES `blog_post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_comment`
--

LOCK TABLES `blog_comment` WRITE;
/*!40000 ALTER TABLE `blog_comment` DISABLE KEYS */;
INSERT INTO `blog_comment` VALUES (1,'jjjjjjjjj','1co','2018-11-03 07:49:35.000000',1,1),(2,'jjjjjjjjj','2co','2018-11-03 07:50:01.000000',1,2),(3,'hh','3co','2018-11-03 07:50:21.000000',1,2);
/*!40000 ALTER TABLE `blog_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_post`
--

DROP TABLE IF EXISTS `blog_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `text` longtext NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `published_date` datetime(6) DEFAULT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_post_author_id_dd7a8485_fk_auth_user_id` (`author_id`),
  CONSTRAINT `blog_post_author_id_dd7a8485_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_post`
--

LOCK TABLES `blog_post` WRITE;
/*!40000 ALTER TABLE `blog_post` DISABLE KEYS */;
INSERT INTO `blog_post` VALUES (1,'1pti','1pte','2018-11-03 07:47:40.000000','2018-11-03 07:48:36.000000',1),(2,'2ti','2te','2018-11-03 07:48:40.000000','2018-11-03 07:49:10.000000',1);
/*!40000 ALTER TABLE `blog_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_tbldoc`
--

DROP TABLE IF EXISTS `blog_tbldoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_tbldoc` (
  `Docid_tblDoc` int(11) NOT NULL AUTO_INCREMENT,
  `Pcd_tblDoc` varchar(200) NOT NULL,
  `Town_tblDoc` varchar(200) NOT NULL,
  PRIMARY KEY (`Docid_tblDoc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_tbldoc`
--

LOCK TABLES `blog_tbldoc` WRITE;
/*!40000 ALTER TABLE `blog_tbldoc` DISABLE KEYS */;
/*!40000 ALTER TABLE `blog_tbldoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_tbldoc_details`
--

DROP TABLE IF EXISTS `blog_tbldoc_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_tbldoc_details` (
  `Doc_detailsid_tblDoc_details` int(11) NOT NULL AUTO_INCREMENT,
  `Qty_tblDoc_details` int(11) NOT NULL,
  `Docid_tblDoc_details_id` int(11) NOT NULL,
  `Productid_tblDoc_details_id` int(11) NOT NULL,
  PRIMARY KEY (`Doc_detailsid_tblDoc_details`),
  KEY `blog_tbldoc_details_Docid_tblDoc_details_d33f3418_fk_blog_tbld` (`Docid_tblDoc_details_id`),
  KEY `blog_tbldoc_details_Productid_tblDoc_det_cef280cd_fk_blog_tblp` (`Productid_tblDoc_details_id`),
  CONSTRAINT `blog_tbldoc_details_Docid_tblDoc_details_d33f3418_fk_blog_tbld` FOREIGN KEY (`Docid_tblDoc_details_id`) REFERENCES `blog_tbldoc` (`Docid_tblDoc`),
  CONSTRAINT `blog_tbldoc_details_Productid_tblDoc_det_cef280cd_fk_blog_tblp` FOREIGN KEY (`Productid_tblDoc_details_id`) REFERENCES `blog_tblproduct` (`Productid_tblProduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_tbldoc_details`
--

LOCK TABLES `blog_tbldoc_details` WRITE;
/*!40000 ALTER TABLE `blog_tbldoc_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `blog_tbldoc_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_tblproduct`
--

DROP TABLE IF EXISTS `blog_tblproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_tblproduct` (
  `Productid_tblProduct` int(11) NOT NULL AUTO_INCREMENT,
  `Product_price_tblProduct` int(11) NOT NULL,
  `Product_description_tblProduct` varchar(200) NOT NULL,
  PRIMARY KEY (`Productid_tblProduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_tblproduct`
--

LOCK TABLES `blog_tblproduct` WRITE;
/*!40000 ALTER TABLE `blog_tblproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `blog_tblproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-11-02 21:50:42.145498','1','Something1',1,'[{\"added\": {}}]',14,1),(2,'2018-11-02 21:50:57.531874','2','Something22',1,'[{\"added\": {}}]',14,1),(3,'2018-11-02 21:51:37.705989','1','Quotation',1,'[{\"added\": {}}]',15,1),(4,'2018-11-02 21:51:50.753814','2','Order',1,'[{\"added\": {}}]',15,1),(5,'2018-11-02 21:52:00.712735','3','Invoice',1,'[{\"added\": {}}]',15,1),(6,'2018-11-02 21:52:36.324847','1','Szeged',1,'[{\"added\": {}}]',12,1),(7,'2018-11-02 21:53:10.834013','2','Pécs',1,'[{\"added\": {}}]',12,1),(8,'2018-11-02 21:53:52.361758','3','Győr',1,'[{\"added\": {}}]',12,1),(9,'2018-11-02 21:54:41.935156','1','Defaultnote1',1,'[{\"added\": {}}]',13,1),(10,'2018-11-02 21:55:06.555670','2','Defaultnote2',1,'[{\"added\": {}}]',13,1),(11,'2018-11-03 07:48:40.249007','1','1pti',1,'[{\"added\": {}}]',7,1),(12,'2018-11-03 07:49:15.331036','2','2ti',1,'[{\"added\": {}}]',7,1),(13,'2018-11-03 07:50:00.846842','1','1co',1,'[{\"added\": {}}]',8,1),(14,'2018-11-03 07:50:21.722024','2','2co',1,'[{\"added\": {}}]',8,1),(15,'2018-11-03 07:51:12.383658','3','3co',1,'[{\"added\": {}}]',8,1),(16,'2018-11-03 12:35:04.602108','3','Something3',1,'[{\"added\": {}}]',14,1),(17,'2018-11-03 16:42:29.827161','3','Defaultnote3',1,'[{\"added\": {}}]',13,1),(18,'2018-11-03 16:43:17.651676','4','Defaultnote6',1,'[{\"added\": {}}]',13,1),(19,'2018-11-03 16:43:43.989990','5','Defaultnote18',1,'[{\"added\": {}}]',13,1),(20,'2018-11-06 20:13:45.812115','4','Békéscsaba',1,'[{\"added\": {}}]',12,1),(21,'2018-11-06 20:14:20.968920','5','Nyíregyháza',1,'[{\"added\": {}}]',12,1),(22,'2018-11-06 20:14:57.179042','6','Eger',1,'[{\"added\": {}}]',12,1),(23,'2018-11-17 12:45:19.377385','1','Company1',1,'[{\"added\": {}}]',16,1),(24,'2018-11-17 12:46:32.695498','1','Contactfirstname1',1,'[{\"added\": {}}]',17,1),(25,'2018-11-17 12:47:20.050215','1','Szeged',2,'[]',12,1),(26,'2018-11-17 19:52:04.750680','2','Company2firstname1',1,'[{\"added\": {}}]',17,1),(27,'2018-11-17 19:52:46.228967','3','Company2firstname2',1,'[{\"added\": {}}]',17,1),(28,'2018-11-21 12:33:40.477665','6','Company3',1,'[{\"added\": {}}]',16,1),(29,'2018-11-21 12:35:24.165214','4','Firstname of company1',1,'[{\"added\": {}}]',17,1),(30,'2018-12-04 12:36:33.426120','1','Firstname1',2,'[{\"changed\": {\"fields\": [\"Companyid_tblContacts\"]}}]',17,1),(31,'2018-12-09 21:38:05.736354','1','Somethi',2,'[]',14,1),(32,'2018-12-09 21:39:11.406678','4','Pr5',1,'[{\"added\": {}}]',14,1),(33,'2018-12-09 21:39:32.638894','5','Pr6',1,'[{\"added\": {}}]',14,1),(34,'2018-12-09 21:39:55.847788','6','Pr7',1,'[{\"added\": {}}]',14,1),(35,'2018-12-12 18:31:56.325787','1','Company1',2,'[{\"changed\": {\"fields\": [\"companyname_tblcompanies\"]}}]',16,1),(36,'2018-12-12 18:32:13.425612','2','Company2',2,'[{\"changed\": {\"fields\": [\"companyname_tblcompanies\"]}}]',16,1),(37,'2018-12-12 18:32:52.929683','1','Firstname3',2,'[{\"changed\": {\"fields\": [\"firstname_tblcontacts\", \"lastname_tblcontacts\"]}}]',17,1),(38,'2018-12-12 18:33:22.476309','4','Firstname1',2,'[{\"changed\": {\"fields\": [\"firstname_tblcontacts\", \"lastname_tblcontacts\"]}}]',17,1),(39,'2018-12-12 18:33:36.386435','4','Firstname1',2,'[]',17,1),(40,'2018-12-12 18:33:57.681834','3','firstname2',2,'[{\"changed\": {\"fields\": [\"firstname_tblcontacts\", \"lastname_tblcontacts\"]}}]',17,1),(41,'2018-12-12 18:34:38.088748','2','firstname2',2,'[{\"changed\": {\"fields\": [\"firstname_tblcontacts\", \"lastname_tblcontacts\"]}}]',17,1),(42,'2018-12-12 18:34:50.419655','1','Firstname3',2,'[]',17,1),(43,'2019-02-05 17:08:29.342974','2','gipszjakab',1,'[{\"added\": {}}]',4,1),(44,'2019-02-05 17:10:11.659158','2','gipszjakab',2,'[{\"changed\": {\"fields\": [\"first_name\", \"last_name\", \"email\"]}}]',4,1),(45,'2019-02-05 17:14:34.156603','2','gipszjakab',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,1),(46,'2019-02-05 17:17:30.405112','2','gipszjakab',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,1),(47,'2019-02-05 17:19:56.815806','2','gipszjakab',3,'',4,1),(48,'2019-02-05 17:21:58.379433','3','gipszjakab',1,'[{\"added\": {}}]',4,1),(49,'2019-02-05 17:24:06.469287','3','gipszjakab',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',4,1),(50,'2019-02-05 17:28:24.714612','3','gipszjakab',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,1),(51,'2019-02-05 17:30:17.357415','3','gipszjakab',2,'[{\"changed\": {\"fields\": [\"first_name\", \"last_name\", \"email\", \"user_permissions\"]}}]',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(8,'blog','comment'),(7,'blog','post'),(11,'blog','tbldoc'),(9,'blog','tbldoc_details'),(10,'blog','tblproduct'),(5,'contenttypes','contenttype'),(18,'ist','tblissue'),(16,'quotation','tblcompanies'),(17,'quotation','tblcontacts'),(12,'quotation','tbldoc'),(13,'quotation','tbldoc_details'),(15,'quotation','tbldoc_kind'),(14,'quotation','tblproduct'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-11-02 21:11:14.376089'),(2,'auth','0001_initial','2018-11-02 21:12:24.450688'),(3,'admin','0001_initial','2018-11-02 21:12:48.408225'),(4,'admin','0002_logentry_remove_auto_add','2018-11-02 21:12:48.456194'),(5,'contenttypes','0002_remove_content_type_name','2018-11-02 21:12:48.552835'),(6,'auth','0002_alter_permission_name_max_length','2018-11-02 21:12:48.605419'),(7,'auth','0003_alter_user_email_max_length','2018-11-02 21:12:48.664379'),(8,'auth','0004_alter_user_username_opts','2018-11-02 21:12:48.682748'),(9,'auth','0005_alter_user_last_login_null','2018-11-02 21:12:48.736570'),(10,'auth','0006_require_contenttypes_0002','2018-11-02 21:12:48.744009'),(11,'auth','0007_alter_validators_add_error_messages','2018-11-02 21:12:48.765243'),(12,'auth','0008_alter_user_username_max_length','2018-11-02 21:12:48.822705'),(13,'blog','0001_initial','2018-11-02 21:13:07.382074'),(14,'blog','0002_comment','2018-11-02 21:13:26.186726'),(15,'blog','0003_doc','2018-11-02 21:13:32.062693'),(16,'blog','0004_auto_20181009_2144','2018-11-02 21:13:32.121358'),(17,'blog','0005_doc_pcd_tbldoc','2018-11-02 21:13:34.870240'),(18,'blog','0006_auto_20181010_1820','2018-11-02 21:13:34.948409'),(19,'blog','0007_doc_town_tbldoc','2018-11-02 21:13:37.659099'),(20,'blog','0008_doc_details','2018-11-02 21:13:47.186922'),(21,'blog','0009_auto_20181011_1605','2018-11-02 21:13:47.246950'),(22,'blog','0010_auto_20181011_1635','2018-11-02 21:13:47.458849'),(23,'blog','0011_doc_details_product_description_tbldoc_details','2018-11-02 21:13:51.033263'),(24,'blog','0012_auto_20181015_1759','2018-11-02 21:14:13.472483'),(31,'sessions','0001_initial','2018-11-02 21:14:56.285954'),(32,'quotation','0001_initial','2018-11-17 14:51:14.569485'),(35,'quotation','0002_tblcompanies','2018-11-17 18:49:50.281212'),(36,'quotation','0003_auto_20181117_1950','2018-11-17 18:51:05.817368'),(38,'quotation','0004_tblcontacts','2018-11-17 19:15:59.537810'),(40,'quotation','0005_tbldoc_contactid_tbldoc','2018-11-17 19:30:49.852540'),(42,'quotation','0006_tbldoc_details_creationtime_tbldoc_details','2018-11-20 21:52:25.514690'),(43,'ist','0001_initial','2019-01-07 10:28:28.558994');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0bv9pucxtow2b87tqqqk94q563az1e2j','YTliMDY1MTlkOTViYzU5YmY5Njc2M2I5ZGU5YmI1ZGRlNDMwMTJkNzp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImZpeHRvdGhpcyI6IjIxNSIsImZpeHN0YXRlIjoiMCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-04-29 14:53:24.762430'),('1n3clnwk8si4t6mbb9kd41gzw90henbd','MTgyZDJmNTBhY2M0OTRmZGQ0NDFlYjRkMjg3NTFlOTU1MTNjYjM2ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-07-29 12:29:35.772187'),('270o7sys9h2608m6uym1jtaqsgu5slez','YjE4MmZjYzA4ZTJkN2ZlMjQyYWEwNDhkNjc3OTFiZDVjZWI5MzA0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-11-17 12:33:57.987435'),('7atng2xgd7fgsjpai4l3mxfavozka9gm','OTA2MDA5ZjI3YWEyNDY4ZDA2YzAwYmY5NDlhOTliOWQyZTY0YTYwZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYjkxM2MwOTA0NjQ3ODE0MjE5NTc1OWJlNTU3OTdjZDFlYjA4MDhjMSIsImZpeHN0YXRlIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiZml4dG90aGlzIjoiODQifQ==','2019-03-25 15:36:55.957910'),('7f3aukochakafp4w4wt2g548vm9giod9','NjA1NTM5ZTgyMTRhNzliZGE4NGU0ZTQ4OTBkNDBiYjc0Nzk5MGMwMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYjkxM2MwOTA0NjQ3ODE0MjE5NTc1OWJlNTU3OTdjZDFlYjA4MDhjMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-06-02 18:47:11.581444'),('9y9mtdrexu1lo17x112l6wbfg02rmje6','OGE5ZTRhNWNlYTNjNjU4YjU5MmNhZWY4NzUwNjJlNDNkZTVlNTgyNjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJmaXhzdGF0ZSI6IjAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiZml4dG90aGlzIjoiNjAifQ==','2019-05-19 18:13:56.833459'),('a26dx5r9zc0s9mjb2wqa3m8z1oikjxoo','MTgyZDJmNTBhY2M0OTRmZGQ0NDFlYjRkMjg3NTFlOTU1MTNjYjM2ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-06-16 19:58:04.485101'),('aq9yqx0zgoaf1txrrpktkaghsveueciq','YjE4MmZjYzA4ZTJkN2ZlMjQyYWEwNDhkNjc3OTFiZDVjZWI5MzA0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-12-01 12:42:49.904647'),('aye1bk06uoe3issurmwgc6z7afirjm3m','NDJjNDhiMzk1MmY2ZTJmMGNmNmUwODA3MjE5NjA5ZDk4MDNmNjUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-01-19 16:38:03.310882'),('b0cvvyukxgplka6c5qrgb2nwj01ifl7t','NDJjNDhiMzk1MmY2ZTJmMGNmNmUwODA3MjE5NjA5ZDk4MDNmNjUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2018-11-16 21:49:22.608693'),('dxmua26cx43qbnfztzfp2cyzzb1hftht','YjE4MmZjYzA4ZTJkN2ZlMjQyYWEwNDhkNjc3OTFiZDVjZWI5MzA0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-08-12 13:23:27.980103'),('gykiq3osjst1x1gxdbfbkhfjn6tlfcxi','MGQzZTIwNTRkNTY3NjhkZmEwNGM1OTc1NTE4MTRjOTMwZmYwMzIyYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-09-12 19:48:29.288640'),('i4tiricjp7ccot2lpdqh5268xdjs5k5z','MGQzZTIwNTRkNTY3NjhkZmEwNGM1OTc1NTE4MTRjOTMwZmYwMzIyYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-09-09 18:57:23.409142'),('i5mbqabs74jz5l69gvaioxrwdwic3qia','ZTk1YjRlOWIwNjM3OTRmMGZiMjg4YTBlNTM2ZjMwODkwNzZlZGU4Mjp7ImZpeHN0YXRlIjoiMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJmaXh0b3RoaXMiOiI2MCIsIl9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEifQ==','2019-05-03 11:52:48.908167'),('j3lyn0r7a32bwidqa1uqr5zp7enrcp9i','NDJjNDhiMzk1MmY2ZTJmMGNmNmUwODA3MjE5NjA5ZDk4MDNmNjUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-09-23 20:00:13.931797'),('n4qaqds5eq7rc83pidhu2xlvolu6trvg','NDJjNDhiMzk1MmY2ZTJmMGNmNmUwODA3MjE5NjA5ZDk4MDNmNjUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-08-26 16:26:25.928342'),('rwn2epelhgtgjtcj2sf101aso4c3u9zk','OThiMWE3ZDA2YTIzMzQ4MjQ4YmNkOGY1YjVmOWFjNGMyMzZmMmY4Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYjkxM2MwOTA0NjQ3ODE0MjE5NTc1OWJlNTU3OTdjZDFlYjA4MDhjMSIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-02-19 17:48:27.184811'),('tczl8t47bfusc9qpc9kqogt6kh39ko43','MTgyZDJmNTBhY2M0OTRmZGQ0NDFlYjRkMjg3NTFlOTU1MTNjYjM2ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-07-15 11:58:16.642030'),('uzbpco32gm1hzj1v0tsa1gyq906mmp9c','ZTZhMDRmYjQxNDc4ZTVjY2JjNDcyY2Q3MTgwNDA5YTZkOTI0MWQzOTp7Im9uZml4IjowLCJmaXh0b3RoaXMiOiI2NCIsIl9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJmaXhzdGF0ZSI6IjAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-03-11 19:13:38.670006'),('wjx5sx3zxtyrg3pei8b8m4u219ohltgb','MGQzZTIwNTRkNTY3NjhkZmEwNGM1OTc1NTE4MTRjOTMwZmYwMzIyYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-12-18 12:33:53.181723'),('wp3odyud0t4o9f9emekbgmujzfv0ymjw','YjE4MmZjYzA4ZTJkN2ZlMjQyYWEwNDhkNjc3OTFiZDVjZWI5MzA0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-07-01 08:40:42.146623');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ist_tblIssue`
--

DROP TABLE IF EXISTS `ist_tblIssue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ist_tblIssue` (
  `issueid_tblissue` int(11) NOT NULL AUTO_INCREMENT,
  `title_tblIssue` varchar(200) NOT NULL,
  `text_tblIssue` longtext NOT NULL,
  `created_tblIssue` datetime(6) NOT NULL,
  `author_tblIssue_id` int(11) NOT NULL,
  PRIMARY KEY (`issueid_tblissue`),
  KEY `ist_tblissue_author_tblIssue_id_63962c65_fk_auth_user_id` (`author_tblIssue_id`),
  CONSTRAINT `ist_tblissue_author_tblIssue_id_63962c65_fk_auth_user_id` FOREIGN KEY (`author_tblIssue_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ist_tblIssue`
--

LOCK TABLES `ist_tblIssue` WRITE;
/*!40000 ALTER TABLE `ist_tblIssue` DISABLE KEYS */;
/*!40000 ALTER TABLE `ist_tblIssue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ist_tblIssuechange`
--

DROP TABLE IF EXISTS `ist_tblIssuechange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ist_tblIssuechange` (
  `issuechangeid_tblIssuechange` int(11) NOT NULL AUTO_INCREMENT,
  `issueid_tblIssuechange` int(11) NOT NULL,
  PRIMARY KEY (`issuechangeid_tblIssuechange`),
  CONSTRAINT `Fk_tblIssuechange_tblIssue` FOREIGN KEY (`issuechangeid_tblIssuechange`) REFERENCES `ist_tblIssue` (`issueid_tblissue`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ist_tblIssuechange`
--

LOCK TABLES `ist_tblIssuechange` WRITE;
/*!40000 ALTER TABLE `ist_tblIssuechange` DISABLE KEYS */;
/*!40000 ALTER TABLE `ist_tblIssuechange` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet`
--

DROP TABLE IF EXISTS `pet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pet` (
  `name` varchar(20) DEFAULT NULL,
  `owner` varchar(20) DEFAULT NULL,
  `species` varchar(20) DEFAULT NULL,
  `sex` char(1) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `death` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet`
--

LOCK TABLES `pet` WRITE;
/*!40000 ALTER TABLE `pet` DISABLE KEYS */;
/*!40000 ALTER TABLE `pet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblbackpageforquotation`
--

DROP TABLE IF EXISTS `quotation_tblbackpageforquotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblbackpageforquotation` (
  `backpageidforquotation_tblbackpageforquotation` int(11) NOT NULL AUTO_INCREMENT,
  `backpagetextforquotation_tblbackpageforquotation` text NOT NULL,
  `backpagenameforquotation_tblbackpageforquotation` varchar(200) NOT NULL,
  `creationtime_tblbackpageforquotation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `obsolete_tblbackpageforquotation` int(2) DEFAULT '0',
  PRIMARY KEY (`backpageidforquotation_tblbackpageforquotation`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblbackpageforquotation`
--

LOCK TABLES `quotation_tblbackpageforquotation` WRITE;
/*!40000 ALTER TABLE `quotation_tblbackpageforquotation` DISABLE KEYS */;
INSERT INTO `quotation_tblbackpageforquotation` VALUES (2,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','backpage standard','2019-02-10 17:15:12',0),(3,'Backpage text222222222','Backpage non standard','2019-02-10 17:15:12',0);
/*!40000 ALTER TABLE `quotation_tblbackpageforquotation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblchartofaccounts`
--

DROP TABLE IF EXISTS `quotation_tblchartofaccounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblchartofaccounts` (
  `accountid_tblchartofaccounts` varchar(10) DEFAULT NULL,
  `nameHU_tblchartofaccounts` varchar(100) DEFAULT NULL,
  `COL 3` varchar(1) DEFAULT NULL,
  `COL 4` varchar(1) DEFAULT NULL,
  `name_tblchartofaccounts` varchar(100) DEFAULT NULL,
  UNIQUE KEY `accountid_tblchartofaccounts` (`accountid_tblchartofaccounts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblchartofaccounts`
--

LOCK TABLES `quotation_tblchartofaccounts` WRITE;
/*!40000 ALTER TABLE `quotation_tblchartofaccounts` DISABLE KEYS */;
INSERT INTO `quotation_tblchartofaccounts` VALUES ('1','Egyes számlaosztály','2','1','Nr 1 class of accounts'),('2','Kettes számlaosztály','2','1',NULL),('3','Hármas számlaosztály','2','1',NULL),('4','Négyes számlaosztály','2','1',NULL),('5','Ötös számlaosztály','2','2',NULL),('8','Nyolcas számlaosztály','2','1',NULL),('9','Kilences számlaosztály','2','1',NULL),('38','Pénzeszközök','2','1','Cashes'),('58','Aktivált saját teljesítmények értéke','1','2',NULL),('87','Pénzügyi műveletek ráfordításai','1','2',NULL),('91','Belföldi értékesítés árbevétele','1','2',NULL),('97','Pénzügyi műveletek bevételei','1','2',NULL),('131','Termelő gépek, berendezések, szerszámok, gyártóeszközök','1','1',NULL),('142','Egyéb járművek','1','1',NULL),('143','Irodai berendezések és felszerelések','1','1',NULL),('149','Egyéb járművek, felszerelések terv sz. é.cs.-e','1','1',NULL),('161','Befejezetlen beruházások','1','1',NULL),('181','Államkötvények','1','1',NULL),('211','Nyers-és alapanyagok','1','1',NULL),('261','Áruk beszerzési áron','1','1',NULL),('271','Közvetített szolgáltatások','1','1',NULL),('311','Belföldi követelések (vevők)','1','1',NULL),('366','Értékpapírokkal kapcsolatos követelések','1','1',NULL),('384','Elszámolási betétszámla 57600101-11063939','1','1',NULL),('389','Átvezetési számla','1','1',NULL),('391','Bevételek aktív időbeli elhatárolása','1','1',NULL),('392','Költségek, ráfordítások aktív időbeli elhatárolása','1','1',NULL),('411','Jegyzett tőke','1','1',NULL),('413','Eredménytartalék','1','1',NULL),('419','Mérleg szerinti eredmény','1','1',NULL),('421','Céltartalék','1','1',NULL),('455','Beruházási szállítók','1','1',NULL),('461','Társasági adó elszámolása','1','1',NULL),('462','Személyi jövedelemadó elszámolása','1','1',NULL),('463','Költségvetési befizetési kötelezettségek','1','1',NULL),('464','Költségvetési befiz. köt. Teljesítése','1','1',NULL),('466','Előzetesen felszámított ÁFA','1','1',NULL),('467','Fizetendő ÁFA','1','1',NULL),('468','ÁFA pénzügyi elszámolási számla','1','1',NULL),('469','Helyi (önkormányzati) adók elszámolási számla','1','1',NULL),('471','Jövedelemelszámolási számla','1','1',NULL),('473','Társadalombiztosítási kötelezettség','1','1',NULL),('481','Bevételek passzív időbeli elhatárolása','1','1',NULL),('482','Költségek, ráfordítások passzív időbeli elhat.-a','1','1',NULL),('491','Nyitómérleg számla','1','2',NULL),('493','Tárgyévi eredmény elszámolása','1','2',NULL),('522','Bérleti díj','1','2',NULL),('523','Szállítási és raktározási költségek','1','2',NULL),('524','Igénybe vett szolgáltatások költségei','1','2',NULL),('531','Hatósági igazgatási, szolg.-i díjak, illetékek','1','2',NULL),('532','Pénzügyi, befektetési szolgáltatási díjak','1','2',NULL),('533','Biztosítási díj','1','2',NULL),('534','Költségként elszámolandó adók','1','2',NULL),('541','Alkalmazottak munkabére','1','2',NULL),('561','Nyugdíjbiztosítási és egészségbiztosítási járulék','1','2',NULL),('562','Egészségügyi hozzájárulás','1','2',NULL),('563','Munkaadói járulék','1','2',NULL),('564','Szakképzési hozzájárulás','1','2',NULL),('571','Terv szerinti értékcsökkenési leírás','1','2',NULL),('812','Igénybe vett szolgáltatások értéke','1','2',NULL),('813','Egyéb szolgáltatások értéke','1','2',NULL),('814','Eladott áruk beszerzési értéke','1','2',NULL),('867','Adók, illetékek, hozzájárulások','1','2',NULL),('869','Egyéb ráfordítás (pl. kerekítési különbözet)','1','2',NULL),('891','Társasági adó','1','2',NULL),('969','Egyéb bevételek (pl. kerekítési különbözet)','1','2',NULL),('973','Befektetett p.ü.-i eszközök kamatai, árf.nyeresége','1','2',NULL),('974','Egyéb kapott kamatok és kamatjellegű bevételek','1','2',NULL),('3811','Pénztár','1','1',NULL),('3812','Elektronikus pénzeszközök','1','1',NULL),('3854','Imp.fedezetre elkül. pénzeszk. 57600101-11065625','1','1',NULL),('3858','HEFOP-angol nyelvi képzés 57600101-11082242','1','1',NULL),('3861','Lekötetlen devizabetét (GBP) 11501000-40730804','1','1',NULL),('3864','Lekötött devizabetét (GBP) 11501000-40738060','1','1',NULL),('3868','Belf. pénzforgalmi látraszóló devizaszámla (EUR)','1','1',NULL),('4144','Fejlesztési tartalék','1','1',NULL),('4541','Belföldi szállítók','1','1',NULL),('4542','Külföldi szállítók','1','1',NULL),('4543','Belföldi szolgáltatók','1','1',NULL),('4611','Társasági adó elszámolása (erre könyvelünk)','1','1',NULL),('4612','Társas vállalkozás különadója (erre könyvelünk)','1','1',NULL),('4634','Egészségügyi hozzájárulás','1','1',NULL),('4639','Szakképzési hozzájárulás','1','1',NULL),('4695','Helyi iparűzési adó elszámolási számla','1','1',NULL),('4696','Gépjárműadó','1','1',NULL),('4699','Egyéb helyi adók','1','1',NULL),('4743','Környezetvédelmi termékdíj','1','1',NULL),('4791','Biztosító intézetekkel szembeni kötelezettségek','1','1',NULL),('5111','Felhasznált anyagok költségei','1','2',NULL),('5113','Üzemanyag költségek','1','2',NULL),('5116','Nyomtatványok, irodaszerek költségei','1','2',NULL),('5271','Telefonköltség','1','2',NULL),('5272','Internet-költségek','1','2',NULL),('5273','Postaköltség','1','2',NULL),('5295','Hirdetés, reklám költségei','1','2',NULL),('5296','Oktatás és továbbképzés költségei','1','2',NULL),('5299','Egyéb igénybevett szolgáltatások költségei','1','2',NULL),('5391','Könyvviteli szolgáltatás költsége','1','2',NULL),('5392','Számítógéppel kapcsolatos költségek','1','2',NULL),('5393','Reprezentációs költségek','1','2',NULL),('5394','Szoftverfejlesztés','1','2',NULL),('5399','Egyéb költségek','1','2',NULL),('5511','Étkezési hozzájárulás','1','2',NULL),('8632','Bírság, kötbér, késedelmi kamat','1','2',NULL),('8672','Önkormányzatokkal elszámolt adók','','2',NULL),('8752','Értékpapírok beváltásának árfolyamvesztesége','1','2',NULL),('8761','Deviza forintra átváltásának árfolyamvesztesége','1','2',NULL),('9752','Értékpapír beváltásának árfolyamnyeresége','1','2',NULL),('9761','Deviza átváltásának árfolyamnyeresége','1','2',NULL),('38512','Fix lekötésű betét (HUF)','1','1',NULL),('46312','Munkaadói járulék','1','1',NULL),('46313','Munkavállalói járulék','1','1',NULL),('46314','Nyugdíjbiztosítási járulék','1','1',NULL),('46315','Egészségbiztosítási járulék','1','1',NULL),('46318','Késedelmi pótlék','1','1',NULL),('51121','IWH segédanyag költségei','1','2',NULL),('51122','EWM segédanyag költségei','1','2',NULL),('51123','GZX segédanyag költségei','1','2',NULL),('51124','LMF685 segédanyag költségei','1','2',NULL),('51131','IWH üzemanyag','1','2',NULL),('51132','EWM üzemanyag','1','2',NULL),('51133','GZX üzemanyag','1','2',NULL),('51134','LMF685 üzemanyag','','2',NULL),('57123','Kisértékű tárgyi eszköz terv sz. é.cs.-i leírása','1','2',NULL),('111111','Szinkronizáció','1','1',NULL),('222222','Szinkronizáció','1','1',NULL),('333333','Szinkronizáció','1','1',NULL),('444444','Szinkronizáció','1','1',NULL),('','','','',NULL);
/*!40000 ALTER TABLE `quotation_tblchartofaccounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblcompanies`
--

DROP TABLE IF EXISTS `quotation_tblcompanies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblcompanies` (
  `Companyid_tblCompanies` int(11) NOT NULL AUTO_INCREMENT,
  `companyname_tblcompanies` varchar(200) NOT NULL,
  `defaultbackpageidforquotation_tblcompanies` int(11) DEFAULT '2',
  `defaultprefaceidforquotation_tblcompanies` int(11) DEFAULT '2',
  `pcd_tblcompanies` varchar(20) DEFAULT NULL,
  `town_tblcompanies` varchar(55) DEFAULT NULL,
  `address_tblcompanies` text,
  `defaultpaymentid_tblcompanies` int(11) NOT NULL DEFAULT '2',
  `stockflag_tblcompanies` int(11) DEFAULT '0',
  `lateststocktaking_tblcompanies` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`Companyid_tblCompanies`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblcompanies`
--

LOCK TABLES `quotation_tblcompanies` WRITE;
/*!40000 ALTER TABLE `quotation_tblcompanies` DISABLE KEYS */;
INSERT INTO `quotation_tblcompanies` VALUES (1,'Apple Inc.',2,2,'6726','Szeged','Akácfa u. 16.',1,0,NULL),(2,'General Mills',2,2,NULL,'Nebraska',NULL,2,0,NULL),(6,'Czapár Kft.',2,2,'6724','Szeged','Gáspár Zoltán u.',2,0,NULL),(7,'Gerebitz Zrt',2,2,'6724','Szeged','Űrhajós u.',2,0,NULL),(8,'Gipsz Bt.',2,2,'6711','Pitricsom','Fő u. 1.',2,0,NULL),(9,'Central Stock',2,2,NULL,NULL,NULL,2,1,'2019-07-10 17:39:00'),(10,'Stock2',2,2,NULL,NULL,NULL,2,1,'2019-07-12 08:48:00'),(11,'Öcsöd Team',2,2,'5000','Harangzug','Kiülő 1.',2,0,NULL);
/*!40000 ALTER TABLE `quotation_tblcompanies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblcontacts`
--

DROP TABLE IF EXISTS `quotation_tblcontacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblcontacts` (
  `Contactid_tblContacts` int(11) NOT NULL AUTO_INCREMENT,
  `firstname_tblcontacts` varchar(200) DEFAULT NULL,
  `lastname_tblcontacts` varchar(200) DEFAULT NULL,
  `Companyid_tblContacts_id` int(11) NOT NULL,
  `title_tblcontacts` varchar(10) DEFAULT NULL,
  `mobile_tblcontacts` varchar(40) DEFAULT NULL,
  `email_tblcontacts` varchar(50) DEFAULT NULL,
  `purchaseordercontact_tblcontacts` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Contactid_tblContacts`),
  KEY `quotation_tblcontact_Companyid_tblContact_26be7ab6_fk_quotation` (`Companyid_tblContacts_id`),
  CONSTRAINT `quotation_tblcontact_Companyid_tblContact_26be7ab6_fk_quotation` FOREIGN KEY (`Companyid_tblContacts_id`) REFERENCES `quotation_tblcompanies` (`Companyid_tblCompanies`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblcontacts`
--

LOCK TABLES `quotation_tblcontacts` WRITE;
/*!40000 ALTER TABLE `quotation_tblcontacts` DISABLE KEYS */;
INSERT INTO `quotation_tblcontacts` VALUES (1,'Arnold','Czapár',6,'Mr','+363011111111','szluka.mate@gmail.com',1),(2,'General','Manager',2,'Ms','+35301111111','szluka.mate@gmail.com',1),(3,'Non Generalll','Non Manager',2,'Mrs','+35301111112','szluka.mate@gmail.com',0),(4,'Steve','Jobs',1,'Mr','+363011111119','szluka.mate@gmail.com',1),(5,'Viktor','Szluka',1,'Mr','+3630','ttjugt357',0),(6,'Defaultx',NULL,1,NULL,NULL,'Noneu',0),(7,'András','Gerebitz',7,'Mr','+363011111111','szluka.mate@gmail.com',1),(8,'Jakab','Gipsz',8,'Mr','+36301111111','szluka.mate@gmail.com',1),(9,'Central Stock Contact',NULL,9,'Mr/Ms',NULL,NULL,0),(11,'Stock2 Contact',NULL,10,NULL,NULL,NULL,0),(12,'András','Gerebitz',11,'Mr','+36301234567','szluka.mate@gmail.com',0);
/*!40000 ALTER TABLE `quotation_tblcontacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblcurrency`
--

DROP TABLE IF EXISTS `quotation_tblcurrency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblcurrency` (
  `currencyid_tblcurrency` int(11) NOT NULL AUTO_INCREMENT,
  `currencyisocode_tblcurrency` varchar(10) DEFAULT NULL,
  `currencydescription_tblcurrency` varchar(50) DEFAULT NULL,
  `currencyrate_tblcurrency` float DEFAULT NULL,
  `obsolete_tblcurrency` int(3) NOT NULL DEFAULT '0',
  `creationtime_tblcurrency` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `accountcurrency_tblcurrency` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`currencyid_tblcurrency`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblcurrency`
--

LOCK TABLES `quotation_tblcurrency` WRITE;
/*!40000 ALTER TABLE `quotation_tblcurrency` DISABLE KEYS */;
INSERT INTO `quotation_tblcurrency` VALUES (1,'HUF','Hungarian Forint',1,0,'2019-02-16 17:04:48',1),(2,'USD','United States Dollar',280,0,'2019-02-16 17:04:48',0),(3,'EUR','European Union Currency',330,0,'2019-02-16 17:04:48',0);
/*!40000 ALTER TABLE `quotation_tblcurrency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tbldoc`
--

DROP TABLE IF EXISTS `quotation_tbldoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tbldoc` (
  `Docid_tblDoc` int(11) NOT NULL AUTO_INCREMENT,
  `Pcd_tblDoc` varchar(200) DEFAULT NULL,
  `Town_tblDoc` varchar(200) DEFAULT NULL,
  `Doc_kindid_tblDoc_id` int(11) NOT NULL,
  `Contactid_tblDoc_id` int(11) DEFAULT NULL,
  `companyname_tblcompanies_ctbldoc` varchar(200) DEFAULT NULL,
  `firstname_tblcontacts_ctbldoc` varchar(200) DEFAULT NULL,
  `lastname_tblcontacts_ctbldoc` varchar(200) DEFAULT NULL,
  `creationtime_tbldoc` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `prefacetextforquotation_tblprefaceforquotation_ctbldoc` text,
  `obsolete_tbldoc` int(11) NOT NULL DEFAULT '0',
  `backpagetextforquotation_tblbackpageforquotation_ctbldoc` text,
  `prefacespecforquotation_tbldoc` text,
  `subject_tbldoc` varchar(255) DEFAULT NULL,
  `docnumber_tbldoc` int(10) DEFAULT '101',
  `creatorid_tbldoc` int(10) DEFAULT NULL,
  `title_tblcontacts_ctbldoc` varchar(20) DEFAULT NULL,
  `mobile_tblcontacts_ctbldoc` varchar(50) DEFAULT NULL,
  `email_tblcontacts_ctbldoc` varchar(50) DEFAULT NULL,
  `pcd_tblcompanies_ctbldoc` varchar(20) DEFAULT NULL,
  `town_tblcompanies_ctbldoc` varchar(55) DEFAULT NULL,
  `address_tblcompanies_ctbldoc` text,
  `total_tbldoc` varchar(10) NOT NULL DEFAULT 'Total_off',
  `deliverydays_tbldoc` int(3) DEFAULT NULL,
  `paymenttextforquotation_tblpayment_ctbldoc` text,
  `currencycodeinreport_tbldoc` varchar(3) DEFAULT 'HUF',
  `currencyrateinreport_tbldoc` float DEFAULT '1',
  `doclinkparentid_tbldoc` int(11) DEFAULT NULL,
  `accountcurrencycode_tbldoc` varchar(5) DEFAULT NULL,
  `debitaccountid_tbldoc` varchar(10) DEFAULT NULL,
  `creditaccountid_tbldoc` varchar(10) DEFAULT NULL,
  `accountvalue_tbldoc` float DEFAULT NULL,
  `accountduedate_tbldoc` date DEFAULT NULL,
  `emailbodytextmodifiedbyuser_tbldoc` longtext,
  `cc_tbldoc` longtext,
  `duedate_tbldoc` date DEFAULT NULL,
  `wherefromdocid_tbldoc` int(11) DEFAULT NULL,
  `wheretodocid_tbldoc` int(11) DEFAULT NULL,
  `denoenabledflag_tbldoc` int(11) DEFAULT '1',
  `stocktakingdeno_tbldoc` int(11) DEFAULT '0',
  `backtostockforcordocid_tbldoc` int(11) DEFAULT NULL,
  `machinemadedocflag_tbldoc` int(11) DEFAULT '0',
  `dateofcompletiononcustomerinvoice_tbldoc` date DEFAULT NULL,
  `deadlineforpaymentoncustomerinvoice_tbldoc` date DEFAULT NULL,
  `numberoforderoncustomerinvoice_tbldoc` varchar(30) DEFAULT NULL,
  `deferredpaymentdaysinquotation_tbldoc` int(11) DEFAULT '8',
  `deferredpaymentdaysincustomerorder_tbldoc` int(11) DEFAULT '8',
  `dateoforderoncustomerinvoice_tbldoc` date DEFAULT NULL,
  `currencyincustomerinvoice_tbldoc` varchar(5) DEFAULT 'HUF',
  `currencyrateforitemsincustomerinvoice_tbldoc` float DEFAULT '1',
  `remarksincustomerinvoice_tbldoc` longtext,
  `customerorderdocidforcustomerinvoice_tbldoc` int(11) DEFAULT NULL,
  PRIMARY KEY (`Docid_tblDoc`),
  KEY `quotation_tbldoc_Doc_kindid_tblDoc_id_844f8ed6_fk_quotation` (`Doc_kindid_tblDoc_id`),
  KEY `quotation_tbldoc_Contactid_tblDoc_id_0de2ee97_fk_quotation` (`Contactid_tblDoc_id`),
  CONSTRAINT `quotation_tbldoc_Contactid_tblDoc_id_0de2ee97_fk_quotation` FOREIGN KEY (`Contactid_tblDoc_id`) REFERENCES `quotation_tblcontacts` (`Contactid_tblContacts`),
  CONSTRAINT `quotation_tbldoc_Doc_kindid_tblDoc_id_844f8ed6_fk_quotation` FOREIGN KEY (`Doc_kindid_tblDoc_id`) REFERENCES `quotation_tbldoc_kind` (`Doc_kindid_tblDoc_kind`)
) ENGINE=InnoDB AUTO_INCREMENT=2426 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tbldoc`
--

LOCK TABLES `quotation_tbldoc` WRITE;
/*!40000 ALTER TABLE `quotation_tbldoc` DISABLE KEYS */;
INSERT INTO `quotation_tbldoc` VALUES (2410,NULL,NULL,2,9,'Central Stock','Central Stock Contact',NULL,'2019-09-05 16:00:00','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n',NULL,NULL,248,1,'Mr/Ms',NULL,NULL,NULL,NULL,NULL,'Total_off',NULL,'Cash','HUF',1,NULL,'HUF',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,0,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2411,NULL,NULL,7,8,'Apple Inc.','Steve','Jobs','2019-09-05 16:01:34','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',700,1,'Mr','+363011111119','szluka.mate@gmail.com','6726','Szeged','Akácfa u. 16.','Total_On',12,'Wire transfer after due date 8 days','EUR',1,60,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,0,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2412,NULL,NULL,8,9,'Central Stock','Central Stock Contact',NULL,'2019-09-05 16:33:28','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n',NULL,'None',1869,1,'Mr/Ms',NULL,NULL,NULL,NULL,NULL,'Total_off',NULL,'Cash','HUF',1,2410,'HUF',NULL,NULL,NULL,NULL,NULL,NULL,NULL,2411,2410,1,0,NULL,1,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2413,NULL,NULL,8,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-05 16:36:41','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',1870,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1382,425,1,0,NULL,0,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2414,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-05 16:36:53','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',114,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-05','2019-09-15','COR-177',8,8,'2019-05-01','HUF',10,NULL,425),(2415,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-07 14:05:34','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',115,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-07','2019-09-17','COR-177',8,8,'2019-05-01','USD',290,NULL,425),(2416,NULL,NULL,2,9,'Central Stock','Central Stock Contact',NULL,'2019-09-09 16:28:08','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n',NULL,NULL,249,1,'Mr/Ms',NULL,NULL,NULL,NULL,NULL,'Total_off',NULL,'Cash','HUF',1,NULL,'HUF',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,0,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2417,NULL,NULL,7,8,'Apple Inc.','Steve','Jobs','2019-09-09 16:28:47','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',701,1,'Mr','+363011111119','szluka.mate@gmail.com','6726','Szeged','Akácfa u. 16.','Total_On',12,'Wire transfer after due date 8 days','USD',1,60,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0,NULL,0,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2418,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-10 20:45:09','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',116,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-10','2019-09-20','COR-177',8,8,'2019-05-01','USD',290,'None\nj\n\nj\n',425),(2419,NULL,NULL,8,9,'Central Stock','Central Stock Contact',NULL,'2019-09-12 18:52:28','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n',NULL,'None',1871,1,'Mr/Ms',NULL,NULL,NULL,NULL,NULL,'Total_off',NULL,'Cash','HUF',1,2416,'HUF',NULL,NULL,NULL,NULL,NULL,NULL,NULL,2417,2416,1,0,NULL,1,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2420,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-12 18:53:01','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',117,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-12','2019-09-22','COR-177',8,8,'2019-05-01','HUF',1,NULL,425),(2421,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-12 19:07:28','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',118,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-12','2019-09-22','COR-177',8,8,'2019-05-01','HUF',1,NULL,425),(2422,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-12 19:12:00','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',119,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-12','2019-09-22','COR-177',8,8,'2019-05-01','HUF',1,NULL,425),(2423,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-12 19:37:21','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',120,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-12','2019-09-22','COR-177',8,8,'2019-05-01','HUF',1,NULL,425),(2424,NULL,NULL,8,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-12 19:38:17','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',1872,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,2377,425,1,0,NULL,1,NULL,NULL,NULL,8,8,NULL,'HUF',1,NULL,NULL),(2425,NULL,NULL,3,8,'Gipsz Bt.','Jakab','Gipsz','2019-09-12 19:40:29','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'<p>Quotation validity: 30 calendar days from date of quotation.</p>\r\n<p>Delivery date: data1 calendar days maximum from date of order.</p>\r\n<p>Payment conditions: data2</p>\r\n','uuuuuuuuuu pfs','Levelling',121,1,'Mr','+36301111111','szluka.mate@gmail.com','6711','Pitricsom','Fő u. 1.','Total_On',12,'Wire transfer','HUF',220,425,'1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,425,1,0,NULL,0,'2019-09-12','2019-09-22','COR-177',8,8,'2019-05-01','HUF',1,NULL,425);
/*!40000 ALTER TABLE `quotation_tbldoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tbldoc_details`
--

DROP TABLE IF EXISTS `quotation_tbldoc_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tbldoc_details` (
  `Doc_detailsid_tblDoc_details` int(11) NOT NULL AUTO_INCREMENT,
  `Qty_tblDoc_details` decimal(10,1) NOT NULL DEFAULT '1.0',
  `Docid_tblDoc_details_id` int(11) NOT NULL,
  `Productid_tblDoc_details_id` int(11) DEFAULT NULL,
  `firstnum_tblDoc_details` int(11) NOT NULL DEFAULT '1',
  `fourthnum_tblDoc_details` int(11) NOT NULL DEFAULT '0',
  `secondnum_tblDoc_details` int(11) NOT NULL DEFAULT '0',
  `thirdnum_tblDoc_details` int(11) NOT NULL DEFAULT '0',
  `Note_tblDoc_details` varchar(200) DEFAULT NULL,
  `creationtime_tblDoc_details` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `purchase_price_tblproduct_ctblDoc_details` float DEFAULT NULL,
  `unitsalespriceACU_tblDoc_details` float DEFAULT NULL,
  `customerdescription_tblProduct_ctblDoc_details` text,
  `currencyisocode_tblcurrency_ctblproduct_ctblDoc_details` varchar(10) DEFAULT NULL,
  `discount_tblDoc_details` float DEFAULT NULL,
  `listprice_tblDoc_details` float DEFAULT NULL,
  `unit_tbldocdetails` varchar(20) NOT NULL DEFAULT 'pc(s)',
  `currencyrate_tblcurrency_ctblDoc_details` float DEFAULT NULL,
  `attachmentname_tbldocdetails` text,
  `attachmentsize_tbldocdetails` varchar(20) DEFAULT NULL,
  `attachmentcontent_tbldocdetails` longblob,
  `suppliercompanyid_tbldocdetails` int(11) NOT NULL DEFAULT '1',
  `supplierdescription_tblProduct_ctblDoc_details` longtext,
  `podetailslink_tbldocdetails` int(11) DEFAULT NULL,
  `dateofarrival_tbldocdetails` date DEFAULT NULL,
  `denotopodetailslink_tbldocdetails` int(11) DEFAULT NULL,
  `denofrom_tbldocdetails` int(11) DEFAULT NULL,
  `denoto_tbldocdetails` int(11) DEFAULT NULL,
  `creatorid_tbldocdetails` int(11) DEFAULT NULL,
  `podocdetailsidforlabel_tbldocdetails` int(11) DEFAULT NULL,
  `delete190804flag_tbldocdetails` int(11) DEFAULT '0',
  `vatpercentincustomerinvoice_tbldocdetails` int(11) DEFAULT '27',
  PRIMARY KEY (`Doc_detailsid_tblDoc_details`),
  KEY `quotation_tbldoc_det_Docid_tblDoc_details_118ffe05_fk_quotation` (`Docid_tblDoc_details_id`),
  CONSTRAINT `quotation_tbldoc_det_Docid_tblDoc_details_118ffe05_fk_quotation` FOREIGN KEY (`Docid_tblDoc_details_id`) REFERENCES `quotation_tbldoc` (`Docid_tblDoc`),
  CONSTRAINT `quotation_tbldoc_details_ibfk_1` FOREIGN KEY (`Docid_tblDoc_details_id`) REFERENCES `quotation_tbldoc` (`Docid_tblDoc`)
) ENGINE=InnoDB AUTO_INCREMENT=85213 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tbldoc_details`
--

LOCK TABLES `quotation_tbldoc_details` WRITE;
/*!40000 ALTER TABLE `quotation_tbldoc_details` DISABLE KEYS */;
INSERT INTO `quotation_tbldoc_details` VALUES (85127,1.0,2414,9,4,4,0,0,'Defaultnote','2019-09-05 16:36:53',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85128,1.0,2414,9,4,4,0,0,'Defaultnote','2019-09-05 16:36:53',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85129,3.0,2414,1,4,3,0,0,'Defaultnote','2019-09-05 16:36:53',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85130,3.0,2414,33,4,6,0,0,'Defaultnote','2019-09-05 16:36:53',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85131,7.0,2414,33,4,6,0,0,'Defaultnote','2019-09-05 16:36:53',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27),(85132,1.0,2415,11,4,2,0,0,'Defaultnote','2019-09-10 19:20:05',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,0),(85133,1.0,2415,11,4,2,0,0,'Defaultnote','2019-09-10 19:20:10',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,0),(85134,1.0,2415,11,4,2,0,0,'Defaultnote','2019-09-10 19:20:13',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,0),(85135,1.0,2415,9,4,4,0,0,'Defaultnote','2019-09-10 19:20:19',300,120000,'Iphone','USD',NULL,428.57,'pc',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,0),(85136,1.0,2415,9,4,4,0,0,'Defaultnote','2019-09-10 19:22:41',300,120000,'Iphone','USD',NULL,428.57,'pc',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,0),(85137,1.0,2415,9,4,4,0,0,'Defaultnote','2019-09-10 19:22:44',300,120000,'Iphone','USD',NULL,428.57,'pc',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,0),(85138,1.0,2415,9,4,4,0,0,'Defaultnote','2019-09-10 19:22:49',300,120000,'Iphone','USD',NULL,428.57,'pc',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,0),(85139,1.0,2415,9,4,4,0,0,'Defaultnote','2019-09-10 19:22:53',300,120000,'Iphone','USD',NULL,428.57,'pc',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,0),(85140,3.0,2415,1,4,3,0,0,'Defaultnote','2019-09-10 19:20:16',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85141,3.0,2415,33,4,6,0,0,'Defaultnote','2019-09-10 19:22:56',1,280,'Szlukabit MousePad','USD',NULL,1,'pc',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,0),(85142,7.0,2415,33,4,6,0,0,'Defaultnote','2019-09-10 19:23:16',1,280,'Szlukabit MousePad','USD',NULL,1,'pc',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,0),(85144,1.0,2416,1,2,0,0,0,'Defaultnote','2019-09-09 16:28:24',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,27),(85145,1.0,2417,1,2,0,0,0,'Defaultnote','2019-09-09 16:29:02',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',85144,'2019-09-09',NULL,NULL,NULL,NULL,NULL,0,27),(85146,1.0,2418,11,4,2,0,0,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww','2019-09-12 16:08:32',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,27),(85147,1.0,2418,11,4,2,0,0,'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww\nwwwwwwwwww\njwwwwwwwwwww','2019-09-12 08:22:10',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,27),(85148,1.0,2418,11,4,2,0,0,'Defaultnote','2019-09-10 20:45:09',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,27),(85149,1.0,2418,9,4,4,0,0,'Defaultnote','2019-09-10 20:45:09',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,27),(85150,1.0,2418,9,4,4,0,0,'Defaultnote','2019-09-10 20:45:09',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,27),(85151,1.0,2418,9,4,4,0,0,'Defaultnote','2019-09-10 20:45:09',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,27),(85152,1.0,2418,9,4,4,0,0,'Defaultnote','2019-09-10 20:45:09',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85153,1.0,2418,9,4,4,0,0,'Defaultnote','2019-09-10 20:45:09',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85154,3.0,2418,1,4,3,0,0,'Defaultnote','2019-09-11 19:40:42',6,10640,'Setup AWS EC2 Ubuntu serverr g','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85155,3.0,2418,33,4,6,0,0,'Defaultnote','2019-09-10 20:45:09',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85156,7.0,2418,33,4,6,0,0,'Defaultnote','2019-09-10 20:45:09',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27),(85157,1.0,2419,1,2,0,0,0,'Defaultnote','2019-09-12 18:52:28',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,85145,NULL,NULL,NULL,85145,0,27),(85158,1.0,2420,11,4,2,0,0,'Defaultnote','2019-09-12 18:53:01',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,27),(85159,1.0,2420,11,4,2,0,0,'Defaultnote','2019-09-12 18:53:01',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,27),(85160,1.0,2420,11,4,2,0,0,'Defaultnote','2019-09-12 18:53:01',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,27),(85161,1.0,2420,9,4,4,0,0,'Defaultnote','2019-09-12 18:53:01',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,27),(85162,1.0,2420,9,4,4,0,0,'Defaultnote','2019-09-12 18:53:01',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,27),(85163,1.0,2420,9,4,4,0,0,'Defaultnote','2019-09-12 18:53:01',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,27),(85164,1.0,2420,9,4,4,0,0,'Defaultnote','2019-09-12 18:53:01',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85165,1.0,2420,9,4,4,0,0,'Defaultnote','2019-09-12 18:53:01',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85166,3.0,2420,1,4,3,0,0,'Defaultnote','2019-09-12 18:53:01',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85167,3.0,2420,33,4,6,0,0,'Defaultnote','2019-09-12 18:53:01',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85168,7.0,2420,33,4,6,0,0,'Defaultnote','2019-09-12 18:53:01',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27),(85169,1.0,2421,11,4,2,0,0,'Defaultnote','2019-09-12 19:07:28',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,27),(85170,1.0,2421,11,4,2,0,0,'Defaultnote','2019-09-12 19:07:28',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,27),(85171,1.0,2421,11,4,2,0,0,'Defaultnote','2019-09-12 19:07:28',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,27),(85172,1.0,2421,9,4,4,0,0,'Defaultnote','2019-09-12 19:07:28',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,27),(85173,1.0,2421,9,4,4,0,0,'Defaultnote','2019-09-12 19:07:28',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,27),(85174,1.0,2421,9,4,4,0,0,'Defaultnote','2019-09-12 19:07:28',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,27),(85175,1.0,2421,9,4,4,0,0,'Defaultnote','2019-09-12 19:07:28',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85176,1.0,2421,9,4,4,0,0,'Defaultnote','2019-09-12 19:07:28',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85177,3.0,2421,1,4,3,0,0,'Defaultnote','2019-09-12 19:07:28',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85178,3.0,2421,33,4,6,0,0,'Defaultnote','2019-09-12 19:07:28',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85179,7.0,2421,33,4,6,0,0,'Defaultnote','2019-09-12 19:07:28',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27),(85180,1.0,2422,11,4,2,0,0,'Defaultnote','2019-09-12 19:12:00',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,27),(85181,1.0,2422,11,4,2,0,0,'Defaultnote','2019-09-12 19:12:00',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,27),(85182,1.0,2422,11,4,2,0,0,'Defaultnote','2019-09-12 19:12:00',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,27),(85183,1.0,2422,9,4,4,0,0,'Defaultnote','2019-09-12 19:12:00',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,27),(85184,1.0,2422,9,4,4,0,0,'Defaultnote','2019-09-12 19:12:00',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,27),(85185,1.0,2422,9,4,4,0,0,'Defaultnote','2019-09-12 19:12:00',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,27),(85186,1.0,2422,9,4,4,0,0,'Defaultnote','2019-09-12 19:12:00',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85187,1.0,2422,9,4,4,0,0,'Defaultnote','2019-09-12 19:12:00',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85188,3.0,2422,1,4,3,0,0,'Defaultnote','2019-09-12 19:12:00',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85189,3.0,2422,33,4,6,0,0,'Defaultnote','2019-09-12 19:12:00',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85190,7.0,2422,33,4,6,0,0,'Defaultnote','2019-09-12 19:12:00',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27),(85191,1.0,2423,11,4,2,0,0,'Defaultnote','2019-09-12 19:37:21',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,27),(85192,1.0,2423,11,4,2,0,0,'Defaultnote','2019-09-12 19:37:21',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,27),(85193,1.0,2423,11,4,2,0,0,'Defaultnote','2019-09-12 19:37:21',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,27),(85194,1.0,2423,9,4,4,0,0,'Defaultnote','2019-09-12 19:37:21',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,27),(85195,1.0,2423,9,4,4,0,0,'Defaultnote','2019-09-12 19:37:21',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,27),(85196,1.0,2423,9,4,4,0,0,'Defaultnote','2019-09-12 19:37:21',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,27),(85197,1.0,2423,9,4,4,0,0,'Defaultnote','2019-09-12 19:37:21',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85198,1.0,2423,9,4,4,0,0,'Defaultnote','2019-09-12 19:37:21',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85199,3.0,2423,33,4,6,0,0,'Defaultnote','2019-09-12 19:37:21',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85200,7.0,2423,33,4,6,0,0,'Defaultnote','2019-09-12 19:37:21',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27),(85201,3.0,2424,1,4,3,0,0,'Defaultnote','2019-09-12 19:38:17',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,84996,NULL,NULL,NULL,84996,0,27),(85202,3.0,2425,1,4,3,0,0,'Defaultnote','2019-09-12 19:40:29',6,10640,'Setup AWS EC2 Ubuntu serverr','USD',NULL,38,'pc(s)',280,NULL,NULL,NULL,1,'Setup AWS supplierdescription',NULL,NULL,NULL,NULL,NULL,NULL,84996,0,27),(85203,1.0,2425,11,4,2,0,0,'wwww','2019-09-12 19:48:32',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85112,0,27),(85204,1.0,2425,11,4,2,0,0,'Defaultnote','2019-09-12 19:40:29',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85113,0,27),(85205,1.0,2425,11,4,2,0,0,'Defaultnote','2019-09-12 19:40:29',220,103716,'Ipod EUR','EUR',NULL,314.29,'pc(s)',330,NULL,NULL,NULL,1,'Ipod EUR supplier description',NULL,NULL,NULL,NULL,NULL,NULL,85114,0,27),(85206,1.0,2425,9,4,4,0,0,'Defaultnote','2019-09-12 19:40:29',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85047,0,27),(85207,1.0,2425,9,4,4,0,0,'Defaultnote','2019-09-12 19:40:29',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,85048,0,27),(85208,1.0,2425,9,4,4,0,0,'Defaultnote','2019-09-12 19:40:29',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85004,0,27),(85209,1.0,2425,9,4,4,0,0,'Defaultnote','2019-09-12 19:40:29',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85005,0,27),(85210,1.0,2425,9,4,4,0,0,'Defaultnote','2019-09-12 19:40:29',300,120000,'Iphone','USD',NULL,428.57,'pc(s)',280,NULL,NULL,NULL,1,'Iphone kit + 10 year warranty',NULL,NULL,NULL,NULL,NULL,NULL,85006,0,27),(85211,3.0,2425,33,4,6,0,0,'Defaultnote','2019-09-12 19:40:29',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,84989,0,27),(85212,7.0,2425,33,4,6,0,0,'Defaultnote','2019-09-12 19:40:29',1,280,'Szlukabit MousePad','USD',NULL,1,'pc(s)',280,NULL,NULL,NULL,1,'Szlukabit MousePad supplier description',NULL,NULL,NULL,NULL,NULL,NULL,83152,0,27);
/*!40000 ALTER TABLE `quotation_tbldoc_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tbldoc_kind`
--

DROP TABLE IF EXISTS `quotation_tbldoc_kind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tbldoc_kind` (
  `Doc_kindid_tblDoc_kind` int(11) NOT NULL AUTO_INCREMENT,
  `Doc_kind_name_tblDoc_kind` varchar(200) NOT NULL,
  `pretag_tbldockind` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`Doc_kindid_tblDoc_kind`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tbldoc_kind`
--

LOCK TABLES `quotation_tbldoc_kind` WRITE;
/*!40000 ALTER TABLE `quotation_tbldoc_kind` DISABLE KEYS */;
INSERT INTO `quotation_tbldoc_kind` VALUES (1,'Customer_Quotation','CQ-'),(2,'Customer_Order','COR-'),(3,'Customer_Invoice','CI-'),(4,'Job Number','JNUM-'),(5,'Email','EMAIL-'),(6,'Accounting_Entry','ACCENT-'),(7,'Purchase_Order','PO-'),(8,'Delivery Note','DENO-');
/*!40000 ALTER TABLE `quotation_tbldoc_kind` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblincomestatement`
--

DROP TABLE IF EXISTS `quotation_tblincomestatement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblincomestatement` (
  `rowid_tblincomestatement` int(11) NOT NULL AUTO_INCREMENT,
  `order_tblincomestatement` varchar(10) DEFAULT NULL,
  `rowname_tblincomestatement` varchar(85) DEFAULT NULL,
  PRIMARY KEY (`rowid_tblincomestatement`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblincomestatement`
--

LOCK TABLES `quotation_tblincomestatement` WRITE;
/*!40000 ALTER TABLE `quotation_tblincomestatement` DISABLE KEYS */;
INSERT INTO `quotation_tblincomestatement` VALUES (1,'010','Inventory'),(2,'020','Income');
/*!40000 ALTER TABLE `quotation_tblincomestatement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblincomestatementdetails`
--

DROP TABLE IF EXISTS `quotation_tblincomestatementdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblincomestatementdetails` (
  `rowid_tblincomestatementdetails` int(11) NOT NULL AUTO_INCREMENT,
  `operationsign_tblincomestatementdetails` varchar(2) DEFAULT NULL,
  `operationkind_tblincomestatementdetails` varchar(10) DEFAULT NULL,
  `side_tblincomestatementdetails` varchar(10) DEFAULT NULL,
  `generalledgeraccount_tblincomestatementdetails` varchar(15) DEFAULT NULL,
  `incomestatementrowid_tblincomestatementdetails` int(11) DEFAULT NULL,
  PRIMARY KEY (`rowid_tblincomestatementdetails`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblincomestatementdetails`
--

LOCK TABLES `quotation_tblincomestatementdetails` WRITE;
/*!40000 ALTER TABLE `quotation_tblincomestatementdetails` DISABLE KEYS */;
INSERT INTO `quotation_tblincomestatementdetails` VALUES (1,'+','Account','Debit','3',1),(2,'+','Account','Debit','9',2),(3,'+','Account','Debit','97',2);
/*!40000 ALTER TABLE `quotation_tblincomestatementdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblpayment`
--

DROP TABLE IF EXISTS `quotation_tblpayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblpayment` (
  `paymentid_tblpayment` int(11) NOT NULL AUTO_INCREMENT,
  `paymenttextforquotation_tblpayment` text,
  `paymentname_tblpayment` varchar(100) DEFAULT NULL,
  `creationtime_tblpayment` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `obsolete_tblpayment` int(3) NOT NULL DEFAULT '0',
  PRIMARY KEY (`paymentid_tblpayment`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblpayment`
--

LOCK TABLES `quotation_tblpayment` WRITE;
/*!40000 ALTER TABLE `quotation_tblpayment` DISABLE KEYS */;
INSERT INTO `quotation_tblpayment` VALUES (1,'Wire Transfer','Wire Transfer','2019-02-14 20:14:32',0),(2,'Cash','Cash','2019-02-14 20:48:46',0);
/*!40000 ALTER TABLE `quotation_tblpayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblprefaceforquotation`
--

DROP TABLE IF EXISTS `quotation_tblprefaceforquotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblprefaceforquotation` (
  `prefaceidforquotation_tblprefaceforquotation` int(11) NOT NULL AUTO_INCREMENT,
  `prefacetextforquotation_tblprefaceforquotation` text,
  `prefacenameforquotation_tblprefaceforquotation` varchar(200) DEFAULT NULL,
  `creationtime_tblprefaceforquotation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `obsolete_tblprefaceforquotation` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`prefaceidforquotation_tblprefaceforquotation`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblprefaceforquotation`
--

LOCK TABLES `quotation_tblprefaceforquotation` WRITE;
/*!40000 ALTER TABLE `quotation_tblprefaceforquotation` DISABLE KEYS */;
INSERT INTO `quotation_tblprefaceforquotation` VALUES (2,'Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n','Standard','2019-02-04 08:36:10',0),(3,'é   h                   n\r\n\r\n\r\nhh  f\r\n								\r\n								\r\n								','Non standard','2019-02-04 08:36:10',1),(4,'New1text','New1','2019-02-04 11:40:47',0),(5,'None','New2','2019-02-04 11:41:04',0);
/*!40000 ALTER TABLE `quotation_tblprefaceforquotation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblproduct`
--

DROP TABLE IF EXISTS `quotation_tblproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblproduct` (
  `Productid_tblProduct` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_price_tblproduct` float NOT NULL DEFAULT '0',
  `customerdescription_tblProduct` text,
  `currencyid_tblcurrency_fktblproduct` int(11) NOT NULL DEFAULT '1',
  `margin_tblproduct` float NOT NULL DEFAULT '0',
  `creationtime_tblproduct` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `currencyisocode_tblcurrency_ctblproduct` varchar(10) DEFAULT NULL,
  `obsolete_tblproduct` tinyint(1) NOT NULL DEFAULT '0',
  `unit_tblproduct` varchar(20) NOT NULL DEFAULT 'pc(s)',
  `suppliercompanyid_tblproduct` int(11) DEFAULT NULL,
  `supplierdescription_tblProduct` longtext,
  `discreteflag_tblproduct` int(11) DEFAULT '1',
  `serviceflag_tblproduct` int(11) DEFAULT '0',
  PRIMARY KEY (`Productid_tblProduct`),
  KEY `currencyid_tblcurrency_fktblproduct` (`currencyid_tblcurrency_fktblproduct`),
  CONSTRAINT `currencyid_tblcurrency_with_currencyid_tblproducts_fktblproduct` FOREIGN KEY (`currencyid_tblcurrency_fktblproduct`) REFERENCES `quotation_tblcurrency` (`currencyid_tblcurrency`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblproduct`
--

LOCK TABLES `quotation_tblproduct` WRITE;
/*!40000 ALTER TABLE `quotation_tblproduct` DISABLE KEYS */;
INSERT INTO `quotation_tblproduct` VALUES (1,6,'Setup AWS EC2 Ubuntu serverr',1,84.2105,'2018-12-17 09:54:39','USD',0,'pc(s)',1,'Setup AWS supplierdescription',1,1),(2,2553,'Something',2,15,'2018-12-17 09:54:39','HUF',1,'pc(s)',1,NULL,1,0),(4,80,'Pr5e',3,22,'2018-12-17 09:54:39','HUF',1,'pc(s)',1,NULL,1,0),(5,9,'Pr66',2,50,'2018-12-17 09:54:39','USD',1,'pc(s)',1,NULL,1,0),(6,7,'Standard Homepage (one page)',2,76.6667,'2018-12-17 09:54:39','USD',0,'hour',6,'Standard Homepage (one page) supplier description',0,1),(7,10,'Extra Scripting',1,66.6667,'2019-01-05 13:24:50','EUR',1,'pc(s)',2,'Bacon',1,1),(8,10,'Contact Form Scripting',1,50,'2019-01-05 13:25:16','EUR',0,'pc(s)',8,'Javascript+CSS+HTML Scripting',1,1),(9,300,'Iphone',1,30,'2019-01-05 13:25:17','USD',0,'pc(s)',1,'Iphone kit + 10 years warranty',1,0),(10,200,'Ipod',1,30,'2019-01-05 13:25:18','USD',1,'pc(s)',1,'Ipod supplier description',1,0),(11,220,'Ipod EUR',1,30,'2019-01-05 13:25:20','EUR',0,'pc(s)',1,'Ipod EUR supplier description',1,0),(12,0,'DefaultDescription',1,0,'2019-01-05 13:25:21',NULL,1,'pc(s)',1,NULL,1,0),(13,0,'DefaultDescription',1,0,'2019-01-05 13:25:21',NULL,1,'pc(s)',1,NULL,1,0),(14,0,'DefaultDescription',1,0,'2019-01-05 13:25:23',NULL,1,'pc(s)',1,NULL,1,0),(15,0,'DefaultDescription',1,0,'2019-01-05 13:25:26',NULL,1,'pc(s)',1,NULL,1,0),(16,0,'DefaultDescription',1,0,'2019-01-05 13:25:27',NULL,1,'pc(s)',1,NULL,1,0),(17,0,'DefaultDescription',1,0,'2019-01-05 13:25:28',NULL,1,'pc(s)',1,'None',1,0),(18,0,'DefaultDescription',1,0,'2019-01-05 13:25:29',NULL,1,'pc(s)',1,NULL,1,0),(19,0,'DefaultDescription',1,0,'2019-01-05 13:25:30',NULL,1,'pc(s)',1,NULL,1,0),(20,0,'DefaultDescription',1,0,'2019-01-05 13:25:32',NULL,1,'pc(s)',1,NULL,1,0),(21,0,'DefaultDescription',1,0,'2019-01-05 13:25:33',NULL,1,'pc(s)',1,NULL,1,0),(22,0,'DefaultDescription',1,0,'2019-01-05 13:25:33',NULL,1,'pc(s)',1,'None',1,0),(23,0,'DefaultDescription',1,0,'2019-01-05 13:25:34',NULL,1,'pc(s)',1,'None',1,0),(24,0,'DefaultDescription',1,0,'2019-01-05 13:25:36',NULL,1,'pc(s)',1,'None',1,0),(25,10,'DefaultDescription',1,30,'2019-01-05 13:25:36','USD',1,'pc(s)',1,NULL,1,0),(26,0,'DefaultDescription',1,0,'2019-01-05 13:25:38','USD',1,'pc(s)',1,'None',1,0),(27,0,'DefaultDescription',1,0,'2019-01-05 13:25:45',NULL,1,'pc(s)',1,'None',1,0),(28,0,'DefaultDescription',1,0,'2019-01-05 13:25:48','USD',1,'pc(s)',1,NULL,1,0),(29,0,'DefaultDescription',1,0,'2019-04-19 16:35:08',NULL,0,'pc(s)',NULL,NULL,1,0),(30,0,'DefaultDescription',1,0,'2019-04-19 16:37:12',NULL,0,'pc(s)',NULL,NULL,1,0),(31,0,'DefaultDescription',1,0,'2019-04-19 16:38:37',NULL,0,'pc(s)',NULL,NULL,1,0),(32,0,'DefaultDescription',1,0,'2019-04-19 16:49:53',NULL,1,'pc(s)',1,NULL,1,0),(33,1,'Szlukabit MousePad',1,0,'2019-06-05 18:48:05','USD',0,'pc(s)',1,'Szlukabit MousePad supplier description',0,0),(34,0,'DefaultDescription',1,0,'2019-06-05 20:51:09',NULL,1,'pc(s)',1,NULL,1,0),(35,0,'DefaultDescription',1,0,'2019-06-05 20:51:15',NULL,1,'pc(s)',1,NULL,1,0),(36,0,'DefaultDescription',1,0,'2019-06-05 20:51:54',NULL,1,'pc(s)',1,NULL,1,0),(37,0,'DefaultDescription',1,0,'2019-06-06 08:50:17',NULL,1,'pc(s)',1,NULL,1,0),(38,0,'DefaultDescription',1,0,'2019-06-06 08:51:44',NULL,1,'pc(s)',1,NULL,1,0),(39,0,'DefaultDescription',1,0,'2019-06-06 08:53:32',NULL,1,'pc(s)',1,NULL,1,0),(40,0,'DefaultDescription',1,0,'2019-06-06 08:54:08',NULL,1,'pc(s)',1,NULL,1,0),(41,0,'DefaultDescription',1,0,'2019-06-06 08:54:45',NULL,1,'pc(s)',1,NULL,1,0),(42,0,'DefaultDescription',1,0,'2019-06-06 09:03:12',NULL,1,'pc(s)',1,NULL,1,1),(43,0,'DefaultDescription',1,0,'2019-06-06 09:05:59',NULL,1,'pc(s)',1,NULL,0,1),(44,0,'DefaultDescription',1,0,'2019-06-06 09:08:52',NULL,1,'pc(s)',1,NULL,0,0),(45,0,'DefaultDescription',1,0,'2019-06-06 09:09:08',NULL,1,'pc(s)',1,NULL,0,1),(46,0,'DefaultDescription',1,0,'2019-06-06 09:09:45',NULL,1,'pc(s)',1,NULL,0,1),(47,0,'DefaultDescription',1,0,'2019-06-06 09:11:07',NULL,1,'pc(s)',1,NULL,1,0),(48,0,'DefaultDescription',1,0,'2019-06-06 09:11:20',NULL,1,'pc(s)',1,NULL,0,0),(49,0,'DefaultDescription',1,0,'2019-06-06 09:11:28',NULL,1,'pc(s)',1,NULL,0,1),(50,1,'Gofri',1,90,'2019-08-11 20:09:42','USD',0,'pc(s)',6,'Supplier Gofri',0,0),(51,1,'Gipsy lecsó',1,20,'2019-08-11 20:10:58','USD',0,'pc(s)',11,'Supplier Gipsy lecsó',0,0);
/*!40000 ALTER TABLE `quotation_tblproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotation_tblsettings`
--

DROP TABLE IF EXISTS `quotation_tblsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quotation_tblsettings` (
  `settingid_tblsettings` int(11) NOT NULL AUTO_INCREMENT,
  `settingname_tblsettings` varchar(45) DEFAULT NULL,
  `settingvalue_tblsettings` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`settingid_tblsettings`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblsettings`
--

LOCK TABLES `quotation_tblsettings` WRITE;
/*!40000 ALTER TABLE `quotation_tblsettings` DISABLE KEYS */;
INSERT INTO `quotation_tblsettings` VALUES (1,'ipaddressdebugtrue','127.0.0.1'),(2,'ipaddressdebugfalse','13.58.18.245');
/*!40000 ALTER TABLE `quotation_tblsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tempo`
--

DROP TABLE IF EXISTS `tempo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tempo` (
  `contact_id` int(11) NOT NULL AUTO_INCREMENT,
  `lasttt_name` varchar(30) NOT NULL,
  `first_name` varchar(25) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tempo`
--

LOCK TABLES `tempo` WRITE;
/*!40000 ALTER TABLE `tempo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tempo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'szlukamate$default'
--
/*!50003 DROP PROCEDURE IF EXISTS `new_procedure` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_procedure`()
BEGIN
	select 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spaccountsum` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spaccountsum`(IN `accountid` INT(10), IN `balancekind` VARCHAR(3))
    NO SQL
BEGIN

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spcompanyeditcompanyfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spcompanyeditcompanyfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tblcompanies SET ',fieldname,' = "',fieldvalue,'" WHERE Companyid_tblCompanies = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tblcompanies
                        WHERE Companyid_tblCompanies = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;
    

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spcompanyeditcontactfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spcompanyeditcontactfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tblcontacts SET ',fieldname,' = "',fieldvalue,'" WHERE Contactid_tblContacts = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tblcontacts
                        WHERE Contactid_tblContacts = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;
    

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spcustomerinvoicedocdetailsfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spcustomerinvoicedocdetailsfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = "',fieldvalue,'" WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc_details
                        WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spcustomerinvoicedocfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spcustomerinvoicedocfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc SET ',fieldname,' = "',fieldvalue,'" WHERE Docid_tblDoc = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc
                        WHERE Docid_tblDoc = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;


END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spcustomerordertbldocdetailsfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spcustomerordertbldocdetailsfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = "',fieldvalue,'" WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc_details
                        WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;
    

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spcustomerordertbldocfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spcustomerordertbldocfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc SET ',fieldname,' = "',fieldvalue,'" WHERE Docid_tblDoc = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc
                        WHERE Docid_tblDoc = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;
    

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spdeliverynotedocdetailsfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spdeliverynotedocdetailsfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = "',fieldvalue,'" WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc_details
                        WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spdeliverynotedocfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spdeliverynotedocfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc SET ',fieldname,' = "',fieldvalue,'" WHERE Docid_tblDoc = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc
                        WHERE Docid_tblDoc = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;


END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spentryuniversalselections` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spentryuniversalselections`(IN `fieldnameto` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `docid` INT(10))
    NO SQL
BEGIN

	 
SET @SQLText = CONCAT('UPDATE quotation_tbldoc SET ',fieldnameto,' = ',fieldvalue,' WHERE docid_tbldoc = ',docid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
SET @SQLText2 = CONCAT('SELECT  ',fieldnameto,', "-" AS hyphon, `nameHU_tblchartofaccounts` 
						FROM quotation_tbldoc
                        LEFT JOIN quotation_tblchartofaccounts
						ON quotation_tbldoc.debitaccountid_tbldoc=quotation_tblchartofaccounts.accountid_tblchartofaccounts
                        WHERE docid_tbldoc = ',docid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;
	

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sppohandlerfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sppohandlerfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN

IF fieldvalue = '' THEN
 SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = NULL WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
		PREPARE stmt FROM @SQLText;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;

ELSE
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = "',fieldvalue,'" WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
			
		PREPARE stmt FROM @SQLText;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
END IF;    

    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc_details
                        WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sppurchaseordertbldocdetailsfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sppurchaseordertbldocdetailsfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = "',fieldvalue,'" WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc_details
                        WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sppurchaseordertbldocfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sppurchaseordertbldocfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc SET ',fieldname,' = "',fieldvalue,'" WHERE Docid_tblDoc = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc
                        WHERE Docid_tblDoc = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spquotationdocdetailsfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spquotationdocdetailsfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc_details SET ',fieldname,' = "',fieldvalue,'" WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc_details
                        WHERE Doc_detailsid_tblDoc_details = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spquotationdocfieldsupdate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spquotationdocfieldsupdate`(IN `fieldname` VARCHAR(255), IN `fieldvalue` VARCHAR(255), IN `rowid` INT(10))
BEGIN
	SET @SQLText = CONCAT('UPDATE quotation_tbldoc SET ',fieldname,' = "',fieldvalue,'" WHERE Docid_tblDoc = ',rowid,'');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @SQLText2 = CONCAT('SELECT  ',fieldname,' 
						FROM quotation_tbldoc
                        WHERE Docid_tblDoc = ',rowid,'');
    
	PREPARE stmt2 FROM @SQLText2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;


END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spstock` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spstock`()
    NO SQL
BEGIN

	 
SET @SQLText = CONCAT('        SELECT 
        P.customerdescription_tblProduct as customerdescription, 
        DD.Productid_tblDoc_details_id as productid, 
        supplierdescription_tblProduct, 
        contactdocwhereto.inlabel as inlabelid,
        contactdocwhereto.onstockingoingqty as onstockingoing, 
        contactdocwherefrom.onstockoutgoingqty as onstockoutgoing, 
        contactdocwhereto.companyid as stockid, 
        unit_tblproduct, 
        purchase_price_tblproduct, 
        margin_tblproduct, 
        round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice, 
        companyname_tblcompanies as supplier,  
        currencyisocode_tblcurrency_ctblproduct 
        
        FROM quotation_tbldoc_details as DD  -- all deno items

-- ingoing

	   JOIN (SELECT -- in
				companyin.companyid as companyid,
			    sum(DD1.onstockingoingqty) as onstockingoingqty, 
				DD1.productid as productid, 
				DD1.inlabel as inlabel
				
				
				FROM quotation_tbldoc as D3  -- contactid lookup

				JOIN (SELECT
									Docid_tblDoc as docid,
                                    lateststocktaking.companyid as companyid,
                                    lateststocktaking.lateststocktaking as lateststocktaking
									

  								    FROM quotation_tbldoc as D4 

									JOIN (SELECT 
													 lateststocktaking_tblcompanies as lateststocktaking, 
													 C.Companyid_tblContacts_id as companyid, 
													 C.Contactid_tblContacts as contactid  

													 FROM quotation_tblcontacts as C 

													 JOIN quotation_tblcompanies as companies
													 ON C.Companyid_tblContacts_id = companies.Companyid_tblCompanies

											   ) as lateststocktaking 
									ON D4.Contactid_tblDoc_id = lateststocktaking.contactid

							) as companyin
                ON D3.wheretodocid_tblDoc = companyin.docid

				JOIN (SELECT -- ingoing qty
						   podocdetailsidforlabel_tbldocdetails as inlabel,
						   Docid_tblDoc_details_id as docid, 
						   sum(Qty_tblDoc_details) as onstockingoingqty, 
						   Productid_tblDoc_details_id as productid 
				
						   FROM quotation_tbldoc_details DD 
						   
							GROUP BY productid, docid, inlabel 
						   ) AS DD1 
				ON D3.Docid_tblDoc = DD1.docid 

				WHERE companyin.companyid in (9,10) and D3.creationtime_tbldoc > companyin.lateststocktaking and obsolete_tbldoc=0

				GROUP BY productid, 
							inlabel,
                            companyin.companyid


			) as contactdocwhereto

	   ON DD.Productid_tblDoc_details_id = contactdocwhereto.productid and DD.podocdetailsidforlabel_tbldocdetails = contactdocwhereto.inlabel

-- outgoing

	   LEFT JOIN (SELECT -- out
--				Docid_tblDoc as docido,
			    sum(DD1o.onstockoutgoingqty) as onstockoutgoingqty, 
--				111 as onstockingoingqty, 
				DD1o.outlabel as outlabel
				
				
				FROM quotation_tbldoc as D3o  -- contactid lookup

				LEFT JOIN (SELECT
									Docid_tblDoc as docido,
                                    lateststocktakingo.companyido as companyido,
                                    lateststocktakingo.lateststocktakingo as lateststocktakingo
									

  								    FROM quotation_tbldoc as D4o 

									LEFT JOIN (SELECT 
													 lateststocktaking_tblcompanies as lateststocktakingo, 
													 Co.Companyid_tblContacts_id as companyido, 
													 Co.Contactid_tblContacts as contactido  

													 FROM quotation_tblcontacts as Co 

													 JOIN quotation_tblcompanies as companieso
													 ON Co.Companyid_tblContacts_id = companieso.Companyid_tblCompanies

											   ) as lateststocktakingo 
									ON D4o.Contactid_tblDoc_id = lateststocktakingo.contactido

							) as companyout
                ON D3o.wherefromdocid_tblDoc = companyout.docido

				JOIN (SELECT -- outgoing qty
						   podocdetailsidforlabel_tbldocdetails as outlabel,
						   Docid_tblDoc_details_id as docid, 
						   sum(Qty_tblDoc_details) as onstockoutgoingqty
				
						   FROM quotation_tbldoc_details DDo 
						   
							GROUP BY docid, outlabel 
						   ) AS DD1o 
				ON D3o.Docid_tblDoc = DD1o.docid 

				WHERE companyout.companyido in (9,10) and D3o.creationtime_tbldoc > companyout.lateststocktakingo and obsolete_tbldoc=0
				GROUP BY outlabel
			) as contactdocwherefrom

	   ON DD.podocdetailsidforlabel_tbldocdetails = contactdocwherefrom.outlabel



        JOIN quotation_tbldoc D 
        ON DD.Docid_tblDoc_details_id = D.Docid_tblDoc 

        JOIN quotation_tblproduct as P 
        ON DD.Productid_tblDoc_details_id = P.Productid_tblProduct 

        JOIN quotation_tblcompanies 
        ON companyid_tblcompanies = suppliercompanyid_tblproduct 

        WHERE obsolete_tbldoc=0 and Doc_kindid_tblDoc_id=8 
        GROUP BY   DD.Productid_tblDoc_details_id,
				   inlabelid,
                   onstockingoing,
                   onstockoutgoing,
                   customerdescription,
                   stockid
');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spstock0` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spstock0`()
    NO SQL
BEGIN

	 
SET @SQLText = CONCAT('        SELECT 
        P.customerdescription_tblProduct as customerdescription, 
        DD.Productid_tblDoc_details_id as productid, 
        supplierdescription_tblProduct, 
        onstockingoing.inlabel as inlabelid,
        onstockingoing.onstockingoingqty as onstockingoing, 
        onstockingoing.onstockoutgoingqty as onstockoutgoing, 
        onstockingoing.incompanyid as incompanyid, 
--        onstockingoing.outcompanyid as outcompanyid, 
        onstockingoing.wheretodocid as wheretodocid, 
--        onstockingoing.wherefromdocid as wherefromdocid, 
--        onstockingoing.outlabel as outlabelid,
        onstockingoing.docid as docid, 
--        DD.Doc_detailsid_tblDoc_details as docdetails,  
--        COALESCE(sum(onstockoutgoing.onstockoutgoingqty),0) as onstockoutgoing, 
--        onstockingoing.docid as docid, 
--        COALESCE(sum(onstockingoing.onstockingoingqty),0)-COALESCE(sum(onstockoutgoing.onstockoutgoingqty),0) as onstock, 
--        DD.Docid_tblDoc_details_id, 
        unit_tblproduct, 
        purchase_price_tblproduct, 
        margin_tblproduct, 
        round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice, 
        companyname_tblcompanies as supplier,  -- 10
        currencyisocode_tblcurrency_ctblproduct 
--        onstockingoing.wheretodocid, 
--        onstockingoing.contactid2 
        
        FROM quotation_tbldoc_details as DD  -- all deno items

-- ingoing
        JOIN (SELECT
                   contactdocwhereto.onstockingoingqty as onstockingoingqty, 
                   contactdocwhereto.productid as inproductid, 
                   contactdocwhereto.inlabel as inlabel,
                   contactdocwhereto.companyid as incompanyid,
                   contactdocwherefrom.onstockoutgoingqty as onstockoutgoingqty, 
--                   contactdocwherefrom.productid as outproductid, 
--                   contactdocwherefrom.outlabel as outlabel,
--                   contactdocwherefrom.companyid as outcompanyid,
                   D2.Docid_tblDoc as docid,
                   D2.wheretodocid_tbldoc as wheretodocid,
                   D2.wherefromdocid_tbldoc as wherefromdocid
					
                   FROM quotation_tbldoc D2 -- denos by products

				   JOIN (SELECT -- in
							Docid_tblDoc as docid,
							lateststocktaking.companyid as companyid,
						   -- DD1.onstockingoingqty as onstockingoingqty, 
						    111 as onstockingoingqty, 
						    DD1.productid as productid, 
						    DD1.inlabel as inlabel,
							wheretodocid_tblDoc as wheretodocid
                            
                            
							FROM quotation_tbldoc as D3  -- contactid lookup

							LEFT JOIN (SELECT 
											 lateststocktaking_tblcompanies as lateststocktaking, 
											 C.Companyid_tblContacts_id as companyid, 
											 C.Contactid_tblContacts as contactid  

											 FROM quotation_tblcontacts as C 

											 JOIN quotation_tblcompanies as companies
											 ON C.Companyid_tblContacts_id = companies.Companyid_tblCompanies

									   ) as lateststocktaking 
							ON D3.Contactid_tblDoc_id = lateststocktaking.contactid

						    JOIN (SELECT -- ingoing qty
									   podocdetailsidforlabel_tbldocdetails as inlabel,
									   Docid_tblDoc_details_id as docid, 
									   sum(Qty_tblDoc_details) as onstockingoingqty, 
									   Productid_tblDoc_details_id as productid 
							
									   FROM quotation_tbldoc_details DD 
									   
										GROUP BY productid, docid, inlabel 
									   ) AS DD1 
						    ON D3.Docid_tblDoc = DD1.docid 

                            
                            WHERE lateststocktaking.companyid in (9,10) and D3.creationtime_tbldoc > lateststocktaking.lateststocktaking

						) as contactdocwhereto

				   ON (D2.wheretodocid_tblDoc = contactdocwhereto.wheretodocid and DD.Productid_tblDoc_details_id = contactdocwhereto.productid)

				   LEFT JOIN (SELECT -- out
							Docid_tblDoc as docid,
							lateststocktakingout.companyid as companyid,
						   -- DD1out.onstockoutgoingqty as onstockoutgoingqty, 
						    222 as onstockoutgoingqty, 
						    DD1out.productid as productid, 
						    DD1out.outlabel as outlabel,
							wherefromdocid_tblDoc as wherefromdocid
                            
                            
							FROM quotation_tbldoc as Do3  -- contactid lookup

							JOIN (SELECT 
											 lateststocktaking_tblcompanies as lateststocktaking, 
											 Cout.Companyid_tblContacts_id as companyid, 
											 Cout.Contactid_tblContacts as contactid  

											 FROM quotation_tblcontacts as Cout 

											 JOIN quotation_tblcompanies as companies
											 ON Cout.Companyid_tblContacts_id = companies.Companyid_tblCompanies

									   ) as lateststocktakingout
							ON Do3.Contactid_tblDoc_id = lateststocktakingout.contactid

						    JOIN (SELECT -- outgoing qty
									   podocdetailsidforlabel_tbldocdetails as outlabel,
									   Docid_tblDoc_details_id as docid, 
									   sum(Qty_tblDoc_details) as onstockoutgoingqty, 
									   Productid_tblDoc_details_id as productid 
							
									   FROM quotation_tbldoc_details DD 
									   
										GROUP BY productid, docid, outlabel 
									   ) AS DD1out 
						    ON Do3.Docid_tblDoc = DD1out.docid 

                            
--                            WHERE lateststocktakingout.companyid in (9,10) and Do3.creationtime_tbldoc > lateststocktakingout.lateststocktaking

						) as contactdocwherefrom


				   ON D2.wherefromdocid_tblDoc = contactdocwherefrom.wherefromdocid 


                   WHERE D2.obsolete_tbldoc = 0  and D2.denoenabledflag_tbldoc=1  

                   ) AS onstockingoing 
        ON (DD.Docid_tblDoc_details_id = onstockingoing.docid and DD.Productid_tblDoc_details_id = onstockingoing.inproductid)


        LEFT JOIN quotation_tbldoc D 
        ON DD.Docid_tblDoc_details_id = D.Docid_tblDoc 

        LEFT JOIN quotation_tblproduct as P 
        ON DD.Productid_tblDoc_details_id = P.Productid_tblProduct 

        JOIN quotation_tblcompanies 
        ON companyid_tblcompanies = suppliercompanyid_tblproduct 

        WHERE obsolete_tbldoc=0 and Doc_kindid_tblDoc_id=8 
        GROUP BY   DD.Productid_tblDoc_details_id,
				   inlabelid,
                   onstockingoing,
                   onstockoutgoing,
                   customerdescription,
                   incompanyid,
                   wheretodocid,
                   docid
--                   outlabelid,
--                   onstockoutgoing,
--                   outcompanyid,
--                   wherefromdocid
');
    
    PREPARE stmt FROM @SQLText;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-12 22:45:18