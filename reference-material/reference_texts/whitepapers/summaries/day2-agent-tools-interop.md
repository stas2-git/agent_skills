# Day 2: Agent Tools And Interoperability

## Core Thesis

Useful agents need ways to reach tools, delegate work, present interfaces, and conduct transactions without bespoke glue for every integration. Protocols reduce integration debt and make agent systems composable.

The main protocol roles are different: MCP extends tool and data reach, Skills package procedural know-how, A2A lets specialist agents collaborate, A2UI lets agents request safe user interfaces, and AP2/UCP handle trustworthy commerce and payments.

## Agent Weaknesses And Failure Modes

- Too many tools can expand the action search space and increase wrong-tool calls.
- Bespoke wrappers create an `N x M` maintenance problem between agents and external systems.
- Public or unvetted MCP servers can expose credentials, prompt-injection surfaces, or unsafe actions.
- Treating an unbounded specialist agent like a simple tool can create hard-to-debug control flow.
- Generated UI code can create security and review risk when a declarative UI contract would be safer.
- Commerce flows need explicit mandates, authorization, and auditability; ordinary prompt approval is not enough.

## Durable Patterns

- Choose the protocol by responsibility: tool access, procedural skill, agent collaboration, user interface, or transaction authority.
- Prefer official, managed, or internally reviewed MCP servers; scope credentials tightly and start read-only when possible.
- Use A2A when another agent owns a multi-turn or open-ended responsibility, not when a deterministic function call is enough.
- Describe specialist agents with discoverable agent cards: capabilities, inputs, outputs, constraints, and auth.
- Use declarative A2UI-style contracts for user-facing interaction instead of letting agents emit arbitrary frontend code.
- Combine data and UI outputs when the user needs both machine-readable state and human confirmation.
- Audit protocol boundaries as part of the agent architecture, not as an afterthought.

## Skill Extraction Opportunities

| Skill idea | Trigger | What it should teach |
|---|---|---|
| `agent-protocol-selector` | Deciding between instructions, skills, scripts, MCP, A2A, A2UI, or application code | Select the smallest protocol that matches responsibility and risk. |
| `agent-architecture-methods` | Designing multi-tool or multi-agent systems | Make tool boundaries, delegation contracts, state, and eval surfaces explicit. |
| `adk-hitl-frontend` | Building approval or review UI | Use structured pending actions, session correlation, and declarative review surfaces. |
| `adk-secure-lifecycle` | Connecting agents to external tools or credentials | Apply least privilege, review gates, logging, and tool governance. |

## Reference Use

Use this summary when a skill or agent needs a protocol choice, tool governance, or integration boundary. Read the full whitepaper when you need deeper protocol descriptions or examples for MCP, A2A, A2UI, AP2, or UCP.

