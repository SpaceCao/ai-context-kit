# `.ai-context` 使用说明

这个目录不是给人完整阅读的项目文档，而是给 AI 工具做“最小必要上下文”。

设计目标只有两个：

1. **减少重复读仓库**
2. **避免一次性喂大段正文**

---

## 最小可用组合

如果你只想先跑起来，至少准备这 3 个文件：

- `project-summary.template.md` 的实例版
- `task-pack.template.md` 的实例版
- `prompt.template.md`

这时即使没有向量库，也已经能明显省 token。

---

## 推荐落地顺序

### 1. 复制模板并去掉 `.template`

建议形成如下实例文件：

```text
.ai-context/
├── project-summary.md
├── topic-card-auth.md
├── topic-card-billing.md
├── task-pack-design-homepage.md
├── prompt.md
└── retrieval-index.json
```

### 2. `project-summary.md` 控制在短摘要

不要写成长文，尽量控制在 500-1200 token。

### 3. `topic-card-*` 一个主题一张卡

不要做“大而全”总结；要做“可路由、可过滤”的卡片。

### 4. `task-pack-*` 一次任务一份

任务越具体，token 越省。

---

## 检索策略建议

推荐顺序：

1. 先按目录/模块/阶段过滤
2. 再按关键词/BM25 检索
3. 再补向量召回
4. 最后 rerank

向量库适合解决“我知道相关，但关键词不完全命中”的问题；  
不适合独立承担“项目路由”和“任务边界”。
