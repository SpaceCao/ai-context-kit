# Low-token design playbook

## 1. Retrieval strategy decision table

| Repo shape | Recommended mode |
|------------|------------------|
| 文档少、目录清晰、模块边界明确 | 目录路由 + 关键词/BM25 |
| 文档中等规模、跨模块较多 | 元数据过滤 + 关键词/BM25 + 可选向量 |
| 文档大、PDF多、问法语义化明显 | 混合检索，加入向量库 |

结论：先建上下文层，再决定是否接向量库。

## 2. Fixed context order

Always prefer:

1. `project-summary`
2. current `task-pack`
3. 1-3 relevant `topic-card`
4. 3-6 retrieved chunks

## 3. File roles

- `project-summary`: stable repo facts and hard constraints
- `topic-card`: module-level routing and evidence status
- `task-pack`: this-task-only boundary and output contract
- `retrieval-index`: machine-readable chunk source

## 4. Maintenance rule

- 更新方向或阶段时改 `project-summary`
- 更新模块结论时改 `topic-card`
- 每个新任务新建 `task-pack`
- 文档大量变化后重建 `retrieval-index`

## 5. Common failure modes

- 把向量库当主路由，导致召回范围失控
- 没有 `task-pack`，每次都从全仓库重新开始
- 摘要写太长，反而比原文更费 token
- 不区分“已确认 / 高概率 / 待确认”
