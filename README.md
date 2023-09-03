# file_sharing
It is essentially file sharing between two user types: operational_user and client_user.


Here are the DDLs for the two tables used in this project:
Data base name : file_sharing

Table 1 ----> auth_user

CREATE TABLE `auth_user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(75) NOT NULL,
  `password` varchar(75) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `x_api_key` varchar(150) NOT NULL,
  `access_token` varchar(1000) DEFAULT NULL,
  `user_type` varchar(45) NOT NULL,
  `verify_code` varchar(45) NOT NULL DEFAULT '0',
  `is_verified` varchar(45) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`email`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

Table 2 ----> file_sharing
CREATE TABLE `file_sharing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(100) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `uploaded_at` datetime NOT NULL,
  `file_extension` varchar(45) NOT NULL,
  `secret_code` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
