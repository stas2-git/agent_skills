# Day 1: Vibe Coding Introduction

## Core Thesis

Software development is moving from syntax-first implementation toward intent-driven orchestration. The practical craft is not "let the model write everything"; it is converting goals into context, specs, tests, feedback loops, and guardrails that let an agentic harness do useful work safely.

An agent should be treated as a model plus its harness: instructions, context, tools, sandbox, orchestration, guardrails, hooks, memory, and observability. When an agent fails, the cause is often the harness or context design, not only the model.

## Agent Weaknesses And Failure Modes

- The "80% problem": agents quickly produce plausible bulk work, then miss edge cases, architecture constraints, or subtle correctness.
- Context rot: long prompts and stale project history degrade performance when they are used as a substitute for selective context.
- Vague intent creates hidden operating costs: review burden, maintenance debt, security risk, and confused tool use.
- Agents can hallucinate dependencies, APIs, imports, paths, or environmental assumptions when context is incomplete.
- Developers may blame the model when the real issue is missing tests, unclear specs, bad tool affordances, or weak verification.
- Generation speed can outpace human judgment, making review and integration the bottleneck.

## Durable Patterns

- Treat context as an engineered input, with static rules for stable behavior and dynamic retrieval for task-specific detail.
- Use a harness view: model, instructions, tools, sandbox, memory, planning, guardrails, hooks, and traces all shape behavior.
- Prefer small specs, tests, and evals over large motivational prompts.
- Make the developer a conductor: set direction, provide constraints, review outcomes, and tighten feedback loops.
- Use a factory model: intent becomes specs, specs drive agents, agents produce diffs, tests and evals produce feedback, and guardrails decide what can ship.
- Separate generation from verification. The agent can draft rapidly, but correctness still needs tests, review, and domain judgment.
- Route work by cost and risk: cheap models for routine work, stronger models for planning, ambiguity, architecture, or hard debugging.

## Skill Extraction Opportunities

| Skill idea | Trigger | What it should teach |
|---|---|---|
| `agent-self-audit` | Before finalizing substantial agent work | Check intent alignment, verification, trajectory quality, context drift, and residual risk. |
| `context-harness-debugger` | Agent loops, calls wrong tools, misses instructions, or hallucinates dependencies | Diagnose the harness: context, tools, instructions, permissions, traces, and feedback loops. |
| `spec-driven-agent-workflow` | User gives vague build intent | Convert intent into a small spec, acceptance checks, and a reviewable implementation path. |
| `agent-architecture-methods` | Designing an agent system | Make model, harness, memory, tools, evals, and guardrails explicit. |

## Reference Use

Use this summary when improving agent behavior, self-audit habits, context strategy, or harness diagnosis. Read the full whitepaper when you need the original framing around the economics of coding agents, developer role changes, or broad "software factory" narrative.

