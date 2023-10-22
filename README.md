# 简介
FileFlow是一个使用 FastAPI 和 Vue3 开发的简单网盘系统，实现了基本的文件上传和下载功能。个人作业项目，仅供参考使用，请勿用于生产用途。（注：本项目随课程结束可能不再更新。）
# 概述
该网盘系统提供基本的文件管理功能，目前已完成的功能：

* 前后端分离：前端使用Vue3，后端使用FastAPI。  
* 用户注册和登录：使用JWT进行用户认证，支持refresh token。用户注册后写入数据库，密码使用bcrypt进行加密。  
* 用户权限分级：用户分为普通用户和管理员，每个用户只能查看自己的文件。  
* 文件上传：上传文件，并将文件信息写入数据库。  
* 文件下载：下载服务器上的文件。  

暂时未实现的功能：  
* 多文件上传下载  
* 用户权限管理  


建议通过 Docker 来部署这个项目，以确保环境配置的一致性和部署的便捷性。
# 使用docker部署
## 克隆项目
```bash
git clone [项目的Git仓库地址]
```
## 构建前端
```bash
cd frontend
docker build -t frontend .
```
## 构建后端
```bash
cd backend
docker build -t backend .
```
## 启动项目
```bash
docker run -d -p 80:80 --name frontend frontend
docker run -d -p 8000:8000 --name backend backend
```
## 一键部署(包含nginx)
```bash
docker-compose up -d
```
# 致谢
特别感谢 [Pure Admin](https://github.com/pure-admin/vue-pure-admin) 项目，它的开源代码为本项目的前端部分提供了极大的便利。[Pure Admin](https://github.com/pure-admin/vue-pure-admin) 是作为项目的一部分而被使用，本项目的其他部分由本人独立开发。