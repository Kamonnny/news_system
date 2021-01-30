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


create table news
(
    id          int unsigned primary key auto_increment,
    title       varchar(255),
    content     text,
    tag_id      int unsigned comment '标签id',
    create_time datetime,
    update_time datetime,
    status      tinyint,
    fulltext key title_content_fulltext (title, content),
    index tag_id (tag_id),
    index create_time (create_time)
);

create table tags
(
    id          int unsigned primary key auto_increment,
    tag         varchar(16) comment '标签名',
    create_time datetime,
    update_time datetime,
    status      tinyint
) comment '标签';

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
