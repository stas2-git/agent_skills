# Day 5: Spec-Driven Production Development

## Core Thesis

"Vibe coding" is not "vibe-in-production." Generated code can be disposable, but specs, tests, guardrails, and review records become the source of truth. As agents increase output speed, the bottleneck moves to review, integration, safety, and maintainability.

The production answer is not to slow agents down; it is to make work spec-driven, test-backed, reviewable, and gated by policy.

## Agent Weaknesses And Failure Modes

- Illusion of speed: large AI-generated diffs create review gridlock and integration risk.
- Vague specs make the agent guess, then make reviewers reverse-engineer intent.
- Huge pull requests increase merge conflicts and hide subtle security or architecture mistakes.
- Approval fatigue makes human gates weaker over time.
- Browser or desktop agents can act on hallucinated context if not constrained.
- Context fragmentation causes agents to miss requirements, hardcode assumptions, leak PII, or duplicate work.
- A passing demo can conceal missing tests, weak rollback, or production-incompatible design.

## Durable Patterns

- Keep specs as durable source of truth, commonly in `/specs`, with Markdown for narrative and YAML for structured constraints.
- Use BDD-style acceptance criteria: Given, When, Then.
- Work in small diffs with clear intent, risk notes, and verification evidence.
- Use explicit modes: Architect, Builder, Forensic specialist, Author, and Librarian.
- Before fixing a bug, capture a failing unit test or reproduction command.
- Use agent-generated PR summaries, risk assessments, test suggestions, and conditional review comments.
- Add policy gates that combine structural checks with semantic checks.
- Use sandboxing and human-in-the-loop review for external writes, production actions, and risky changes.
- Use context resolvers and placeholders to avoid hardcoding sensitive or environment-specific data.
- Treat review and integration as first-class workflow steps, not cleanup after generation.

## Skill Extraction Opportunities

| Skill idea | Trigger | What it should teach |
|---|---|---|
| `spec-driven-agent-workflow` | Turning vague work into production-ready changes | Create specs, BDD scenarios, failing tests, small diffs, and review evidence. |
| `agent-self-audit` | Before shipping or handing off work | Check intent, tests, risk, reviewability, and residual uncertainty. |
| `adk-secure-lifecycle` | Productionizing a tool-using or autonomous agent | Add policy gates, sandboxing, approvals, and audit records. |
| Future `code-review-agent` | Reviewing AI-generated diffs | Prioritize risks, correctness, tests, security, and maintainability. |
| `context-harness-debugger` | Agent misses requirements or hardcodes assumptions | Diagnose context fragmentation, stale assumptions, and missing environment contracts. |

## Reference Use

Use this summary when building production workflow habits into skills or agent behavior. Read the full whitepaper when you need the original framing around spec storage, BDD, review agents, policy servers, or production delivery patterns.

