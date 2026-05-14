# 考勤系统 README

本项目是一个基于 B/S 架构的课程结课作业考勤系统，后端使用 `FastAPI`，前端使用 `Vue 3 + Element Plus`。

当前已经打通的主链路包括：
- 教师登录
- 前端考勤页
- 活体检测
- 考勤记录筛选与导出
- 学生信息管理
- 学生账号自动绑定
- 学生端个人中心
- 合照识别
- 合照准确率评估
- 活动参与频次统计与报表
- 情绪统计页

## 项目结构

```text
Time_Attendance/
├─ backend/                 # FastAPI 后端
├─ frontend/                # Vue 3 前端
├─ 6.考勤系统.pptx
├─ 框架.md
└─ README.md
```

## 运行环境

- Windows 10 / 11
- PowerShell
- Python 3.10+
- Node.js 20+
- npm 10+

## 从零运行项目

以下命令默认在项目根目录 `D:\code\Time_Attendance` 下执行。

### 1. 安装后端依赖

```powershell
pip install -r backend\requirements.txt
```

如果你使用 Conda，也可以：

```powershell
conda env create -f backend\environment.yml
conda activate attendance_cs
```

### 2. 安装前端依赖

```powershell
cd frontend
npm install
cd ..
```

### 3. 启动后端

新开一个 PowerShell：

```powershell
cd D:\code\Time_Attendance\backend
python run.py
```

后端地址：

```text
http://127.0.0.1:8000
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

### 4. 启动前端

再开一个 PowerShell：

```powershell
cd D:\code\Time_Attendance\frontend
npm run dev
```

前端地址通常为：

```text
http://127.0.0.1:5173
```

## 默认账号

系统启动后会自动初始化教师账号，并为已有学生自动补齐学生账号。

教师账号：

```text
username: teacher
password: 123456
```

学生账号规则：

- 默认以 `student_no` 作为登录用户名
- 若重名会自动回退到 `stu_{student_no}` 等备用用户名
- 默认密码为 `123456`

当前仓库现有示例学生账号通常为：

```text
username: 20240001
password: 123456
```

## 学生端说明

学生登录后会自动进入学生端页面 `/student-portal`，可查看：

- 个人信息
- 本人考勤记录
- 本人活动参与记录
- 本人情绪记录

学生角色会被路由守卫限制，不能直接访问教师端页面。

## 如何验证系统正常运行

### 1. 后端健康检查

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/system/health
```

### 2. 教师登录检查

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/auth/login `
  -ContentType "application/json" `
  -Body '{"username":"teacher","password":"123456"}'
```

### 3. 前端构建检查

```powershell
cd D:\code\Time_Attendance\frontend
npm run build
```

### 4. 学生端接口冒烟检查

可以在 `backend` 目录下执行：

```powershell
@'
import sys
sys.dont_write_bytecode = True
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
teacher = client.post('/api/v1/auth/login', json={'username': 'teacher', 'password': '123456'})
print(teacher.status_code)
'@ | python -B -
```

## 当前已实现的主要功能

后端：

- JWT 登录鉴权
- 教师 / 学生角色区分
- 学生增删改查
- 学生 CSV 批量导入
- 学生账号自动生成、绑定、重置密码
- 学生注册照上传与特征提取
- 单张图片考勤识别
- 活体检测
- 考勤记录查询与导出
- 合照识别与识别结果存储
- 合照准确率评估
- 活动频次统计与 Excel 报表
- 情绪记录与情绪统计接口

前端：

- 登录页
- 教师端考勤页
- 安全测试页
- 学生管理页
- 合照识别页
- 统计报表页
- 情绪统计页
- 学生端个人中心页

## 已验证通过的命令

以下命令已经在当前仓库实际执行通过：

```powershell
cd D:\code\Time_Attendance\frontend
npm run build
```

```powershell
cd D:\code\Time_Attendance\backend
@'
import sys
sys.dont_write_bytecode = True
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
print(client.post('/api/v1/auth/login', json={'username': 'teacher', 'password': '123456'}).status_code)
'@ | python -B -
```

## 注意事项

- 首次安装 `torch`、`torchvision`、`facenet-pytorch` 会比较慢，属于正常现象。
- 浏览器考勤页依赖摄像头权限，若无法调起，请检查浏览器授权。
- Windows 下个别 `__pycache__` 目录可能存在写权限问题；这不会影响接口运行，但会影响 `compileall` 这类需要落盘 `.pyc` 的检查命令。
