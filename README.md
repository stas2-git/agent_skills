# Agent Skills

Project workspace for developing and organizing agent skills.

The root [AGENTS.md](AGENTS.md) defines the always-on behavior for this repo:
use the skill router, self-audit substantial work, and think in evals when skills
change.

## Excel Package

This repo vendors the Excel/workbook-related Codex skills as a portable package
so they can be moved to another machine through Git.

See [excel/README.md](excel/README.md) for the package overview and
install notes.

## Agent Package

The `agent/` folder is the copyable agent skill package. It has the router at
`agent/SKILL.md`, with focused skills directly underneath it for coding-agent
workflow, agent engineering, safety governance, ADK implementation, and capstone
planning.

Copy the whole folder into a skills library:

```bash
cp -R agent /path/to/skills-library/agent
```

For Codex, that looks like:

```bash
cp -R agent ~/.codex/skills/agent
```

After install, the router should be at:

```text
/path/to/skills-library/agent/SKILL.md
```

## Reference Material

The `reference-material/` folder contains the copied Kaggle Agent reference
material, including source PDFs/RTFs, codelabs, extracted text, and
implementation specs.
