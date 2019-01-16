/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost
 Source Database       : business

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : utf-8

 Date: 01/16/2019 13:04:02 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `business_keyword`
-- ----------------------------
DROP TABLE IF EXISTS `business_keyword`;
CREATE TABLE `business_keyword` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `des` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Records of `business_keyword`
-- ----------------------------
BEGIN;
INSERT INTO `business_keyword` VALUES ('1', 'systemName', '社会猪', '系统名称'), ('2', 'cataLogIcon', '/static/image/folder.png,/static/image/file.png,/static/image/image.png', '文件icon');
COMMIT;

-- ----------------------------
--  Table structure for `business_resource`
-- ----------------------------
DROP TABLE IF EXISTS `business_resource`;
CREATE TABLE `business_resource` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `parent` int(11) DEFAULT NULL,
  `delete_flag` int(255) DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Records of `business_resource`
-- ----------------------------
BEGIN;
INSERT INTO `business_resource` VALUES ('1', '系统管理', null, '-1', '0', '2019-01-09 14:07:07', '2019-01-09 14:07:11'), ('2', '角色列表', '/business/roleManage', '1', '0', '2019-01-09 14:08:35', '2019-01-09 14:08:37'), ('3', '用户列表', '/business/userManage', '1', '0', '2019-01-09 14:09:04', '2019-01-09 14:09:06'), ('4', '内容管理', null, '-1', '0', '2019-01-09 14:09:28', '2019-01-09 14:09:30'), ('5', '文件系统', '/content/catalog', '4', '0', '2019-01-09 14:10:00', '2019-01-09 14:10:02'), ('6', '参数配置', '/business/systemConfigManage', '1', '0', '2019-01-14 13:50:24', '2019-01-14 13:50:26');
COMMIT;

-- ----------------------------
--  Table structure for `business_role`
-- ----------------------------
DROP TABLE IF EXISTS `business_role`;
CREATE TABLE `business_role` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) DEFAULT NULL,
  `role_des` varchar(255) DEFAULT NULL,
  `delete_flag` int(11) DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Records of `business_role`
-- ----------------------------
BEGIN;
INSERT INTO `business_role` VALUES ('1', '超级管理员', '超级管理员', '0', '2019-01-09 16:09:27', '2019-01-14 18:33:09');
COMMIT;

-- ----------------------------
--  Table structure for `business_role_resource`
-- ----------------------------
DROP TABLE IF EXISTS `business_role_resource`;
CREATE TABLE `business_role_resource` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) DEFAULT NULL,
  `resource_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Records of `business_role_resource`
-- ----------------------------
BEGIN;
INSERT INTO `business_role_resource` VALUES ('17', '3', '2', '2019-01-10 13:17:42', '2019-01-10 13:17:42'), ('18', '3', '5', '2019-01-10 13:17:42', '2019-01-10 13:17:42'), ('75', '1', '2', '2019-01-14 18:33:09', '2019-01-14 18:33:09'), ('76', '1', '3', '2019-01-14 18:33:09', '2019-01-14 18:33:09'), ('77', '1', '6', '2019-01-14 18:33:09', '2019-01-14 18:33:09'), ('78', '1', '5', '2019-01-14 18:33:09', '2019-01-14 18:33:09');
COMMIT;

-- ----------------------------
--  Table structure for `business_user`
-- ----------------------------
DROP TABLE IF EXISTS `business_user`;
CREATE TABLE `business_user` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `extra_resource` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `forbidden_resource` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `delete_flag` int(11) NOT NULL DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `nick_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `login_name` (`login_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- ----------------------------
--  Records of `business_user`
-- ----------------------------
BEGIN;
INSERT INTO `business_user` VALUES ('1', 'admin', 'e10adc3949ba59abbe56e057f20f883e', '1', '', '', '0', '2019-01-12 23:07:04', '2019-01-13 20:49:42', '霜之哀伤');
COMMIT;

-- ----------------------------
--  Table structure for `content_file`
-- ----------------------------
DROP TABLE IF EXISTS `content_file`;
CREATE TABLE `content_file` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `parent` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL COMMENT '0：文件夹，1：HTML文档，2：图片',
  `des` text,
  `delete_flag` varchar(255) DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
