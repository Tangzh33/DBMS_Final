
-- OLD
CREATE TABLE messages (
  id SERIAL NOT NULL,
  mid varchar(45) DEFAULT NULL,
  time varchar(45) DEFAULT NULL,
  content varchar(1000) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_messages_users FOREIGN KEY (mid) REFERENCES users (uid)
);

CREATE TABLE users (
  uid varchar(45) UNIQUE NOT NULL,
  password varchar(45) NOT NULL,
  PRIMARY KEY (uid)
);

INSERT INTO messages VALUES (8,'hw','2022-04-18 11:47:08','大家好\n'),(9,'lulu','2022-04-18 11:47:20','你好\n'),(10,'hw','2022-04-18 11:48:19','社会主义核心价值观是社会主义核心价值体系的内核，体现社会主义核心价值体系的根本性质和基本特征，反映社会主义核心价值体系的丰富内涵和实践要求，是社会主义核心价值体系的高度凝练和集中表达\n'),(11,'lulu','2022-04-18 11:48:34','党的十八大提出，倡导富强、民主、文明、和谐，倡导自由、平等、公正、法治，倡导爱国、敬业、诚信、友善，积极培育和践行社会主义核心价值观\n'),(12,'lulu','2022-04-18 11:48:42','新中国的建立，确立了以社会主义基本政治制度、基本经济制度的确立和以马克思主义为指导思想的社会主义意识形态，为社会主义核心价值体系建设奠定了政治前提、物质基础和文化条件\n'),(13,'hw','2022-04-18 11:49:05','高举中国特色社会主义伟大旗帜，以邓小平理论、“三个代表”重要思想、科学发展观为指导，深入学习贯彻党的十八大精神和习近平同志系列讲话精神，紧紧围绕坚持和发展中国特色社会主义这一主题，紧紧围绕实现中华民族伟大复兴中国梦这一目标，紧紧围绕“三个倡导”这一基本内容，注重宣传教育、示范引领、实践养成相统一，注重政策保障、制度规范、法律约束相衔接，使社会主义核心价值观融入人们生产生活和精神世界，激励全体人民为夺取中国特色社会主义新胜利而不懈奋斗。\n'),(14,'hw','2022-04-18 11:54:23','bb**'),(15,'lulu','2022-04-18 12:19:29','@robot 天津的天气如何@@天津:周一 04月18日,多云转晴 东风转西南风,最低气温12度，最高气温21度。'),(16,'hw','2022-04-18 12:37:24','@robot 达州的天气呢@@达州:周一 04月18日,阴 持续无风向,最低气温12度，最高气温21度。'),(17,'hw','2022-04-18 20:23:14','@robot 全世界最帅的人是谁@@人品好，心地善良的男人都很帅呢。');

INSERT INTO users VALUES ('hw','e10adc3949ba59abbe56e057f20f883e'),('hw2','e10adc3949ba59abbe56e057f20f883e'),('lulu','e10adc3949ba59abbe56e057f20f883e'),('quantumcloud','e10adc3949ba59abbe56e057f20f883e'),('test','e10adc3949ba59abbe56e057f20f883e');

--OUR
-- Time Format: '2003-04-12 04:05:06'
-- 1. _user：
create table _user(
    uid serial not null,
    name varchar(20) not null,
    nickname varchar,
    gender varchar(10),
    hobby varchar(100),
    passwd varchar(47) not null,
    primary key(uid)
);

-- 2. Message：
create table Message(
    mid serial not null,
    contents varchar(100) not null,
    _timestamp TIMESTAMP not null,
    primary key(mid)
);

-- 3. chatgroup:
create table chatgroup(
    gid serial not null,
    chatgroupname varchar(20) not null,
    _timestamp TIMESTAMP not null,
    primary key(gid)
);

-- 4. Articles:
create table articles(
    aid int not null ,
    content_url varchar(100) not null,
    _timestamp TIMESTAMP not null,
    primary key(aid)
);

-- 5. Comment:
create table comment(
    cid serial not null,
    contents varchar(100) not null,
    _timestamp TIMESTAMP not null,
    aid int not null,
    uid int not null,
    primary key(cid),
    foreign key(aid) references articles(aid) on delete cascade,
    foreign key(uid) references _user(uid) on delete cascade
);

-- 6. History; 
create table history(
    hid serial not null,
    aid int not null,
    uid int not null,
    _timestamp TIMESTAMP not null,
    primary key(hid),
    foreign key(aid) references articles(aid) on delete cascade,
    foreign key(uid) references _user(uid) on delete cascade
);

--7 _user2chatgroup
create table _user_chatgroup
(
    uid int not null,
    gid int not null,
    primary key(uid,gid),
    foreign key(uid) references _user(uid) on delete cascade,
    foreign key(gid) references chatgroup(gid) on delete cascade
);

--8. _user2message
create table _user_message
(
    uid int not null,
    mid int not null,
    primary key(uid,mid),
    foreign key(uid) references _user(uid) on delete cascade,
    foreign key(mid) references message(mid) on delete cascade
);

--9. _user2article
create table _user_article
(
    uid int not null,
    aid int not null,
    primary key(uid,aid),
    foreign key(uid) references _user(uid) on delete cascade,
    foreign key(aid) references articles(aid) on delete cascade
);

--10. message2chatgroup
create table message_chatgroup
(
    mid int not null,
    gid int not null,
    primary key(mid,gid),
    foreign key(mid) references message(mid) on delete cascade,
    foreign key(gid) references chatgroup(gid) on delete cascade
);