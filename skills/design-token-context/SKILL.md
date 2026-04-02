---
name: design-token-context
description: Scaffold and use a low-token design-context workflow for local AI coding projects. Use when Codex needs to reduce prompt/context cost during product design, technical design, reconstruction planning, RFP preparation, or document-heavy repo analysis; especially when the user mentions token usage, context bloat, vector databases, RAG, project summaries, topic cards, task packs, or wants a reusable `.ai-context` scaffold.
---

# Design Token Context

Use this skill to keep design work out of the “read the whole repo again” trap.

The default pattern is:

1. Route by project phase and module
2. Feed a short `project-summary`
3. Feed 1-3 `topic-card` files
4. Feed one `task-pack`
5. Add only a few retrieved chunks when evidence is still missing

## Workflow

### 1. Choose the retrieval mode

- Skip vector search for small, well-structured repos
- Use metadata + keyword/BM25 first for most repos
- Add vector search only when semantic recall is genuinely missing

Read `references/playbook.md` when you need the decision table.

### 2. Scaffold `.ai-context`

Run:

```bash
python3 scripts/scaffold_ai_context.py --target /path/to/repo
```

Use `--force` only when the user explicitly wants to overwrite existing files.

This copies the bundled templates from `assets/ai-context/`.

### 3. Fill the minimum files first

Start with:

- `project-summary.md`
- one `task-pack-*.md`
- one or more `topic-card-*.md`

Do not build a retrieval index first unless the repo is already too large for manual routing.

### 4. Run design work with bounded context

Prompt the model with:

1. `project-summary`
2. current `task-pack`
3. selected `topic-card`
4. optional retrieved chunks

If evidence is insufficient, ask for more retrieval inputs instead of loading whole documents.

### 5. Add retrieval index only when needed

Use `assets/ai-context/retrieval-index.template.json` as the schema seed.

Prefer the sequence:

`metadata filter -> keyword/BM25 -> vector(optional) -> rerank`

## Resources

### `scripts/scaffold_ai_context.py`

Copy the scaffold into a target repo.

### `references/playbook.md`

Read this when you need the decision matrix for “no vector / hybrid / vector”.

### `assets/ai-context/*`

Copy-ready templates for:

- `project-summary`
- `topic-card`
- `task-pack`
- prompt wrapper
- retrieval index seed
