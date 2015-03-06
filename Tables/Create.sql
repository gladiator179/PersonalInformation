DROP DATABASE personal_information;
CREATE DATABASE personal_information;
USE personal_information;


/*
 * 本文件主要用于记录创建各个表的sql语句
 */
create table basic_information
(
    user_id       bigint     AUTO_INCREMENT primary key ,
    user_name     varchar(50)  not null,
    user_sex       enum('男', '女'),                 /* 这里应更换为枚举类型 */
    user_email    varchar(50),
    user_passwd   varchar(50),
    user_phone    varchar(20)
);

create table memorandum
(
    memo_id     bigint        primary key AUTO_INCREMENT,
    memo_date   date          not null,
    memo_place  varchar(30),
    memo_happen varchar(70)   not null,
    u_id        bigint,
    foreign key (u_id) references basic_information(user_id)
);

create table address_list
(
    address_id  bigint        primary key AUTO_INCREMENT,
    al_name     varchar(50)     not null,
    al_phone    varchar(20)     not null,
    u_id        bigint,
    foreign key (u_id) references basic_information(user_id)
);

create table personal_journal
(
    journal_id  bigint        primary key AUTO_INCREMENT,
    j_subject   varchar(20)     not null,
    j_content   text,
    j_type      varchar(30),
    u_id        bigint,
    foreign key (u_id) references basic_information(user_id)
);

create table friends
(
    friends_id  bigint        primary key AUTO_INCREMENT,       
    f_name      varchar(50)  not null,
    f_know_date enum('小学','初中','高中', '大学','工作单位'),         
    f_birth     date,
    f_friend_email      varchar(50),
    f_friend_qq         varchar(13),
    u_id        bigint,
    foreign key (u_id) references basic_information(user_id)
);

create table admin
(
    admin_id            bigint  primary key AUTO_INCREMENT,
    admin_passwd        varchar(50) not null,
    admin_phone         varchar(50) not null
);
