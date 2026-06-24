# Agent Skills

These skills were distilled from the Kaggle Agent reference material into
portable Codex skill folders.

The top-level `SKILL.md` is a router skill that helps choose which focused skill
to load.

## Included

### `core-methods/`

- `agent-architecture-methods`
- `code-review-agent`
- `agent-skill-design`
- `agent-protocol-selector`

### `self-improvement/`

- `agent-self-audit`
- `agent-incident-retrospective`
- `agent-observability-trace-review`
- `agent-eval-case-builder`
- `context-harness-debugger`
- `context-budget-planner`
- `prompt-injection-triage`
- `least-privilege-tool-planner`
- `human-approval-gate-designer`
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
cp -R agent/skills/core-methods/code-review-agent ~/.codex/skills/
cp -R agent/skills/core-methods/agent-skill-design ~/.codex/skills/
cp -R agent/skills/core-methods/agent-protocol-selector ~/.codex/skills/
cp -R agent/skills/self-improvement/agent-self-audit ~/.codex/skills/
cp -R agent/skills/self-improvement/agent-incident-retrospective ~/.codex/skills/
cp -R agent/skills/self-improvement/agent-observability-trace-review ~/.codex/skills/
cp -R agent/skills/self-improvement/agent-eval-case-builder ~/.codex/skills/
cp -R agent/skills/self-improvement/context-harness-debugger ~/.codex/skills/
cp -R agent/skills/self-improvement/context-budget-planner ~/.codex/skills/
cp -R agent/skills/self-improvement/prompt-injection-triage ~/.codex/skills/
cp -R agent/skills/self-improvement/least-privilege-tool-planner ~/.codex/skills/
cp -R agent/skills/self-improvement/human-approval-gate-designer ~/.codex/skills/
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
