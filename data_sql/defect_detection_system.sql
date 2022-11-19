/*
 Navicat Premium Data Transfer

 Source Server         : mysql8018Test
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : defect_detection_system

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 04/10/2022 13:00:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tbl_picture
-- ----------------------------
DROP TABLE IF EXISTS `tbl_picture`;
CREATE TABLE `tbl_picture`  (
  `picture_id` int(20) NOT NULL AUTO_INCREMENT COMMENT '图片id',
  `picture_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '图片名称',
  `created_time` datetime(0) NOT NULL COMMENT '图片生成时间',
  `update_time` datetime(0) NOT NULL COMMENT '图片修改时间',
  `picture_width` double(20, 0) NOT NULL COMMENT '图片宽度',
  `picture_height` double(20, 0) NOT NULL COMMENT '图片高度',
  `picture_size` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片大小（字节）',
  `picture_format` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片格式',
  `uploader_id` int(20) UNSIGNED NOT NULL COMMENT '图片用户id',
  `uploader_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片用户名称',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图片描述',
  `is_test` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片是否被测试',
  `save_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图片源位置',
  `result_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图片结果路径的位置（存放的是已经标记过的图片）',
  PRIMARY KEY (`picture_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tbl_picture
-- ----------------------------
INSERT INTO `tbl_picture` VALUES (1, 'wyy_1', '2021-11-02 00:00:00', '2022-03-19 21:49:26', 64, 64, '700KB', 'jpg', 1, 'wyy', 'wyy上传的第1张图片', '是', 'img/imagesDB/wyy_1.jpg', 'img/imagesResultDB/wyy_1_result.jpg');
INSERT INTO `tbl_picture` VALUES (2, 'wyy_2', '2022-02-08 23:58:54', '2022-02-08 23:58:57', 64, 88, '900KB', 'jpg', 1, 'wyy', 'wyy的第2张图片', '否', 'img/imagesDB/wyy_1.jpg', '');

-- ----------------------------
-- Table structure for tbl_user
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user`  (
  `user_id` int(20) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `user_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户姓名',
  `login_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录用户名',
  `login_password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录用户密码',
  `phone_number` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户手机号',
  `info` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户详情',
  `identification` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户身份',
  `lastLoginTime` datetime(0) NOT NULL COMMENT '用户最后登录时间',
  `register_time` datetime(0) NOT NULL COMMENT '用户注册时间',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
INSERT INTO `tbl_user` VALUES (1, 'wyy', 'wyy', 'wyy666888', '13803907433', 'A admin manager!', 'admin', '2022-03-19 21:49:13', '2021-12-12 19:47:45');

SET FOREIGN_KEY_CHECKS = 1;
