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

 Date: 01/14/2019 11:42:46 AM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Records of `business_resource`
-- ----------------------------
BEGIN;
INSERT INTO `business_resource` VALUES ('1', '系统管理', null, '-1', '0', '2019-01-09 14:07:07', '2019-01-09 14:07:11'),
                                       ('2', '角色列表', '/business/roleManage', '1', '0', '2019-01-09 14:08:35', '2019-01-09 14:08:37'),
                                       ('3', '用户列表', '/business/userManage', '1', '0', '2019-01-09 14:09:04', '2019-01-09 14:09:06'),
                                       ('4', '学校管理', null, '-1', '0', '2019-01-09 14:09:28', '2019-01-09 14:09:30'),
                                       ('5', '学校列表', '/business/index', '4', '0', '2019-01-09 14:10:00', '2019-01-09 14:10:02');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
