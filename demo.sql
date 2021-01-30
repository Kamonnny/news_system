create database news_system;

use news_system;

create table users
(
    id          int unsigned primary key auto_increment,
    username    varchar(32),
    password    varchar(255),
    email       varchar(64),
    create_time datetime,
    update_time datetime,
    status      tinyint,
    is_admin    tinyint comment '是否是管理员',
    unique index username (username),
    unique index email (email),
    index create_time (create_time)
);

#
# create table user_groups
# (
#     id          int unsigned primary key auto_increment comment 'id 为非负整型',
#     group_name  varchar(32),
#     power       json,
#     create_time datetime,
#     update_time datetime
# );
#
# create table powers
# (
#     id          int unsigned primary key auto_increment,
#     power_name  varchar(64),
#     create_time datetime
# );
#
# create table news
# (
#     id          int unsigned primary key auto_increment,
#     title       varchar(255),
#     content     text,
#     tag_id      int unsigned comment '标签id',
#     create_time datetime,
#     update_time datetime,
#     status      varchar(32)
# );
#
# create table tags
# (
#     id          int unsigned primary key auto_increment,
#     tag         varchar(16) comment '标签名',
#     create_time datetime
# ) comment '标签';
#
# create table comment
# (
#     id          int unsigned primary key auto_increment,
#     news_id     int unsigned,
#     comment     varchar(255),
#     create_time datetime,
#     update_time datetime,
#     status      varchar(32)
# ) comment '评论';
