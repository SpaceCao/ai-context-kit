# AI Context Kit

`AI Context Kit` is a reusable, low-token context strategy for design-phase AI work.

It helps you avoid the common failure mode of sending an entire repository, PRD, or long design document to an LLM on every turn. Instead, it organizes context into small, stable layers and retrieves only what is needed for the current task.

This repository includes:

- a portable `.ai-context/` scaffold for any project
- a reusable Codex skill at `skills/design-token-context/`
- templates for project summaries, topic cards, task packs, and retrieval indexes

Repository:

- `https://github.com/SpaceCao/ai-context-kit`

---

## Why this exists

Most AI coding and design workflows waste tokens in predictable ways:

- the model re-reads the same project background in every conversation
- large design documents are pasted in full even when only one section matters
- semantic retrieval is added too early, without task boundaries or routing
- tools like Claude Code, Gemini, Cursor, or ChatGPT are allowed to over-read the repo

`AI Context Kit` solves this by separating:

1. stable project context
2. topic-level context
3. task-specific context
4. evidence-level retrieval

The result is lower token usage, cleaner prompts, and more predictable outputs.

---

## Core model

The recommended context stack has four layers:

1. `Project Summary`  
   Stable project background, constraints, structure, and must-read entry points.

2. `Topic Card`  
   A compact summary for one module, capability, or workstream.

3. `Task Pack`  
   A single-task brief that defines what to read, what not to read, and what “done” means.

4. `Retrieved Chunks`  
   A few evidence snippets added only when the higher layers are insufficient.

This is the key principle of the repository:

> Route first, summarize second, retrieve third.

Do not start with full-repo reading.  
Do not start with vector search unless recall quality actually requires it.

---

## When to use this

This kit is especially useful for:

- product design and PRD drafting
- technical design and architecture writing
- reconstruction or migration planning
- RFP and procurement preparation
- document-heavy engineering repos
- mixed code-and-doc repos where context is expensive

It is less useful for:

- very small repos with only a few short files
- narrow coding tasks that only touch one or two files
- purely conversational or brainstorming sessions with no project memory

---

## When to use a vector database

Do not assume a vector database is required.

| Scenario | Recommended strategy |
|----------|----------------------|
| Fewer than 20 documents, clear structure | directory routing + keyword search + summaries |
| 20-200 documents, cross-module work | metadata filtering + keyword/BM25 + optional vectors |
| 200+ documents, many PDFs, semantic queries | hybrid retrieval with vectors becomes worthwhile |

Recommended retrieval order:

`metadata filter -> keyword/BM25 -> vector search (optional) -> rerank -> top 3-6 chunks`

The vector database is an accelerator, not the architecture.

---

## What is included

### `.ai-context/`

The reusable scaffold contains:

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

The repository also ships a Codex skill with:

- a reusable `SKILL.md`
- a scaffold script
- bundled template assets
- a short playbook for retrieval decisions

---

## Quick start

### Option A: Copy the scaffold into a project

1. Copy `.ai-context/` into your target repository
2. Rename the templates into working files such as:
   - `project-summary.md`
   - `topic-card-<topic>.md`
   - `task-pack-<task>.md`
   - `prompt.md`
   - `retrieval-index.json`
3. Fill `project-summary.md` first
4. Create one `task-pack` per task
5. Add `topic-card` files only for active modules

### Option B: Use the Codex skill

If the skill is installed under `~/.codex/skills/design-token-context/`, run:

```bash
python3 ~/.codex/skills/design-token-context/scripts/scaffold_ai_context.py --target /path/to/repo
```

This will create `.ai-context/` in the target repository.

---

## Recommended workflow

### Step 1: Write `project-summary`

Keep it short and stable. A good summary usually contains:

- project name and objective
- current phase
- directory routing
- key constraints
- must-read documents
- topics that are explicitly out of scope

Recommended size: `500-1200` tokens.

### Step 2: Create `topic-card` files

Each topic card should cover one topic only:

- confirmed facts
- high-probability assumptions
- open questions
- relevant files
- search keywords
- boundary with adjacent topics

Recommended size: `200-500` tokens per card.

### Step 3: Create one `task-pack` per task

This is the most important file in the kit.

A good `task-pack` defines:

- what the current task is
- what “done” means
- which files are required
- which files should not be read
- which keywords or filters should be used for retrieval

Recommended size: `200-600` tokens.

### Step 4: Retrieve only when needed

If the model cannot complete the task from summary layers alone, add:

- `3-6` relevant chunks
- not full documents
- not broad “read the repo” instructions

---

## How to use with different tools

### Codex

Best fit:

- repo-aware workflows
- local coding tasks
- repeated use across many repositories

Recommended input order:

1. `project-summary`
2. current `task-pack`
3. `topic-card` files
4. retrieved chunks if needed

### Claude Code

Best fit:

- design reasoning
- refactoring plans
- structured drafts
- task-specific implementation support

Recommended usage:

- prepare `.ai-context/` in the target repo
- direct Claude Code to read only the relevant `.ai-context` files first
- avoid letting it scan the entire repository by default

Suggested prompt:

```text
Use only the provided project-summary, task-pack, topic-card files, and a few evidence chunks if needed.

Do not read the entire repository by default.
Classify conclusions as: confirmed / high-probability / unknown.
If the current context is insufficient, return retrieval suggestions first.
```

### Gemini

Best fit:

- comparison writing
- structured synthesis
- outline generation
- risk and gap analysis

Recommended usage:

- provide `.ai-context` content in order
- do not start with full PRDs or full repo trees
- use Gemini to compress, compare, and structure before deep retrieval

Suggested prompt:

```text
Work only from the provided project-summary, task-pack, topic-cards, and a small set of evidence snippets.

Do not ask to read the entire repository unless the current context is insufficient.
If evidence is missing, suggest which keywords or files should be retrieved next.
```

### Cursor

Best fit:

- codebase navigation
- file-local editing
- light design support inside an editor workflow

Recommended usage:

- keep `.ai-context/` inside the repository
- pin or open `project-summary.md` and the active `task-pack`
- use topic cards to constrain editor-side context expansion

### ChatGPT

Best fit:

- manual review
- lightweight planning
- public-web workflow without repo integration

Recommended usage:

- paste only the minimal `.ai-context` layers
- add retrieved chunks only after the first answer exposes a gap

---

## Minimal prompt pattern

For most tools, this prompt pattern is enough:

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

## Practical guidance

### Do

- keep summaries short
- use one task pack per task
- route by module before retrieval
- retrieve a few chunks, not full documents
- separate confirmed facts from assumptions

### Do not

- paste an entire PRD into every chat
- ask the model to “read the whole repo” as a first step
- treat vector search as the first or only routing layer
- let one summary file grow into another long document

---

## Suggested repository usage

If you want to use this repository as a public starter kit:

- copy `.ai-context/` into each target repository
- install or reuse the Codex skill from `skills/design-token-context/`
- standardize your team on the same four-layer context model
- add retrieval only after the summary-first workflow is stable

---

## Repository structure

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

## Next steps

Common extensions after adopting this kit:

- add a generator for `project-summary` first drafts
- add a generator for `topic-card` drafts from existing docs
- add a retrieval index builder for larger repositories
- add team conventions for naming and evidence levels

If you only adopt one idea from this repository, make it this:

> Give the model the smallest context that can still complete the current task correctly.
