# Agent Skills

Project workspace for developing and organizing agent skills.

The root [AGENTS.md](AGENTS.md) defines the always-on behavior for this repo:
use the skill router, self-audit substantial work, and think in evals when skills
change.

## Skill Packages

The `agent-skills/` folder is the copyable agent skill package. It has the router at
`agent-skills/SKILL.md`, with focused skills directly underneath it for coding-agent
workflow, agent engineering, safety governance, ADK implementation, and capstone
planning.

The `excel-skills/` folder is the copyable Excel/workbook skill package. It has
the router at `excel-skills/SKILL.md`, with focused skills underneath it for
spreadsheet artifacts, workbook decomposition, deterministic workbook edits,
live Excel automation, VBA/macros, workbook pipelines, and screen interaction.

Copy the whole folder into a skills library.

Agent skills:

```bash
cp -R agent-skills /path/to/skills-library/agent-skills
```

Excel skills:

```bash
cp -R excel-skills /path/to/skills-library/excel-skills
```

For Codex, that looks like:

```bash
cp -R agent-skills ~/.codex/skills/agent-skills
cp -R excel-skills ~/.codex/skills/excel-skills
```

After install, the routers should be at:

```text
/path/to/skills-library/agent-skills/SKILL.md
/path/to/skills-library/excel-skills/SKILL.md
```

## Reference Material

The `reference-material/` folder contains the copied Kaggle Agent reference
material, including source PDFs/RTFs, codelabs, extracted text, and
implementation specs.
