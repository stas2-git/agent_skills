# Day 4: Security And Evaluation

## Core Thesis

Security answers whether an agent stayed inside the allowed boundary. Evaluation answers whether the in-boundary result is good enough to ship. Agentic systems need both: a safety harness and a quality framework.

Final output is not enough. The trajectory matters: which tools were called, what data was exposed, whether the agent respected approvals, and how it recovered from errors.

## Agent Weaknesses And Failure Modes

- Ambient authority: the agent inherits broad access it does not need.
- Confused deputy behavior: the agent uses legitimate tools for unintended user or attacker goals.
- Prompt injection and context poisoning through web pages, files, emails, tickets, or tool outputs.
- Invisible or indirect payloads hidden in external content or retrieved context.
- Hallucinated packages and dependency confusion, including typosquatting or slopsquatting.
- Frontend/backend authorization mismatches where generated UI implies permissions the backend does not enforce.
- Denial-of-wallet loops from repeated expensive calls, tool loops, or runaway retries.
- Intent drift and trust decay when agents optimize for plausible completion instead of the user's actual boundary.
- Underspecification gap: users may not know enough to validate generated code or agent behavior.

## Durable Patterns

- Build around least privilege: no ambient authority, scoped credentials, just-in-time access, and explicit user approvals for risky actions.
- Use a layered security architecture: infrastructure and network, data, model, application/runtime, IAM, observability/SecOps, and governance.
- Sandbox agent work, especially code execution, dependency installation, browser use, filesystem edits, and external writes.
- Treat tool outputs and retrieved documents as untrusted input.
- Use dependency controls: approved registries, lockfiles, SBOMs, vulnerability scans, and package review.
- Add observability: traces, tool-call logs, approval records, cost monitoring, checkpoints, and circuit breakers.
- Evaluate multiple dimensions: intent alignment, functional correctness, visual/behavioral quality, cost, code quality, trajectory, and self-repair.
- Combine tests, scanners, LLM-as-judge, browser checks, trajectory inspection, human review, online evals, and benchmark suites.
- Mine user corrections and production failures into future eval cases.

## Skill Extraction Opportunities

| Skill idea | Trigger | What it should teach |
|---|---|---|
| `agent-self-audit` | Before final delivery or after risky autonomous work | Check boundary compliance, verification evidence, trajectory, and residual risk. |
| `adk-secure-lifecycle` | Securing an ADK or tool-using agent | Add validation, auth, callbacks, human gates, tests, and security controls. |
| `skill-evaluation-loop` | Measuring agent or skill quality | Evaluate both outputs and trajectories, then turn failures into regression cases. |
| `context-harness-debugger` | Prompt injection, tool misuse, or runaway behavior appears | Inspect inputs, permissions, traces, retry loops, and context boundaries. |
| `spec-driven-agent-workflow` | Production work needs reviewable gates | Convert vague goals into specs, tests, security checks, and approval points. |

## Reference Use

Use this summary when strengthening security, evals, observability, or self-audit behavior. Read the full whitepaper when you need detailed security architecture, red/blue/green teaming ideas, or broader evaluation methodology.

