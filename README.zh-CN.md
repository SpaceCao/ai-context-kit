# AI Context Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/SpaceCao/ai-context-kit)](https://github.com/SpaceCao/ai-context-kit/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/SpaceCao/ai-context-kit?style=social)](https://github.com/SpaceCao/ai-context-kit/stargazers)

[English](README.md) | [简体中文](README.zh-CN.md)

`AI Context Kit` 是一套面向设计阶段 AI 工作流的低 token 上下文方案。

它解决的核心问题是：不要在每一轮对话里都把整个仓库、整份 PRD 或整篇设计文档重新喂给模型。相反，它把上下文拆成几个稳定而小的层级，只在当前任务确实需要时再补充证据片段。

本仓库包含：

- 一套可复制到任意项目中的 `.ai-context/` 脚手架
- 一个可复用的 Codex skill：`skills/design-token-context/`
- 项目摘要、专题卡、任务包、检索索引的模板

仓库地址：

- `https://github.com/SpaceCao/ai-context-kit`

---

## 为什么要做这个

大多数 AI coding / AI 设计场景都会在这些地方浪费 token：

- 每次对话都重复读取同一份项目背景
- 明明只需要一个章节，却把整份长文档贴进去
- 过早引入向量检索，但没有任务边界和目录路由
- 让 Claude Code、Gemini、Cursor、ChatGPT 默认扫描整个仓库

`AI Context Kit` 的做法是把上下文拆成四层：

1. 稳定的项目上下文
2. 专题级上下文
3. 任务级上下文
4. 证据级检索片段

这样可以降低 token 消耗，同时让提示词更干净、输出更稳定。

---

## 核心模型

推荐的上下文栈有四层：

1. `Project Summary`  
   项目级稳定背景、结构、约束、必读入口。

2. `Topic Card`  
   某个模块、能力域或专题的一页摘要卡。

3. `Task Pack`  
   单次任务的工作包，明确这次要读什么、不要读什么、完成标准是什么。

4. `Retrieved Chunks`  
   只有在前面几层不足时，才额外补充少量证据片段。

这个仓库的核心原则是：

> 先路由，再摘要，最后检索。

不要一开始就让模型读全仓库。  
也不要在没有必要时，一开始就上向量检索。

---

## 适用场景

这套方案特别适合：

- 产品方案设计与 PRD 编写
- 技术方案与架构文档撰写
- 重构规划与迁移规划
- 招标、RFP、采购前置梳理
- 文档密集型工程仓库
- 代码与文档混合、上下文成本很高的仓库

不太适合：

- 只有少量短文件的小仓库
- 只修改 1-2 个文件的窄范围编码任务
- 没有项目记忆要求的纯聊天或头脑风暴场景

---

## 什么时候需要向量库

不要默认“有文档就该上向量库”。

| 场景 | 推荐策略 |
|------|----------|
| 文档少于 20 份，目录结构清晰 | 目录路由 + 关键词搜索 + 摘要卡 |
| 20-200 份文档，跨模块较多 | 元数据过滤 + 关键词/BM25 + 可选向量 |
| 200+ 文档、PDF 多、问法偏语义化 | 混合检索开始更有价值 |

推荐的检索顺序：

`metadata filter -> keyword/BM25 -> vector search (optional) -> rerank -> top 3-6 chunks`

向量库是加速器，不是整个架构本身。

---

## 检索模式

`AI Context Kit` 支持三种实用运行模式。

### 1. 无向量模式

适合：

- 小型仓库
- 目录结构清晰
- 模块边界明确的任务

使用：

- `project-summary`
- `topic-card`
- `task-pack`
- 目录路由
- 关键词搜索或 BM25

这种模式下**不需要额外安装向量库**。

### 2. 混合模式

适合：

- 中等规模仓库
- 跨模块设计任务
- 关键词搜索有效，但偶尔召回不足的情况

使用：

- 元数据过滤
- 关键词 / BM25 检索
- 可选向量召回
- chunk 发送给模型前做 rerank

