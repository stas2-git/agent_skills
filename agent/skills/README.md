# Agent Skills

These skills were distilled from the Kaggle Agent reference material into
portable Codex skill folders.

The top-level `SKILL.md` is a router skill that helps choose which focused skill
to load.

## Included

### `core-methods/`

- `agent-architecture-methods`
- `agent-skill-design`
- `agent-protocol-selector`

### `self-improvement/`

- `agent-self-audit`
- `context-harness-debugger`
- `skill-evaluation-loop`
- `spec-driven-agent-workflow`

### `adk-implementation/`

- `adk-ambient-agent`
- `adk-secure-lifecycle`
- `adk-runtime-deployment`
- `adk-hitl-frontend`

### `capstone/`

- `kaggle-capstone-planner`

Each skill keeps `SKILL.md` short and stores detailed source material under its
own `references/` folder.

## Install

Copy selected skills into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/agent-skills-router
cp agent/skills/SKILL.md ~/.codex/skills/agent-skills-router/SKILL.md
cp -R agent/skills/core-methods/agent-architecture-methods ~/.codex/skills/
cp -R agent/skills/core-methods/agent-skill-design ~/.codex/skills/
cp -R agent/skills/core-methods/agent-protocol-selector ~/.codex/skills/
cp -R agent/skills/self-improvement/agent-self-audit ~/.codex/skills/
cp -R agent/skills/self-improvement/context-harness-debugger ~/.codex/skills/
cp -R agent/skills/self-improvement/skill-evaluation-loop ~/.codex/skills/
cp -R agent/skills/self-improvement/spec-driven-agent-workflow ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-ambient-agent ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-secure-lifecycle ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-runtime-deployment ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-hitl-frontend ~/.codex/skills/
cp -R agent/skills/capstone/kaggle-capstone-planner ~/.codex/skills/
```

Or install an entire group:

```bash
cp -R agent/skills/self-improvement/* ~/.codex/skills/
```

To install the router and all focused skills:

```bash
mkdir -p ~/.codex/skills/agent-skills-router
cp agent/skills/SKILL.md ~/.codex/skills/agent-skills-router/SKILL.md
cp -R agent/skills/core-methods/* ~/.codex/skills/
cp -R agent/skills/self-improvement/* ~/.codex/skills/
cp -R agent/skills/adk-implementation/* ~/.codex/skills/
cp -R agent/skills/capstone/* ~/.codex/skills/
```
