# Agent Skills

These skills were distilled from the Kaggle Agent reference material into portable Codex skill folders.

The top-level `SKILL.md` is a router skill that helps choose which focused skill to load.

## Included

### `coding-agent-workflow/`

Skills for Codex, GitHub Copilot, Cursor, and other coding agents while they do software work.

- `spec-driven-agent-workflow`
- `agent-self-audit`
- `code-review-agent`
- `context-harness-debugger`
- `context-budget-planner`
- `agent-incident-retrospective`

### `agent-engineering/`

Skills for designing, packaging, evaluating, and debugging agent systems or reusable skills.

- `agent-architecture-methods`
- `agent-protocol-selector`
- `agent-skill-design`
- `agent-eval-case-builder`
- `skill-evaluation-loop`
- `agent-observability-trace-review`

### `safety-governance/`

Skills for authority boundaries, prompt-injection handling, approvals, and tool access.

- `prompt-injection-triage`
- `least-privilege-tool-planner`
- `human-approval-gate-designer`

### `adk-implementation/`

- `adk-ambient-agent`
- `adk-secure-lifecycle`
- `adk-runtime-deployment`
- `adk-hitl-frontend`

### `capstone/`

- `kaggle-capstone-planner`

Each skill keeps `SKILL.md` short and stores detailed source material under its own `references/` folder.

## Install

Copy selected skills into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/agent-skills-router
cp agent/skills/SKILL.md ~/.codex/skills/agent-skills-router/SKILL.md
cp -R agent/skills/coding-agent-workflow/spec-driven-agent-workflow ~/.codex/skills/
cp -R agent/skills/coding-agent-workflow/agent-self-audit ~/.codex/skills/
cp -R agent/skills/coding-agent-workflow/code-review-agent ~/.codex/skills/
cp -R agent/skills/coding-agent-workflow/context-harness-debugger ~/.codex/skills/
cp -R agent/skills/coding-agent-workflow/context-budget-planner ~/.codex/skills/
cp -R agent/skills/coding-agent-workflow/agent-incident-retrospective ~/.codex/skills/
cp -R agent/skills/agent-engineering/agent-architecture-methods ~/.codex/skills/
cp -R agent/skills/agent-engineering/agent-protocol-selector ~/.codex/skills/
cp -R agent/skills/agent-engineering/agent-skill-design ~/.codex/skills/
cp -R agent/skills/agent-engineering/agent-eval-case-builder ~/.codex/skills/
cp -R agent/skills/agent-engineering/skill-evaluation-loop ~/.codex/skills/
cp -R agent/skills/agent-engineering/agent-observability-trace-review ~/.codex/skills/
cp -R agent/skills/safety-governance/prompt-injection-triage ~/.codex/skills/
cp -R agent/skills/safety-governance/least-privilege-tool-planner ~/.codex/skills/
cp -R agent/skills/safety-governance/human-approval-gate-designer ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-ambient-agent ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-secure-lifecycle ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-runtime-deployment ~/.codex/skills/
cp -R agent/skills/adk-implementation/adk-hitl-frontend ~/.codex/skills/
cp -R agent/skills/capstone/kaggle-capstone-planner ~/.codex/skills/
```

Or install an entire group:

```bash
cp -R agent/skills/coding-agent-workflow/* ~/.codex/skills/
cp -R agent/skills/agent-engineering/* ~/.codex/skills/
cp -R agent/skills/safety-governance/* ~/.codex/skills/
```

To install the router and all focused skills:

```bash
mkdir -p ~/.codex/skills/agent-skills-router
cp agent/skills/SKILL.md ~/.codex/skills/agent-skills-router/SKILL.md
cp -R agent/skills/coding-agent-workflow/* ~/.codex/skills/
cp -R agent/skills/agent-engineering/* ~/.codex/skills/
cp -R agent/skills/safety-governance/* ~/.codex/skills/
cp -R agent/skills/adk-implementation/* ~/.codex/skills/
cp -R agent/skills/capstone/* ~/.codex/skills/
```