当“摘要优先 + 路由优先”开始漏召回时，这通常是最自然的升级路径。

### 3. 向量模式

适合：

- 大型文档集合
- PDF 多、知识库长
- 用户问题更偏语义表达、关键词不稳定

使用：

- embedding
- 向量库
- 元数据过滤
- 可选 rerank

即使进入这个模式，也依然应该把 `project-summary`、`topic-card`、`task-pack` 作为主要上下文层。

---

## 向量检索的安装方式

开始使用本仓库时，**并不需要**安装向量库。

建议先跑通无向量模式，只有当检索质量确实不够时，再补向量检索。

### 方案 A：Chroma

适合本地实验和轻量文档库。

```bash
pip install chromadb
```

### 方案 B：FAISS

适合本地进程内相似度检索。

```bash
pip install faiss-cpu
```

### 方案 C：Qdrant

适合元数据过滤更强、服务化部署的场景。

```bash
docker run -p 6333:6333 qdrant/qdrant
```

或者：

```bash
pip install qdrant-client
```

### Embedding

如果你要加向量检索，还需要 embedding 模型或 embedding API。

常见选择：

- OpenAI embeddings
- 本地 embedding 模型，例如 `bge`、`gte`

实践里，最小可用链路通常是：

`documents -> chunking -> embeddings -> vector store -> rerank -> top chunks`

---

## 仓库内容

### `.ai-context/`

可复用脚手架包含：

```text
.ai-context/
├── README.md
├── project-summary.template.md
├── topic-card.template.md
├── task-pack.template.md
├── prompt.template.md
└── retrieval-index.template.json
```

### `skills/design-token-context/`

仓库同时提供一个 Codex skill，包含：

- 可复用的 `SKILL.md`
- 一个脚手架脚本
- 模板资源
- 一份简短的检索决策 playbook

---

## 快速开始

### 方案 A：直接复制脚手架

1. 把 `.ai-context/` 复制到目标仓库
2. 将模板改成真实工作文件，例如：
   - `project-summary.md`
   - `topic-card-<topic>.md`
   - `task-pack-<task>.md`
   - `prompt.md`
   - `retrieval-index.json`
3. 先填写 `project-summary.md`
4. 每个任务单独创建一个 `task-pack`
5. 只为当前活跃模块创建 `topic-card`

### 方案 B：使用 Codex skill

如果你已经把 skill 安装到 `~/.codex/skills/design-token-context/`，可以运行：

```bash
python3 ~/.codex/skills/design-token-context/scripts/scaffold_ai_context.py --target /path/to/repo
```

脚本会在目标仓库中生成 `.ai-context/`。

---

## 推荐工作流

### 第一步：写 `project-summary`

它应该尽量短且稳定，通常包括：

- 项目名称与目标
- 当前阶段
- 目录路由
- 关键约束
- 必读文档
- 明确不在本轮范围内的话题

建议长度：`500-1200` tokens。

### 第二步：创建 `topic-card`

每张卡只覆盖一个主题：

- 已确认事实
- 高概率判断
- 未确认问题
- 相关文件
- 检索关键词
- 与相邻主题的边界

建议长度：每张 `200-500` tokens。

### 第三步：每个任务创建一个 `task-pack`

这是整套方案里最重要的文件。

一个好的 `task-pack` 应该明确：

- 当前任务是什么
- 什么叫完成
- 必须读取哪些文件
- 明确不要读取哪些文件
- 建议使用哪些关键词或过滤条件

建议长度：`200-600` tokens。

### 第四步：只有在必要时补检索片段

如果模型仅靠摘要层无法完成任务，再补：

- `3-6` 个相关 chunk
- 不要补整篇长文
- 不要给“把仓库都读一遍”这种宽指令

---

## 不同工具的使用方式

### Codex

最适合：

- 仓库感知型工作流
- 本地 coding 任务
- 多项目重复复用

推荐输入顺序：

1. `project-summary`
2. 当前 `task-pack`
3. `topic-card`
4. 必要时补检索片段

### Claude Code

最适合：

- 设计推理
- 重构计划
- 结构化草稿
- 面向任务的实现支持

