---
name: agent-skills-router
description: Use when deciding which bundled agent skill to use for agent architecture, self-improvement, skill design, ADK implementation, deployment, security, human review frontends, protocol selection, or Kaggle capstone planning.
---

# Agent Skills Router

Use this high-level skill to choose the smallest useful downstream skill. Do not treat this as a replacement for the focused skills; use it to route, then load the selected skill's `SKILL.md`.

## How To Route

1. Identify the user's actual task type.
2. Pick the smallest matching focused skill.
3. Name the exact focused skill and, when working inside this repo, its repo path.
4. If the package has been installed into `~/.codex/skills/`, focused skills usually live by skill name, such as `agent-skill-design`, not by grouped repo path.
5. Load the focused skill's `SKILL.md` before acting.

Do not use this router as the operational instructions for the task after a focused skill matches.

## Routing

### Core Methods

- Use `agent-architecture-methods` (`core-methods/agent-architecture-methods` in this repo) when designing an agent system, choosing single-agent versus multi-agent, defining tools/state/evals/security, or turning a vague agent idea into a buildable architecture.
- Use `agent-skill-design` (`core-methods/agent-skill-design` in this repo) when creating, refactoring, packaging, or reviewing portable skills and deciding what belongs in `SKILL.md`, `references/`, `scripts/`, or `assets/`.
- Use `agent-protocol-selector` (`core-methods/agent-protocol-selector` in this repo) when choosing between project instructions, skills, scripts, MCP, A2A, A2UI, AP2/UCP, or ordinary application code.

### Self Improvement

- Use `agent-self-audit` (`self-improvement/agent-self-audit` in this repo) before finalizing substantial work when the agent should check its own likely weaknesses, residual risk, verification gaps, context drift, and trajectory quality.
- Use `context-harness-debugger` (`self-improvement/context-harness-debugger` in this repo) when the agent is looping, missing instructions, calling the wrong tool, hallucinating dependencies, overloading context, or otherwise needs harness/context repair.
- Use `skill-evaluation-loop` (`self-improvement/skill-evaluation-loop` in this repo) when testing or improving a skill with trigger tests, execution tests, token-budget checks, regression checks, red-teaming, or promotion tiers.
- Use `spec-driven-agent-workflow` (`self-improvement/spec-driven-agent-workflow` in this repo) when converting vague intent into a spec, BDD scenarios, failing tests, small diffs, policy gates, or reviewable production work.

### ADK Implementation

- Use `adk-ambient-agent` (`adk-implementation/adk-ambient-agent` in this repo) when building event-driven, scheduled, Pub/Sub-style, or ambient ADK agents with normalized inputs, deterministic routing, state, traces, and HITL.
- Use `adk-secure-lifecycle` (`adk-implementation/adk-secure-lifecycle` in this repo) when securing an ADK/tool-using agent with validation, authorization, guardrails, hooks, secret scanning, STRIDE, human gates, tests, and behavioral evals.
- Use `adk-runtime-deployment` (`adk-implementation/adk-runtime-deployment` in this repo) when packaging, testing, deploying, monitoring, or rolling back an ADK agent on Google Agent Runtime with Agents CLI, Terraform, IAM, artifacts, telemetry, and remote validation.
- Use `adk-hitl-frontend` (`adk-implementation/adk-hitl-frontend` in this repo) when building a human-in-the-loop frontend for pending approvals, event correlation, session resume, function responses, dashboards, auth, audit, Cloud Run, or Pub/Sub wiring.

### Capstone

- Use `kaggle-capstone-planner` (`capstone/kaggle-capstone-planner` in this repo) when planning, scoping, validating, or preparing a Kaggle Agent capstone submission, writeup, demo, local evaluation, track choice, or compliance review.

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

## Evaluation Prompts

Use these prompts to test routing behavior:

- Positive: "Help me decide whether this should be an MCP server, a skill, or an A2A agent." Expected: `agent-protocol-selector`.
- Positive: "My agent keeps calling the wrong tool and looping after long context." Expected: `context-harness-debugger`.
- Positive: "Plan my Kaggle Agent capstone submission and evaluation checklist." Expected: `kaggle-capstone-planner`.
- Negative: "Edit this CSS button color." Expected: no bundled agent skill unless the task expands into architecture, workflow, or evaluation.
- Negative: "Deploy this ordinary static website." Expected: no ADK deployment skill unless it is an ADK/Agent Runtime deployment.
- Negative: "Summarize this unrelated PDF." Expected: no bundled agent skill unless the summary is for capstone, architecture, or skill creation.
