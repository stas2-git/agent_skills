# Day 3: Agent Skills

## Core Thesis

Skills are portable procedural memory. They let an agent load specialized know-how only when relevant, reducing context rot while making repeated workflows reusable across projects and agents.

A good skill is not a motivational document. It changes behavior by giving the agent a clear trigger, a focused procedure, and optional references, scripts, or assets that load progressively.

## Agent Weaknesses And Failure Modes

- Trigger failure: the skill is not selected when it should be, or it is selected for the wrong task.
- Execution failure: the skill triggers but does not provide enough operational guidance.
- Token-budget failure: `SKILL.md` or references are too bulky, so important context is crowded out.
- Regression: improving one skill makes another skill route or perform worse.
- Vague descriptions behave like weak classifiers and make routing unreliable.
- Single-skill tests can be misleading because real sessions often load multiple skills and project instructions.
- Meta-skills can become gimmicky if they only tell the agent to "be better" without changing concrete actions.

## Durable Patterns

- Use progressive disclosure: metadata first, then `SKILL.md`, then only the relevant references, scripts, and assets.
- Treat the description as the routing interface. It should be specific enough to include positive use cases and exclude nearby non-use cases.
- Keep one skill to one job. Split skills when the trigger or procedure becomes multi-purpose.
- Put durable procedure in `SKILL.md`, long background in `references/`, deterministic repeated logic in `scripts/`, and reusable deliverables in `assets/`.
- Evaluate skills with trigger tests, execution tests, token-budget checks, and regression prompts.
- Use positive and negative prompts: should trigger, should trigger with an edge case, and should not trigger.
- For complex systems, compose skills through clear file outputs, capability profiles, or DAG-like handoffs instead of hidden assumptions.
- Treat installed skills as dependencies: audit them, pin them, and be cautious with untrusted code or instructions.

## Skill Extraction Opportunities

| Skill idea | Trigger | What it should teach |
|---|---|---|
| `agent-skill-design` | Creating, reviewing, or refactoring a skill | Scope one job, write routing metadata, choose refs/scripts/assets, and define validation prompts. |
| `skill-evaluation-loop` | Testing or improving a skill | Run trigger, execution, token-budget, regression, and red-team checks. |
| `context-harness-debugger` | Skill routing fails or context becomes noisy | Diagnose context loading, conflicting instructions, and skill selection boundaries. |
| `agent-skills-router` | Selecting among bundled skills | Route to the smallest focused skill and avoid loading irrelevant material. |

## Reference Use

Use this summary when building or refactoring skills, especially when shortening references and improving routing. Read the full whitepaper when you need the original discussion of progressive disclosure, eval design, skill tiers, composition, or security implications.