推荐方式：

- 在目标仓库中准备 `.ai-context/`
- 优先让 Claude Code 先读相关 `.ai-context` 文件
- 不要默认让它扫描整个仓库

推荐提示词：

```text
Use only the provided project-summary, task-pack, topic-card files, and a few evidence chunks if needed.

Do not read the entire repository by default.
Classify conclusions as: confirmed / high-probability / unknown.
If the current context is insufficient, return retrieval suggestions first.
```

### Gemini

最适合：

- 方案对比
- 信息收敛
- 结构化提纲
- 风险与缺口分析

推荐方式：

- 按顺序提供 `.ai-context` 内容
- 不要一开始就贴整份 PRD 或完整仓库树
- 让 Gemini 先做压缩、比较、结构化，再决定是否继续深检索

推荐提示词：

```text
Work only from the provided project-summary, task-pack, topic-cards, and a small set of evidence snippets.

Do not ask to read the entire repository unless the current context is insufficient.
If evidence is missing, suggest which keywords or files should be retrieved next.
```

### Cursor

最适合：

- 代码导航
- 局部编辑
- 编辑器内的轻量设计支持

推荐方式：

- 把 `.ai-context/` 放在仓库里
- 固定打开或 pin 住 `project-summary.md` 和当前 `task-pack`
- 用 `topic-card` 约束编辑器侧的上下文扩张

### ChatGPT

最适合：

- 人工复制粘贴场景
- 轻量规划
- 无仓库集成的公共 Web 场景

推荐方式：

- 只粘贴最小 `.ai-context` 层
- 当第一次回答暴露证据缺口时，再补检索片段

---

## 最小提示词模式

对大多数工具，下面这段已经足够：

```text
You are working only from the following context:
1. project-summary
2. current task-pack
3. selected topic-cards
4. a few evidence chunks when necessary

Rules:
- do not default to reading the whole repository
- do not assume missing facts
- classify conclusions as confirmed / high-probability / unknown
- if evidence is insufficient, return retrieval suggestions instead of expanding blindly
```

---

## 实践建议

### 建议这样做

- 保持摘要短小
- 一个任务对应一个 task pack
- 先按模块路由，再做检索
- 一次只补少量 chunk
- 严格区分事实与假设

### 不建议这样做

- 每次都把整份 PRD 贴进对话
- 一上来就让模型“把整个仓库读一遍”
- 把向量搜索当成唯一或第一层路由
- 把摘要文件越写越长，最后变成新的长文档

---

## 示例

仓库现在提供了一个最小示例项目：`examples/minimal-design-repo/`。

它展示了以下结构应该如何组织：

- `project-summary.md`
- `topic-card-*.md`
- `task-pack-*.md`
- 作为原始材料来源的小型 `docs/` 目录

如果你想在迁移到自己仓库之前先看一个完整例子，可以直接从这个示例开始。

## 作为公共 Starter Kit 的使用建议

如果你想把这个仓库作为团队或公开 starter kit 使用：

- 给每个真实项目复制一份 `.ai-context/`
- 安装或复用 `skills/design-token-context/`
- 团队统一使用四层上下文模型
- 在摘要优先流程跑稳之后，再考虑补检索系统

---

## 仓库结构

```text
.
├── .ai-context/
│   ├── README.md
│   ├── project-summary.template.md
│   ├── topic-card.template.md
│   ├── task-pack.template.md
│   ├── prompt.template.md
│   └── retrieval-index.template.json
└── skills/
    └── design-token-context/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── assets/ai-context/*
        ├── references/playbook.md
        └── scripts/scaffold_ai_context.py
```

---

## 后续可扩展方向

采用这套方案后，常见的下一步包括：

- 增加 `project-summary` 初稿生成器
- 增加 `topic-card` 草稿生成器
- 为大仓库增加检索索引构建器
- 为团队定义命名规范和证据等级规范

如果你只采纳这个仓库的一条原则，那就是：

> 始终只给模型“足以正确完成当前任务”的最小上下文。
