---
name: agent-skills-router
description: Use when deciding which bundled agent skill to use for agent architecture, self-improvement, skill design, ADK implementation, deployment, security, human review frontends, protocol selection, or Kaggle capstone planning.
---

# Agent Skills Router

Use this high-level skill to choose the smallest useful downstream skill. Do not treat this as a replacement for the focused skills; use it to route, then load the selected skill's `SKILL.md`.

## Routing

### Core Methods

- Use `core-methods/agent-architecture-methods` when designing an agent system, choosing single-agent versus multi-agent, defining tools/state/evals/security, or turning a vague agent idea into a buildable architecture.
- Use `core-methods/agent-skill-design` when creating, refactoring, packaging, or reviewing portable skills and deciding what belongs in `SKILL.md`, `references/`, `scripts/`, or `assets/`.
- Use `core-methods/agent-protocol-selector` when choosing between project instructions, skills, scripts, MCP, A2A, A2UI, AP2/UCP, or ordinary application code.

### Self Improvement

- Use `self-improvement/agent-self-audit` before finalizing substantial work when the agent should check its own likely weaknesses, residual risk, verification gaps, context drift, and trajectory quality.
- Use `self-improvement/context-harness-debugger` when the agent is looping, missing instructions, calling the wrong tool, hallucinating dependencies, overloading context, or otherwise needs harness/context repair.
- Use `self-improvement/skill-evaluation-loop` when testing or improving a skill with trigger tests, execution tests, token-budget checks, regression checks, red-teaming, or promotion tiers.
- Use `self-improvement/spec-driven-agent-workflow` when converting vague intent into a spec, BDD scenarios, failing tests, small diffs, policy gates, or reviewable production work.

### ADK Implementation

- Use `adk-implementation/adk-ambient-agent` when building event-driven, scheduled, Pub/Sub-style, or ambient ADK agents with normalized inputs, deterministic routing, state, traces, and HITL.
- Use `adk-implementation/adk-secure-lifecycle` when securing an ADK/tool-using agent with validation, authorization, guardrails, hooks, secret scanning, STRIDE, human gates, tests, and behavioral evals.
- Use `adk-implementation/adk-runtime-deployment` when packaging, testing, deploying, monitoring, or rolling back an ADK agent on Google Agent Runtime with Agents CLI, Terraform, IAM, artifacts, telemetry, and remote validation.
- Use `adk-implementation/adk-hitl-frontend` when building a human-in-the-loop frontend for pending approvals, event correlation, session resume, function responses, dashboards, auth, audit, Cloud Run, or Pub/Sub wiring.

### Capstone

- Use `capstone/kaggle-capstone-planner` when planning, scoping, validating, or preparing a Kaggle Agent capstone submission, writeup, demo, local evaluation, track choice, or compliance review.

## Combination Patterns

- New production agent idea: start with `agent-architecture-methods`, then `spec-driven-agent-workflow`, then the relevant ADK implementation skill.
- Agent behaving badly: start with `agent-self-audit`; if the issue repeats, use `context-harness-debugger`; if a skill is involved, use `skill-evaluation-loop`.
- New skill from reference material: use `agent-skill-design`, then `skill-evaluation-loop`.
- Tool/protocol confusion: use `agent-protocol-selector`, then route to MCP/A2A/A2UI/ADK implementation work as appropriate.
- Capstone build: start with `kaggle-capstone-planner`, then `agent-architecture-methods`, then `adk-secure-lifecycle` and `adk-runtime-deployment` when implementation matures.

## Rules

- Prefer the most specific skill that matches the current task.
- Load only one or two focused skills unless the task genuinely crosses boundaries.
- If no focused skill matches, proceed without forcing one.
- If the selected skill has references, load only the references relevant to the immediate task.

