create database news_system;

use news_system;

drop table if exists users;
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

drop table if exists news;
create table news
(
    id          int unsigned primary key auto_increment,
    title       varchar(255),
    content     text,
    tag_id      int unsigned comment '标签id',
    views       bigint unsigned,
    create_time datetime,
    update_time datetime,
    status      tinyint,
    fulltext key title_content_fulltext (title, content),
    index tag_id (tag_id),
    index create_time (create_time)
);

drop table if exists tags;
create table tags
(
    id          int unsigned primary key auto_increment,
    tag         varchar(16) comment '标签名',
    create_time datetime,
    update_time datetime,
    status      tinyint
) comment '标签';


drop table if exists comments;
create table comments
(
    id          int unsigned primary key auto_increment,
    user_id     int unsigned,
    news_id     int unsigned,
    comment     varchar(255),
    create_time datetime,
    update_time datetime,
    status      varchar(32)
) comment '评论';
