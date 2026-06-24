# Agent Skills

Project workspace for developing and organizing agent skills.

The root [AGENTS.md](AGENTS.md) defines the always-on behavior for this repo:
use the skill router, self-audit substantial work, and think in evals when skills
change.

## Skills Library

The `skills-library/` folder contains the copyable skill packages. Copy its
contents into another machine's skills library, or copy individual package
folders from inside it.

```bash
cp -R skills-library/* /path/to/skills-library/
```

The `skills-library/agent-skills/` folder is the agent skill package. It has the router at
`skills-library/agent-skills/SKILL.md`, with focused skills directly underneath it for coding-agent
workflow, agent engineering, safety governance, ADK implementation, and capstone
planning.

The `skills-library/excel-skills/` folder is the Excel/workbook skill package. It has
the router at `skills-library/excel-skills/SKILL.md`, with focused skills underneath it for
spreadsheet artifacts, workbook decomposition, deterministic workbook edits,
live Excel automation, VBA/macros, workbook pipelines, and screen interaction.

The `skills-library/sql-skills/` folder is the SQL skill package. It has the router at
`skills-library/sql-skills/SKILL.md`, with focused skills underneath it for actuarial SQL
query writing/review and safe ODBC-backed database exploration/execution.

To install package folders individually:

Agent skills:

```bash
cp -R skills-library/agent-skills /path/to/skills-library/agent-skills
```

Excel skills:

```bash
cp -R skills-library/excel-skills /path/to/skills-library/excel-skills
```

SQL skills:

```bash
cp -R skills-library/sql-skills /path/to/skills-library/sql-skills
```

For Codex, that looks like:

```bash
cp -R skills-library/agent-skills ~/.codex/skills/agent-skills
cp -R skills-library/excel-skills ~/.codex/skills/excel-skills
cp -R skills-library/sql-skills ~/.codex/skills/sql-skills
```

After install, the routers should be at:

```text
/path/to/skills-library/agent-skills/SKILL.md
/path/to/skills-library/excel-skills/SKILL.md
/path/to/skills-library/sql-skills/SKILL.md
```

## Reference Material

The `reference-material/` folder contains the copied Kaggle Agent reference
material, including source PDFs/RTFs, codelabs, extracted text, and
implementation specs.
