# GraphRAG & LightRAG 实用教程与精炼代码库

本项目整合精炼了 **Microsoft GraphRAG** 与 **LightRAG** 的核心使用配置、提示词模板、结果表解析工具脚本、LightRAG Python API 代码示例及传统向量 RAG 对比代码。

---

## 📁 目录结构

```text
.
├── README.md                      # 项目说明文档
├── .gitignore                     # Git 忽略配置
├── requirements.txt               # 依赖说明清单
├── basic_rag/                     # 传统向量 RAG 示例 (Naive RAG)
│   ├── basic_rag_langchain.py     # 基于 LangChain + FAISS 的向量库构建脚本
│   └── query_index.py             # 向量检索交互式问答脚本
├── validate_conn/                 # LLM API 连接测试
│   └── test_connection.py         # OpenAI / DeepSeek / 硅基流动 API 校验脚本
├── view_graphrag_tables/          # GraphRAG 图谱数据表导出解析
│   └── view_tables.py             # 读取 GraphRAG 导出的 Parquet 图谱表并转存为 CSV
├── graphrag_config/               # Microsoft GraphRAG 核心配置与 Prompt 模板
│   ├── .env.example               # 环境变量配置模板 (包含 GRAPHRAG_API_KEY)
│   ├── settings.yaml              # GraphRAG 核心配置文件 (支持 DashScope/Ollama/DeepSeek)
│   └── prompts/                   # 13 个 GraphRAG 核心提示词模板
└── lightrag_examples/            # ⚡ LightRAG Python API 调用代码示例
    ├── lightrag_openai_compatible_demo.py # 兼容 OpenAI 接口 (DeepSeek/Qwen/SiliconFlow) 的 LightRAG 示例
    ├── lightrag_ollama_demo.py            # 本地 Ollama 模型的 LightRAG 离线运行示例
    └── graph_visual_with_html.py          # 将 LightRAG 知识图谱导出为 3D/HTML 交互可视化的脚本
```

---

## 🛠️ 快速上手指南

### 1. 环境准备
推荐使用 Python 3.10+ 并安装项目依赖：
```bash
pip install -r requirements.txt
pip install lightrag-hku  # 安装 LightRAG 核心包
```

### 2. 测试 LLM API 联通性
配置 API Key 并校验模型连通性：
```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.siliconflow.cn/v1" # 或 DeepSeek Base URL
python validate_conn/test_connection.py
```

---

## ⚡ 1. LightRAG (代码 SDK 驱动模式)

与 Microsoft GraphRAG 依赖 CLI 命令不同，**LightRAG 支持原生 Python SDK 深度集成与嵌入**。

### 核心特点：
* **四种检索模式**：`naive`（纯向量）、`local`（局部实体）、`global`（全局社区）、`hybrid`（混合检索）。
* **极低的计算开销与快速增量更新**。

### 运行 LightRAG 示例：
```bash
# 运行基于 OpenAI 兼容 API (如 DeepSeek/SiliconFlow) 的 LightRAG 异步建图与查询
python lightrag_examples/lightrag_openai_compatible_demo.py

# 运行本地纯离线 (Ollama) LightRAG
python lightrag_examples/lightrag_ollama_demo.py

# 将构建好的 GraphML 知识图谱渲染导出为 HTML 可视化网页
python lightrag_examples/graph_visual_with_html.py
```

---

## 🕸️ 2. Microsoft GraphRAG (CLI 命令行驱动模式)

**注意**：Microsoft GraphRAG 是一个**基于命令行 (CLI) 驱动**的知识图谱引擎。

### 核心步骤：

#### 1. 初始化工作空间
```bash
python -m graphrag.index --init --root ./my_workspace
```

#### 2. 拷贝配置与输入文件
1. 将 `graphrag_config/settings.yaml` 与 `graphrag_config/prompts/` 复制到 `./my_workspace` 目录下。
2. 在 `./my_workspace` 下创建 `input/` 文件夹，将待提取图谱的 `.txt` 文档放入其中。
3. 创建 `.env` 文件设置 API Key：
   ```env
   GRAPHRAG_API_KEY=your-api-key-here
   ```

#### 3. 构建知识图谱索引 (Indexing)
运行以下 CLI 命令自动完成文本分块、实体抽取、关系提取、社区划分与社区报告生成：
```bash
python -m graphrag.index --root ./my_workspace
```

#### 4. 执行图谱问答检索 (Querying)
* **Global Search（全局社区概括搜索）**：
  ```bash
  python -m graphrag.query --root ./my_workspace --method global "这本小说/文档的主旨是什么？"
  ```
* **Local Search（局部实体细粒度搜索）**：
  ```bash
  python -m graphrag.query --root ./my_workspace --method local "贾宝玉与林黛玉是什么关系？"
  ```

#### 5. 导出并查看图谱结果表
GraphRAG 抽取的实体、关系和社区数据存放在 `output/*.parquet` 中，运行工具脚本即可一键导出为 CSV 方便查看：
```bash
python view_graphrag_tables/view_tables.py
```

---

## 🔍 3. 传统向量 RAG (Naive RAG) 对比测试

如果你想对比标准向量检索 (LangChain + FAISS) 与 图谱 RAG 的效果：

1. **构建 FAISS 向量索引**：
   ```bash
   python basic_rag/basic_rag_langchain.py
   ```
2. **交互式问答测试**：
   ```bash
   python basic_rag/query_index.py
   ```

---

## ⚖️ GraphRAG vs LightRAG 核心对比

| 特性 | Microsoft GraphRAG | LightRAG |
| :--- | :--- | :--- |
| **使用方式** | 命令行 CLI 驱动 | Python SDK / REST API 驱动 |
| **社区抽取算法** | 层次化 Leiden 社区算法 + Community Reports | 双层实体图谱 + 增量向量表 |
| **增量更新成本** | 较高 (重新生成社区报告) | 极低 (支持即时增量插入) |
| **适合场景** | 大型离线文档全量图谱挖掘 | 实时应用、Web 服务集成与动态更新 |

---

## 📄 License
MIT License.
