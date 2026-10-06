# 💼 AI Job Assistant

一个基于 **Python + 大语言模型 API + Streamlit + SQLite** 开发的 AI 智能求职辅助系统。

项目面向求职场景，通过调用大语言模型，为用户提供简历分析、岗位分析、简历与岗位匹配、面试题生成以及自我介绍生成等功能，并通过 Streamlit 构建 Web 交互界面，实现从本地 Python 程序到在线 AI Web 应用的完整开发流程。

---

## 🌐 在线体验

项目已部署至 Streamlit Community Cloud，可通过浏览器直接访问。

👉 **在线体验：**

https://ai-job-assistant-kh84v5irzyzb3pklk8nb2h.streamlit.app/

---

## ✨ 核心功能

### 📄 1. 简历分析

输入个人简历内容，通过大语言模型分析：

- 个人优势
- 简历存在的问题
- 能力与经历亮点
- 简历优化方向
- 求职竞争力提升建议

同时支持将简历保存至 SQLite 数据库，方便后续岗位匹配使用。

---

### 💼 2. 岗位分析

输入公司、岗位名称及招聘要求，对目标岗位进行分析，包括：

- 核心岗位职责
- 关键能力要求
- 岗位核心关键词
- 招聘方关注重点
- 面试准备方向

岗位信息可以保存至 SQLite 数据库。

---

### 🎯 3. 简历 × 岗位匹配

综合分析个人简历与目标岗位 JD，对二者进行匹配分析，包括：

- 综合匹配情况
- 与岗位匹配的个人优势
- 当前能力差距
- 简历优化建议
- 面试准备重点
- 求职策略建议

支持直接选择 SQLite 数据库中已经保存的简历和岗位进行分析，也支持手动输入。

---

### 💬 4. 面试题生成

根据目标公司、岗位及招聘要求，通过大语言模型生成具有针对性的面试问题，帮助用户提前进行面试准备。

---

### 👤 5. 自我介绍生成

结合个人经历和目标岗位要求，生成具有岗位针对性的面试自我介绍，减少通用自我介绍与具体岗位之间的脱节。

---

## 🧠 AI 模型

项目通过大模型 API 实现 AI 能力。

当前使用：

```text
XingChenAGI/Xing4.0-29B
```

API 服务通过 SiliconFlow 接入。

项目将大模型调用封装在独立的 `ai_client.py` 模块中，使业务逻辑与模型调用逻辑分离，便于后续更换或扩展其他模型。

---

## 🛠️ 技术栈

| 技术 | 用途 |
|---|---|
| Python | 项目主要开发语言 |
| Streamlit | Web 前端及交互界面 |
| SQLite | 简历与岗位数据存储 |
| OpenAI Python SDK | 调用兼容 OpenAI API 格式的大模型接口 |
| SiliconFlow API | 大模型 API 服务 |
| Xing4.0-29B | AI 分析与文本生成 |
| python-dotenv | 本地环境变量管理 |
| Git | 项目版本管理 |
| GitHub | 代码托管 |
| Streamlit Community Cloud | Web 应用云端部署 |

---

## 🏗️ 系统架构

```text
用户
 │
 ▼
Streamlit Web 页面
 │
 ├───────────────┐
 ▼               ▼
AI 功能模块      SQLite 数据库
 │               │
 ▼               │
ai_client.py     简历 / 岗位数据
 │
 ▼
SiliconFlow API
 │
 ▼
Xing4.0-29B
 │
 ▼
AI 分析结果
 │
 ▼
Streamlit 页面展示
```

---

## 📁 项目结构

```text
AI-Job-Assistant/
│
├── main.py
│   └── CLI 主程序
│
├── web_app.py
│   └── Streamlit Web 应用入口
│
├── ai_client.py
│   └── 大语言模型 API 调用封装
│
├── config.py
│   └── 模型及 API 基础配置
│
├── database.py
│   └── SQLite 数据库操作
│
├── resume.py
│   └── 简历分析功能
│
├── jobs.py
│   └── 岗位分析功能
│
├── matcher.py
│   └── 简历与岗位匹配功能
│
├── interview.py
│   └── 面试题及自我介绍生成功能
│
├── requirements.txt
│   └── Python 项目依赖
│
├── .gitignore
│   └── Git 忽略文件配置
│
└── README.md
    └── 项目说明文档
```

---

## 🔑 API Key 安全管理

为了避免 API Key 泄露，本项目不会将真实 API Key 写入源代码或上传至 GitHub。

本地运行时，通过 `.env` 保存：

```env
SILICONFLOW_API_KEY=your_api_key
```

程序通过环境变量读取：

```python
api_key = os.getenv("SILICONFLOW_API_KEY")
```

`.env` 已加入 `.gitignore`，避免敏感信息被提交至 GitHub。

云端部署时，通过 Streamlit Community Cloud 的 Secrets 功能配置 API Key。

---

## 🚀 本地运行

### 1. 克隆项目

```bash
git clone https://github.com/xia0730/AI-Job-Assistant.git
```

进入项目目录：

```bash
cd AI-Job-Assistant
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

在项目根目录创建：

```text
.env
```

写入：

```env
SILICONFLOW_API_KEY=your_api_key
```

### 4. 启动 Web 应用

```bash
streamlit run web_app.py
```

默认可通过浏览器访问：

```text
http://localhost:8501
```

---

## 💡 项目特点

### 1. 面向真实求职场景

项目并非单一 AI 对话页面，而是围绕实际求职流程拆分为：

```text
简历分析
   ↓
岗位分析
   ↓
人岗匹配
   ↓
面试题生成
   ↓
自我介绍生成
```

形成较完整的求职辅助流程。

### 2. 模块化设计

将不同功能拆分为独立 Python 模块，同时将 AI 调用、数据库操作和 Web 页面进行分离，降低代码之间的耦合。

### 3. 引入数据存储

使用 SQLite 保存简历和岗位信息，使用户可以在后续人岗匹配过程中直接复用已有数据。

### 4. API Key 安全管理

使用环境变量和 Streamlit Secrets 管理 API Key，避免将敏感信息直接写入代码仓库。

### 5. 完成 Web 化与云端部署

项目从最初的 Python CLI 程序逐步扩展为 Streamlit Web 应用，并部署至云端，实现公网访问。

---

## 📈 后续优化方向

后续可继续探索：

- PDF / Word 简历自动解析
- 多岗位批量匹配与排序
- 更结构化的匹配评分机制
- 用户数据管理
- 云端持久化数据库
- Prompt 进一步优化
- 多模型切换
- 求职数据可视化
- RAG 求职知识库
- AI Agent 求职工作流

---

## ⚠️ 说明

本项目主要用于 AI 应用开发学习、求职辅助及技术实践。

AI 生成内容仅作为求职准备参考，实际求职过程中应结合个人真实经历、岗位要求及招聘信息进行判断。

---

## 👨‍💻 Author

**Xuefeng Xia**

GitHub: `xia0730`