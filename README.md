# README

## 0.简介

该项目为2022学年中山大学计算机学院数据库期末大作业——基于Opengauss数据库的网络聊天室，包括了socket通信、基于CustomTkinter的GUI界面、MD5加密等技术，实现了在线聊天、消息同步等功能。



## 1.文件结构

值得注意的是：**录制的视频**结果存放在**result_video**文件夹下；演示视频可以使用Chrome播放。

```bash
.
├── Client.py 客户端
├── LoginPanel.py 注册界面
├── MD5.py	密码MD5加密
├── Main.py 客户端主函数
├── MainPanel.py	主界面
├── RegisterPanel.py 注册界面
├── Server.py	服务端
├── databaseTool.py 数据库接口
├── emoji 表情
├── res 数据库建表等资源文件
**├──result_video 录制视频结果**
└── image 素材图片
```


## 2.环境依赖

```bash
Python 3.10.2  
psycopg2 2.9.5
Opengauss
```




## 3.使用

- 修改databaseTool.py文件中有关数据库的配置（如数据库的ip地址，端口号，账号密码等）
- 运行Server.py启动服务端
- 运行Main.py启动客户端





