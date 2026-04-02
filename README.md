# AI Context Kit

一套面向本地 AI Coding「设计阶段」的通用省 token 方案。

目标不是把整个仓库塞给模型，而是把上下文拆成 4 层，只在需要时逐层补充：

1. `Project Summary`：项目级稳定摘要
2. `Topic Card`：模块/专题摘要卡
3. `Task Pack`：当前任务包
4. `Retrieved Chunks`：检索出的少量原文块

同时，这个仓库也包含一个可分发的 Codex skill：

- `skills/design-token-context/`

---

## 什么时候用向量库

不要一上来就上向量库。

| 场景 | 推荐方案 |
|------|----------|
| 文档少于 20 份，结构清楚 | 目录路由 + `rg`/关键词检索 + 摘要卡 |
| 文档 20-200 份，跨模块较多 | 元数据过滤 + BM25/关键词 + 可选向量检索 |
| 文档 200+、PDF 多、语义问法多 | 混合检索，向量库开始变得划算 |

结论：**向量库是加速器，不是主架构。**

最稳的方案始终是：

`路由过滤 -> 关键词/BM25 -> 向量召回(可选) -> rerank -> 只喂前 3-6 个 chunk`

---

## 仓库结构

```text
.ai-context/
├── README.md
├── project-summary.template.md
├── topic-card.template.md
├── task-pack.template.md
├── prompt.template.md
└── retrieval-index.template.json
```

---

## 推荐使用方式

### 第一步：先填 `project-summary`

每个仓库只保留一份 500-1200 token 的稳定摘要，内容只写：

- 项目目标
- 当前阶段
- 目录路由
- 关键约束
- 必读文档
- 不要做什么

### 第二步：按模块写 `topic-card`

每张卡尽量控制在 200-500 token，只写：

- 已确认
- 高概率
- 待确认
- 关键词
- 必读文件
- 排除范围

### 第三步：每次任务都写 `task-pack`

`task-pack` 是最省 token 的关键。它把“当前任务到底要读什么、不该读什么、完成标准是什么”固定下来，避免模型每次重新扫仓库。

### 第四步：只在必要时喂原文块

如果摘要卡不足，再从 `retrieval-index` 中取前 3-6 个 chunk。

---

## 推荐调用顺序

给 Claude / Codex / ChatGPT 的上下文顺序建议固定为：

1. `project-summary`
2. 当前 `task-pack`
3. 相关 `topic-card` 1-3 张
4. 检索返回的原文 chunk 3-6 个

不要直接：

- 贴整个 `README`
- 贴整份 PRD
- 贴整个代码目录
- 让模型“自己去读全仓库”

---

## 维护规则

- `project-summary`：只在方向变化时更新
- `topic-card`：模块结论变化时更新
- `task-pack`：按任务创建，可沉淀为历史记录
- `retrieval-index`：文档更新后重建

---

## 适用范围

这套脚手架适合：

- 产品方案设计
- 技术方案设计
- 重构设计
- 招标/RFP前置梳理
- 文档型代码仓库
- 代码 + 设计混合仓库

如果你愿意继续扩展，下一步通常是：

1. 给每个真实项目复制 `.ai-context/`
2. 先手工填 `project-summary`
3. 先只用关键词/BM25
4. 只有召回效果不够时再接 Qdrant / Chroma / FAISS
