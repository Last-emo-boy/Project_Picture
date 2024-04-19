# Project_Picture
## 项目名称：图片墙系统 (SFLSWALL?)

### 简介
图片墙系统是一个允许用户上传、查看和搜索具有人脸识别功能的照片库的应用。该系统旨在提供一个直观的用户界面，用户可以通过人脸匹配和名字搜索来找到特定的照片。

### 架构概述
本项目采用前后端分离的架构，后端提供RESTful API供前端调用，前端则负责展示界面和用户交互。系统主要分为以下几个部分：
1. **前端**：使用React.js构建，负责展示用户界面和与后端进行数据交互。
2. **后端**：使用Flask框架，处理API请求，实现业务逻辑，包括文件上传、人脸识别、数据检索等。
3. **数据存储**：使用SQLite数据库存储基本数据，所有的人脸数据和图像文件存储在文件系统中。

### 技术栈
- **前端**：
  - React.js
  - HTML/CSS
  - JavaScript (ES6+)
- **后端**：
  - Flask (Python)
  - face_recognition库
  - SQLAlchemy (ORM)
- **数据库**：
  - SQLite

### 模块化设计
1. **前端模块**：
   - **Home页面**：展示所有图片和搜索框。
   - **Search功能**：允许用户通过名称搜索相关的照片。
   - **Image Upload组件**：用于上传图片，并显示上传状态。
   - **Gallery视图**：根据搜索结果或全部图片显示图片墙。

2. **后端模块**：
   - **API服务**：处理前端请求，包括上传图片、搜索、获取图片列表等。
   - **人脸识别处理器**：对上传的图片进行人脸检测和识别，存储人脸数据。
   - **数据库管理**：处理所有数据库交互，如增删查改操作。

3. **数据模型**：
   - **用户**：存储用户信息（如果有用户系统）。
   - **图片**：存储图片文件路径及其元数据。
   - **人脸**：存储人脸识别得到的数据和与人物名称的关联。

### 可扩展性和升级性
- **API扩展**：后端设计为RESTful API，易于扩展新的功能和接口。
- **组件化前端**：前端使用React组件化开发，便于增加新功能和维护。
- **数据库抽象**：使用ORM管理数据库交互，支持未来更换为更高性能的数据库系统，如PostgreSQL。

### 安全性
- **文件上传安全**：后端将验证上传的文件类型和大小，避免潜在的安全风险。
- **用户验证**（如果实现）：使用JWT或OAuth进行用户身份验证和授权。

/backend
│
├── app.py                  # Flask应用的入口和配置文件
├── config.py               # 配置管理，例如数据库配置
│
├── /api                    # API端点相关的模块
│   ├── __init__.py         # 将api目录标记为Python包
│   ├── routes.py           # 路由定义
│   └── utils.py            # 辅助功能，如错误处理器、响应格式化
│
├── /models                 # 数据模型相关的模块
│   ├── __init__.py         # 将models目录标记为Python包
│   ├── user.py             # 用户模型
│   ├── image.py            # 图片模型
│   └── face.py             # 人脸数据模型
│
├── /services               # 业务逻辑层
│   ├── __init__.py         # 将services目录标记为Python包
│   ├── face_recognition.py# 人脸识别的逻辑
│   └── image_processing.py# 图像处理逻辑
│
├── /repositories           # 数据库交互层
│   ├── __init__.py         # 将repositories目录标记为Python包
│   ├── user_repository.py  # 用户数据的数据库操作
│   ├── image_repository.py # 图片数据的数据库操作
│   └── face_repository.py  # 人脸数据的数据库操作
│
├── /static                 # 存放静态文件
│   └── /uploads            # 上传的文件存储位置
│
├── /templates              # Flask模板文件（如果有前端内容由Flask渲染）
│
└── requirements.txt        # 项目依赖文件

/frontend
│
├── public                  # 公共文件，如HTML入口文件和favicon
│   ├── index.html          # 主HTML文件
│   └── favicon.ico         # 网站图标
│
├── src                     # 源代码目录
│   ├── index.js            # 应用的入口文件
│   ├── App.js              # 根组件
│   ├── App.css             # 根组件的样式
│
│   ├── /components         # 可复用组件
│   │   ├── Navbar.js       # 导航栏组件
│   │   ├── Gallery.js      # 图片墙展示组件
│   │   ├── SearchBar.js    # 搜索栏组件
│   │   └── ImageCard.js    # 单个图片卡片组件
│   │
│   ├── /pages              # 页面组件
│   │   ├── Home.js         # 主页组件
│   │   ├── Upload.js       # 图片上传页面
│   │   └── About.js        # 关于页面
│   │
│   ├── /services           # 与后端通信的服务
│   │   ├── api.js          # 封装API请求的函数
│   │
│   ├── /hooks              # 自定义钩子
│   │   ├── useFetch.js     # 用于数据获取的自定义钩子
│   │
│   ├── /context            # Context API
│   │   ├── AuthContext.js  # 认证相关的上下文
│   │
│   ├── /assets             # 静态资源，如图片和样式文件
│   │   ├── images          # 存放图片
│   │   └── styles          # 全局样式
│   │
│   ├── /utils              # 工具函数
│   │   └── helpers.js      # 辅助函数集
│   │
│   └── setupTests.js       # Jest测试设置文件
│
├── package.json            # 项目元数据和依赖关系
└── README.md               # 项目的README文件
