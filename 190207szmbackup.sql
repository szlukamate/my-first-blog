-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: szlukamate$default
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.16.04.2

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
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$1CI2zMgGEmBC$EZSMhvGjTetCWK5AftJBM0GIVhE/sNi/nfKxkQDNhNY=','2019-02-05 17:48:27.162001',1,'szlukamate','Mate','Szluka','szluka.mate@gmail.com',1,1,'2018-11-02 21:48:04.683828','Sales Engineer\r\n+36309680-469\r\nszluka.mate@gmail.com'),(3,'pbkdf2_sha256$36000$fBK7P9yKbYST$NxLXdiX7FNisBZyf3F6VphHV2hnixqKT7SoGeqlwtnI=','2019-02-05 17:30:33.598559',0,'gipszjakab','Jakab','Gipsz','q@q.hu',1,1,'2019-02-05 17:21:58.000000',NULL);
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
INSERT INTO `django_session` VALUES ('270o7sys9h2608m6uym1jtaqsgu5slez','YjE4MmZjYzA4ZTJkN2ZlMjQyYWEwNDhkNjc3OTFiZDVjZWI5MzA0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-11-17 12:33:57.987435'),('aq9yqx0zgoaf1txrrpktkaghsveueciq','YjE4MmZjYzA4ZTJkN2ZlMjQyYWEwNDhkNjc3OTFiZDVjZWI5MzA0Zjp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-12-01 12:42:49.904647'),('aye1bk06uoe3issurmwgc6z7afirjm3m','NDJjNDhiMzk1MmY2ZTJmMGNmNmUwODA3MjE5NjA5ZDk4MDNmNjUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2019-01-19 16:38:03.310882'),('b0cvvyukxgplka6c5qrgb2nwj01ifl7t','NDJjNDhiMzk1MmY2ZTJmMGNmNmUwODA3MjE5NjA5ZDk4MDNmNjUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiOTEzYzA5MDQ2NDc4MTQyMTk1NzU5YmU1NTc5N2NkMWViMDgwOGMxIn0=','2018-11-16 21:49:22.608693'),('rwn2epelhgtgjtcj2sf101aso4c3u9zk','OThiMWE3ZDA2YTIzMzQ4MjQ4YmNkOGY1YjVmOWFjNGMyMzZmMmY4Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYjkxM2MwOTA0NjQ3ODE0MjE5NTc1OWJlNTU3OTdjZDFlYjA4MDhjMSIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-02-19 17:48:27.184811'),('wjx5sx3zxtyrg3pei8b8m4u219ohltgb','MGQzZTIwNTRkNTY3NjhkZmEwNGM1OTc1NTE4MTRjOTMwZmYwMzIyYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MTNjMDkwNDY0NzgxNDIxOTU3NTliZTU1Nzk3Y2QxZWIwODA4YzEiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-12-18 12:33:53.181723');
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
  PRIMARY KEY (`backpageidforquotation_tblbackpageforquotation`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblbackpageforquotation`
--

LOCK TABLES `quotation_tblbackpageforquotation` WRITE;
/*!40000 ALTER TABLE `quotation_tblbackpageforquotation` DISABLE KEYS */;
INSERT INTO `quotation_tblbackpageforquotation` VALUES (2,'Backpage text1','backpage standard'),(3,'Backpage text2','Backpage non standard');
/*!40000 ALTER TABLE `quotation_tblbackpageforquotation` ENABLE KEYS */;
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
  PRIMARY KEY (`Companyid_tblCompanies`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblcompanies`
--

LOCK TABLES `quotation_tblcompanies` WRITE;
/*!40000 ALTER TABLE `quotation_tblcompanies` DISABLE KEYS */;
INSERT INTO `quotation_tblcompanies` VALUES (1,'Apple Inc.',3,2,'6726','Szeged','Akácfa u. 16.'),(2,'General Mills',2,2,NULL,'Nebraska',NULL),(6,'Company3',2,2,NULL,NULL,NULL),(7,'DefaultCompany',2,2,NULL,NULL,NULL);
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
  `firstname_tblcontacts` varchar(200) NOT NULL,
  `lastname_tblcontacts` varchar(200) NOT NULL,
  `Companyid_tblContacts_id` int(11) NOT NULL,
  `title_tblcontacts` varchar(10) DEFAULT NULL,
  `mobile_tblcontacts` varchar(40) DEFAULT NULL,
  `email_tblcontacts` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Contactid_tblContacts`),
  KEY `quotation_tblcontact_Companyid_tblContact_26be7ab6_fk_quotation` (`Companyid_tblContacts_id`),
  CONSTRAINT `quotation_tblcontact_Companyid_tblContact_26be7ab6_fk_quotation` FOREIGN KEY (`Companyid_tblContacts_id`) REFERENCES `quotation_tblcompanies` (`Companyid_tblCompanies`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblcontacts`
--

LOCK TABLES `quotation_tblcontacts` WRITE;
/*!40000 ALTER TABLE `quotation_tblcontacts` DISABLE KEYS */;
INSERT INTO `quotation_tblcontacts` VALUES (1,'Firstname3','Lastname3',6,NULL,NULL,NULL),(2,'firstname2','lastname2',2,NULL,NULL,NULL),(3,'firstname2','lastname2',2,NULL,NULL,NULL),(4,'Steve','Jobs',1,'Mr.','+36301111111','j@v.com');
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
  PRIMARY KEY (`currencyid_tblcurrency`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblcurrency`
--

LOCK TABLES `quotation_tblcurrency` WRITE;
/*!40000 ALTER TABLE `quotation_tblcurrency` DISABLE KEYS */;
INSERT INTO `quotation_tblcurrency` VALUES (1,'HUF','Hungarian Forint'),(2,'USD','United States Dollar'),(3,'EUR','European Union Currency');
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
  `Contactid_tblDoc_id` int(11) NOT NULL,
  `companyname_tblcompanies_ctbldoc` varchar(200) DEFAULT NULL,
  `firstname_tblcontacts_ctbldoc` varchar(200) DEFAULT NULL,
  `lastname_tblcontacts_ctbldoc` varchar(200) DEFAULT NULL,
  `creationtime_tbldoc` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `prefacetextforquotation_tblprefaceforquotation_ctbldoc` text,
  `obsolete_tbldoc` int(11) NOT NULL DEFAULT '0',
  `backpagetextforquotation_tblbackpageforquotation_ctbldoc` text,
  `prefacespecforquotation_tbldoc` text,
  `subject_tbldoc` varchar(255) DEFAULT NULL,
  `docnumber_tbldoc` int(10) DEFAULT NULL,
  `creatorid_tbldoc` int(10) DEFAULT NULL,
  `title_tblcontacts_ctbldoc` varchar(20) DEFAULT NULL,
  `mobile_tblcontacts_ctbldoc` varchar(50) DEFAULT NULL,
  `email_tblcontacts_ctbldoc` varchar(50) DEFAULT NULL,
  `pcd_tblcompanies_ctbldoc` varchar(20) DEFAULT NULL,
  `town_tblcompanies_ctbldoc` varchar(55) DEFAULT NULL,
  `address_tblcompanies_ctbldoc` text,
  `total_tbldoc` varchar(10) NOT NULL DEFAULT 'Total_off',
  PRIMARY KEY (`Docid_tblDoc`),
  KEY `quotation_tbldoc_Doc_kindid_tblDoc_id_844f8ed6_fk_quotation` (`Doc_kindid_tblDoc_id`),
  KEY `quotation_tbldoc_Contactid_tblDoc_id_0de2ee97_fk_quotation` (`Contactid_tblDoc_id`),
  CONSTRAINT `quotation_tbldoc_Contactid_tblDoc_id_0de2ee97_fk_quotation` FOREIGN KEY (`Contactid_tblDoc_id`) REFERENCES `quotation_tblcontacts` (`Contactid_tblContacts`),
  CONSTRAINT `quotation_tbldoc_Doc_kindid_tblDoc_id_844f8ed6_fk_quotation` FOREIGN KEY (`Doc_kindid_tblDoc_id`) REFERENCES `quotation_tbldoc_kind` (`Doc_kindid_tblDoc_kind`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tbldoc`
--

LOCK TABLES `quotation_tbldoc` WRITE;
/*!40000 ALTER TABLE `quotation_tbldoc` DISABLE KEYS */;
INSERT INTO `quotation_tbldoc` VALUES (1,'6726','Szeged',1,4,'Apple Inc.','Steve','Jobs','2018-12-12 16:47:30','				gf456\n',0,'na','prefacespecs\n\nkk\n\n\n\njjj\n\n\n\n\n\nhh\n\n\n\n\n\n\n\n\n\n\nff\n','na665',77,NULL,'Mr.','+36301111111','j@v.com','6726','Szeged','Akácfa u. 16.','0'),(2,'7777','Pécs',1,3,'Company2','firstname2','lastname2','2018-12-12 16:47:30','',0,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(3,'9999','Győr',1,4,'Company1','Firstname1','Lastname1','2018-12-12 16:47:30','',0,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(4,'5555','Békéscsaba',2,1,NULL,NULL,NULL,'2018-12-12 16:47:30','',0,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(5,'4444','Nyíregyháza',3,1,NULL,NULL,NULL,'2018-12-12 16:47:30','',1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(6,'3333','Eger',3,1,NULL,NULL,NULL,'2018-12-12 16:47:30','',1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(9,NULL,NULL,1,2,NULL,NULL,NULL,'2018-12-12 16:47:30','',1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(10,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-29 12:34:46',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(11,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-29 12:36:44',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(12,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-29 12:37:37',NULL,0,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(13,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-29 13:20:57',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(14,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-29 13:23:12',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(15,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-29 13:25:31',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(16,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-01-29 13:42:01',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(17,NULL,NULL,1,4,NULL,NULL,NULL,'2019-01-30 13:40:33',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(18,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-01-30 13:41:16',NULL,1,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(19,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-01-30 16:40:04','Thank you for your inquery.',1,'Backpage text1','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(20,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-01-30 16:44:03','Thank you for your inquery.',1,'Backpage text1','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(21,NULL,NULL,1,2,'General Mills','firstname2','lastname2','2019-01-30 16:47:39','Thank you for your inquery.',1,'Backpage text1','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(22,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-01-30 17:29:39','Thank you for your inquery.',1,'Backpage text1','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(23,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-01-30 17:30:03','Thank you for your inquery.',0,'Backpage text1','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(24,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-03 20:38:44','								t\r\n								',1,'Backpage text2','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(25,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 11:43:07','New1text',1,'Backpage text2','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(26,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 11:45:20','New1text',1,'Backpage text2','',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(27,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 15:17:16','New1text',1,'Backpage text2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(28,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 15:22:22','New1text',1,'Backpage text2','Backpage text23',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(29,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 15:32:56','New1text',1,'Backpage text2','t','s',NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(30,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 15:39:28','Thank you for your inquery.\r\n\r\nWe wait your feedback or any question connection to quotation.\r\n\r\n\r\n\r\n',1,'Backpage text2','Given data:\n\nHP 6200\nCisco 6521','Technical and cost quotation',NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(31,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-04 16:39:59','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2','33333333333\n\n\n34\n\n222222222222222','Cisco programming',NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(32,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 10:03:05','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,78,NULL,NULL,NULL,NULL,'',NULL,NULL,'0'),(33,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 15:43:30','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,1,79,NULL,NULL,NULL,'',NULL,NULL,'0'),(34,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 15:44:11','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,1,79,NULL,NULL,NULL,'',NULL,NULL,'0'),(35,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 15:46:28','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,1,79,NULL,NULL,NULL,'',NULL,NULL,'0'),(36,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 15:50:03','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,79,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(37,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:25:25','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,80,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(38,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:27:11','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,81,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(39,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:27:47','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,82,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(40,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:29:04','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,83,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(41,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:31:08','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,84,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(42,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:31:52','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,85,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(43,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:37:19','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,86,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(44,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:41:59','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,87,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(45,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 16:48:43','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,88,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(46,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 17:25:10','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,89,3,NULL,NULL,NULL,'',NULL,NULL,'0'),(47,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-05 17:49:21','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',1,'Backpage text2',NULL,NULL,90,1,NULL,NULL,NULL,'',NULL,NULL,'0'),(48,NULL,NULL,1,4,'Apple Inc.','Steve','Jobs','2019-02-06 09:30:17','Thank you for your inquery.\r\nAs you requested we send our quotation for your kind information.\r\nWe wait your feedback or any question connection to quotation.\r\nWe hope you will be satisfied our service and we can serve your need in the future again.\r\n\r\nYou can see our reference projects on site www.example.com in point refererence (here is the link).\r\n\r\nIn the order please reference to our quotation number. ({{ link }}\r\n\r\n\r\n\r\n\r\n',0,'Backpage text2','Noness',NULL,91,1,'Mr.','+36301111111','j@v.com','6726','Szeged','Akácfa u. 16.','Total_On');
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
  `Qty_tblDoc_details` int(11) NOT NULL DEFAULT '1',
  `Docid_tblDoc_details_id` int(11) NOT NULL,
  `Productid_tblDoc_details_id` int(11) DEFAULT NULL,
  `firstnum_tblDoc_details` int(11) NOT NULL DEFAULT '1',
  `fourthnum_tblDoc_details` int(11) NOT NULL DEFAULT '0',
  `secondnum_tblDoc_details` int(11) NOT NULL DEFAULT '0',
  `thirdnum_tblDoc_details` int(11) NOT NULL DEFAULT '0',
  `Note_tblDoc_details` varchar(200) DEFAULT NULL,
  `creationtime_tblDoc_details` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `purchase_price_tblproduct_ctblDoc_details` float DEFAULT NULL,
  `salesprice_tblDoc_details` float DEFAULT NULL,
  `Product_description_tblProduct_ctblDoc_details` varchar(200) DEFAULT NULL,
  `currencyisocode_tblcurrency_ctblproduct_ctblDoc_details` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Doc_detailsid_tblDoc_details`),
  KEY `quotation_tbldoc_det_Docid_tblDoc_details_118ffe05_fk_quotation` (`Docid_tblDoc_details_id`),
  CONSTRAINT `quotation_tbldoc_det_Docid_tblDoc_details_118ffe05_fk_quotation` FOREIGN KEY (`Docid_tblDoc_details_id`) REFERENCES `quotation_tbldoc` (`Docid_tblDoc`),
  CONSTRAINT `quotation_tbldoc_details_ibfk_1` FOREIGN KEY (`Docid_tblDoc_details_id`) REFERENCES `quotation_tbldoc` (`Docid_tblDoc`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tbldoc_details`
--

LOCK TABLES `quotation_tbldoc_details` WRITE;
/*!40000 ALTER TABLE `quotation_tbldoc_details` DISABLE KEYS */;
INSERT INTO `quotation_tbldoc_details` VALUES (4,6,2,2,4,0,0,0,'Defaultnote6','2019-01-24 14:20:33.282563',0,0,'',''),(5,1,3,3,18,0,0,0,'Defaultnote18','2018-11-21 05:52:25.443132',0,0,'',''),(28,1,2,1,33,0,1,0,'Defaultnote','2019-01-24 14:20:07.883695',0,0,'s',''),(29,1,3,1,2,0,0,0,'Defaultnote','2018-12-01 11:53:40.073139',0,0,'',''),(32,1,4,1,1,0,0,0,'Defaultnote','2018-11-21 05:52:25.443132',0,0,'',''),(33,1,5,1,2,0,2,0,'Defaultnote2','2018-11-21 05:52:25.443132',0,0,'',''),(48,1,2,1,33345678,0,2,0,'Defaultnote','2019-01-24 14:20:11.834025',0,0,'d',''),(53,1,9,1,1,0,0,0,'Defaultnote','2018-12-01 20:24:40.488388',0,0,'',''),(74,1,9,2,2,44,22,33,'Defaultnote','2018-12-23 19:40:34.300098',2553,15,'Something','HUF'),(81,111,1,5,129,2,333,2,'','2019-02-04 13:18:56.482106',9,18,'Pr666','USD'),(82,1,1,3,130,1,231,0,'Defaultnote','2019-02-07 20:30:37.755743',35,2,'Prgggggggggggggggggggggggggggggggggggggggggggggggggg gggggggggggggggggggggggggggggggggggggggggggggg ggggggggggggggggggggg','HUF'),(83,1,1,6,131,1,0,1,'Defaultnote','2019-01-23 14:46:57.881933',7,0,'Pr7bbb bbbbbbbbnnnnnnnnnnnnnnnnnnnn hhhhhh hhhhhhhhhhhhhhhhhhhhhhhhh kkkkkkkkkkkkkk','USD'),(87,1,1,3,135,0,0,0,'Defaultnote','2019-01-05 14:37:42.945382',35,36,'Pr','HUF'),(90,1,1,28,136,0,0,0,'Defaultnote','2019-01-06 19:59:35.280443',0,0,'DefaultDescription','USD'),(91,1,1,1,137,0,0,0,'Defaultnote','2019-01-23 16:51:03.485918',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(92,1,1,1,138,0,0,0,'Defaultnote','2019-01-23 16:51:32.516952',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(93,1,1,1,139,0,0,0,'Defaultnote','2019-01-23 16:51:38.898735',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(94,1,1,1,140,0,0,0,'Defaultnote','2019-01-23 16:51:46.447991',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(95,1,1,5,141,0,0,0,'Defaultnote','2019-01-23 16:51:52.919107',9,18,'Pr6','USD'),(96,1,1,1,142,0,0,0,'Defaultnote','2019-01-23 16:51:59.802886',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(98,1,1,1,143,0,0,0,'Defaultnote','2019-01-24 13:10:32.562633',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(99,1,1,1,144,0,0,0,'Defaultnote','2019-01-24 13:50:07.914701',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(100,1,1,1,145,0,0,0,'Defaultnote','2019-01-24 13:51:10.790589',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(101,1,1,1,146,0,0,0,'Defaultnote','2019-01-24 13:51:18.375114',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(102,1,1,1,147,0,0,0,'Defaultnote','2019-01-24 14:08:26.315982',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(103,1,1,5,148,0,0,0,'Defaultnote','2019-01-24 14:09:33.798240',9,18,'Pr6','USD'),(104,1,1,1,149,0,0,0,'Defaultnote','2019-01-26 13:39:04.343656',55,101,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(106,1,16,1,1,0,0,0,NULL,'2019-01-29 13:42:42.874127',6,36,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(107,1,17,NULL,1,0,0,0,NULL,'2019-01-30 13:40:34.048789',NULL,NULL,NULL,NULL),(108,1,18,NULL,1,0,0,0,NULL,'2019-01-30 13:41:16.323672',NULL,NULL,NULL,NULL),(109,1,1,1,150,0,0,0,'Defaultnote','2019-01-30 14:28:46.966998',6,36,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr','USD'),(110,1,19,NULL,1,0,0,0,NULL,'2019-01-30 16:40:04.400883',NULL,NULL,NULL,NULL),(111,1,20,NULL,1,0,0,0,NULL,'2019-01-30 16:44:03.425341',NULL,NULL,NULL,NULL),(112,1,21,NULL,1,0,0,0,NULL,'2019-01-30 16:47:39.537258',NULL,NULL,NULL,NULL),(113,1,22,NULL,1,0,0,0,NULL,'2019-01-30 17:29:39.483899',NULL,NULL,NULL,NULL),(114,1,23,NULL,1,0,0,0,NULL,'2019-01-30 17:30:03.997293',NULL,NULL,NULL,NULL),(115,1,24,NULL,1,0,0,0,NULL,'2019-02-03 20:38:44.563799',NULL,NULL,NULL,NULL),(116,1,25,NULL,1,0,0,0,NULL,'2019-02-04 11:43:07.955435',NULL,NULL,NULL,NULL),(117,1,26,NULL,1,0,0,0,NULL,'2019-02-04 11:45:20.132369',NULL,NULL,NULL,NULL),(118,1,27,NULL,1,0,0,0,NULL,'2019-02-04 15:17:16.605155',NULL,NULL,NULL,NULL),(119,1,28,NULL,1,0,0,0,NULL,'2019-02-04 15:22:22.158048',NULL,NULL,NULL,NULL),(120,1,29,NULL,1,0,0,0,NULL,'2019-02-04 15:32:56.537200',NULL,NULL,NULL,NULL),(121,1,30,NULL,1,0,0,0,NULL,'2019-02-04 15:39:28.656762',NULL,NULL,NULL,NULL),(122,1,31,NULL,1,0,0,0,NULL,'2019-02-04 16:39:59.452817',NULL,NULL,NULL,NULL),(123,1,32,NULL,1,0,0,0,NULL,'2019-02-05 10:03:05.158122',NULL,NULL,NULL,NULL),(124,1,33,NULL,1,0,0,0,NULL,'2019-02-05 15:43:30.979642',NULL,NULL,NULL,NULL),(125,1,34,NULL,1,0,0,0,NULL,'2019-02-05 15:44:11.841624',NULL,NULL,NULL,NULL),(126,1,35,NULL,1,0,0,0,NULL,'2019-02-05 15:46:28.874090',NULL,NULL,NULL,NULL),(127,1,36,NULL,1,0,0,0,NULL,'2019-02-05 15:50:03.891791',NULL,NULL,NULL,NULL),(128,1,37,NULL,1,0,0,0,NULL,'2019-02-05 16:25:25.327099',NULL,NULL,NULL,NULL),(129,1,38,NULL,1,0,0,0,NULL,'2019-02-05 16:27:11.361033',NULL,NULL,NULL,NULL),(130,1,39,NULL,1,0,0,0,NULL,'2019-02-05 16:27:47.406182',NULL,NULL,NULL,NULL),(131,1,40,NULL,1,0,0,0,NULL,'2019-02-05 16:29:04.474286',NULL,NULL,NULL,NULL),(132,1,41,NULL,1,0,0,0,NULL,'2019-02-05 16:31:08.613606',NULL,NULL,NULL,NULL),(133,1,42,NULL,1,0,0,0,NULL,'2019-02-05 16:31:52.220488',NULL,NULL,NULL,NULL),(134,1,43,NULL,1,0,0,0,NULL,'2019-02-05 16:37:19.440039',NULL,NULL,NULL,NULL),(135,1,44,NULL,1,0,0,0,NULL,'2019-02-05 16:41:59.397349',NULL,NULL,NULL,NULL),(136,1,45,NULL,1,0,0,0,NULL,'2019-02-05 16:48:43.300668',NULL,NULL,NULL,NULL),(137,1,46,NULL,1,0,0,0,NULL,'2019-02-05 17:25:10.119037',NULL,NULL,NULL,NULL),(138,1,47,NULL,1,0,0,0,NULL,'2019-02-05 17:49:21.692032',NULL,NULL,NULL,NULL),(139,1,48,NULL,1,0,0,0,NULL,'2019-02-06 09:30:17.565528',NULL,NULL,NULL,NULL);
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
  PRIMARY KEY (`Doc_kindid_tblDoc_kind`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tbldoc_kind`
--

LOCK TABLES `quotation_tbldoc_kind` WRITE;
/*!40000 ALTER TABLE `quotation_tbldoc_kind` DISABLE KEYS */;
INSERT INTO `quotation_tbldoc_kind` VALUES (1,'Quotation'),(2,'Order'),(3,'Invoice');
/*!40000 ALTER TABLE `quotation_tbldoc_kind` ENABLE KEYS */;
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
  `Product_description_tblProduct` varchar(200) NOT NULL,
  `currencyid_tblcurrency_fktblproduct` int(11) NOT NULL DEFAULT '1',
  `margin_tblproduct` float NOT NULL DEFAULT '0',
  `creationtime_tblproduct` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `currencyisocode_tblcurrency_ctblproduct` varchar(10) DEFAULT NULL,
  `obsolete_tblproduct` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Productid_tblProduct`),
  KEY `currencyid_tblcurrency_fktblproduct` (`currencyid_tblcurrency_fktblproduct`),
  CONSTRAINT `currencyid_tblcurrency_with_currencyid_tblproducts_fktblproduct` FOREIGN KEY (`currencyid_tblcurrency_fktblproduct`) REFERENCES `quotation_tblcurrency` (`currencyid_tblcurrency`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotation_tblproduct`
--

LOCK TABLES `quotation_tblproduct` WRITE;
/*!40000 ALTER TABLE `quotation_tblproduct` DISABLE KEYS */;
INSERT INTO `quotation_tblproduct` VALUES (1,6,'Somethinffgggggggg  ggggggggggggggg ggg gggggggg  ggggggggggggt tttttttttttt ttttttttt ttttttttttttttt ttttttttttttttttttt tttttttttttttttttt tttttttttttttttttttttrrr rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrr',1,83.3333,'2018-12-17 09:54:39','HUF',0),(2,2553,'Something',2,15,'2018-12-17 09:54:39','HUF',1),(4,80,'Pr5e',3,22,'2018-12-17 09:54:39','HUF',1),(5,9,'Pr66',2,50,'2018-12-17 09:54:39','USD',0),(6,7,'Pr7',2,10,'2018-12-17 09:54:39','USD',0),(7,0,'DefaultDescription',1,0,'2019-01-05 13:24:50','USD',0),(8,0,'DefaultDescription',1,0,'2019-01-05 13:25:16',NULL,0),(9,0,'DefaultDescription',1,0,'2019-01-05 13:25:17',NULL,0),(10,0,'DefaultDescription',1,0,'2019-01-05 13:25:18',NULL,0),(11,0,'DefaultDescription',1,0,'2019-01-05 13:25:20',NULL,0),(12,0,'DefaultDescription',1,0,'2019-01-05 13:25:21',NULL,0),(13,0,'DefaultDescription',1,0,'2019-01-05 13:25:21',NULL,0),(14,0,'DefaultDescription',1,0,'2019-01-05 13:25:23',NULL,0),(15,0,'DefaultDescription',1,0,'2019-01-05 13:25:26',NULL,0),(16,0,'DefaultDescription',1,0,'2019-01-05 13:25:27',NULL,0),(17,0,'DefaultDescription',1,0,'2019-01-05 13:25:28',NULL,0),(18,0,'DefaultDescription',1,0,'2019-01-05 13:25:29',NULL,0),(19,0,'DefaultDescription',1,0,'2019-01-05 13:25:30',NULL,0),(20,0,'DefaultDescription',1,0,'2019-01-05 13:25:32',NULL,0),(21,0,'DefaultDescription',1,0,'2019-01-05 13:25:33',NULL,0),(22,0,'DefaultDescription',1,0,'2019-01-05 13:25:33',NULL,0),(23,0,'DefaultDescription',1,0,'2019-01-05 13:25:34',NULL,0),(24,0,'DefaultDescription',1,0,'2019-01-05 13:25:36',NULL,0),(25,10,'DefaultDescription',1,30,'2019-01-05 13:25:36','USD',0),(26,0,'DefaultDescription',1,0,'2019-01-05 13:25:38','USD',0),(27,0,'DefaultDescription',1,0,'2019-01-05 13:25:45',NULL,0),(28,0,'DefaultDescription',1,0,'2019-01-05 13:25:48','USD',0);
/*!40000 ALTER TABLE `quotation_tblproduct` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-07 21:33:19
