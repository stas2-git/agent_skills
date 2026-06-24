# Agent Skill Package

This folder packages skills derived from the Kaggle Agent reference material as
one copyable skill group with a router plus focused subskills.

## Contents

- `skills/SKILL.md`: router for choosing the focused agent skill
- `skills/coding-agent-workflow`: skills for coding agents such as Codex,
  GitHub Copilot, Cursor, and similar tools
- `skills/agent-engineering`: skills for designing, packaging, evaluating, and
  debugging agent systems or reusable skills
- `skills/safety-governance`: skills for prompt injection, authority
  boundaries, approvals, and tool access
- `skills/adk-implementation`: ADK implementation, security, deployment, and
  HITL frontend skills
- `skills/capstone`: Kaggle Agent capstone planning skill

## Included Skills

Coding agent workflow:

- `spec-driven-agent-workflow`
- `agent-self-audit`
- `code-review-agent`
- `context-harness-debugger`
- `context-budget-planner`
- `agent-incident-retrospective`

Agent engineering:

- `agent-architecture-methods`
- `agent-protocol-selector`
- `agent-skill-design`
- `agent-eval-case-builder`
- `skill-evaluation-loop`
- `agent-observability-trace-review`

Safety governance:

- `prompt-injection-triage`
- `least-privilege-tool-planner`
- `human-approval-gate-designer`

ADK implementation:

- `adk-ambient-agent`
- `adk-secure-lifecycle`
- `adk-runtime-deployment`
- `adk-hitl-frontend`

Capstone:

- `kaggle-capstone-planner`

## Install

Recommended grouped install:

```bash
cp -R agent/skills /path/to/github-copilot/skills/agent
```

This installs one agent group folder with the router at:

```text
/path/to/github-copilot/skills/agent/SKILL.md
```

Focused skills remain inside that group folder, for example:

```text
/path/to/github-copilot/skills/agent/coding-agent-workflow/spec-driven-agent-workflow/SKILL.md
/path/to/github-copilot/skills/agent/agent-engineering/agent-skill-design/SKILL.md
/path/to/github-copilot/skills/agent/safety-governance/prompt-injection-triage/SKILL.md
```

For Codex, the same grouped install pattern is:

```bash
cp -R agent/skills ~/.codex/skills/agent
```

If a tool expects flat skill folders instead, copy the focused skill folders
individually from the group subfolders.

## Validate

Run the local skill checks after adding, moving, or editing agent skills:

```bash
python3 agent/skills/scripts/validate_agent_skills.py
```

The validator checks frontmatter, folder/name alignment, reference links, code
fences, eval prompt coverage, stale paths, packaging clutter, and oversized
references.
