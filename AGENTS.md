# Agent Skills Project Instructions

This repo is a portable skill library. Treat the skills as the primary product.

## Default Behavior

- When a task touches agent design, skill design, ADK, capstone work, protocol choice, deployment, security, or agent self-improvement, first consult `agent-skills/SKILL.md` as the router.
- After the router selects a focused skill, read that focused skill's `SKILL.md` before editing or advising.
- Load reference files only when the focused skill says they are relevant to the immediate task.
- For Excel/workbook work, use the skills under `excel-skills/`.
- For SQL work in an actuarial or insurance context, first consult `sql-skills/SKILL.md` as the router.

## Automatic Self-Improvement Habits

- Before finishing substantial work, run a lightweight self-audit using the ideas in `agent-skills/coding-agent-workflow/agent-self-audit/SKILL.md`: intent, verification, trajectory, context drift, security risk, and residual risk.
- When a skill is changed, think in eval terms: what prompts should trigger it, what prompts should not trigger it, and what behavior proves success?
- After editing agent skills, run `python3 agent-skills/scripts/validate_agent_skills.py`.
- After editing Excel skills, run `python3 excel-skills/scripts/validate_excel_skills.py`.
- After editing SQL skills, run `python3 sql-skills/scripts/validate_sql_skills.py`.
- If a skill or agent behavior feels unreliable, prefer diagnosing the harness/context/tooling problem over adding more generic instructions.
- For vague build requests, convert the request into a small spec or checklist before implementation.

## Skill Quality Bar

- One skill, one job.
- Keep `SKILL.md` short and procedural.
- Put long knowledge in `references/`, deterministic repeated logic in `scripts/`, and reusable output material in `assets/`.
- Avoid broad, motivational, or gimmicky instructions. A good skill changes what the agent does.
- Prefer edits that make routing sharper, behavior more verifiable, or references easier to load selectively.
