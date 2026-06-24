# Workbook Action Executor Improvement Plan

## Purpose

This plan captures the next round of improvements for `workbook-action-executor` based on real test feedback.

The goal is to make the skill more likely to be chosen over ad hoc `openpyxl` scripting for:

- building new workbook tabs and sections
- structured workbook refactors
- presentation cleanup and polish
- repeatable formatting workflows

## Current Read

What is working well:

- The skill is now being used successfully for structured workbook-building tasks.
- Audit artifacts and run logs are strong.
- Managed backup behavior is useful and low-friction.
- `run-plan` is good enough to support real multi-step edits.

What is still weak:

- Presentation cleanup still often feels easier in direct `openpyxl`.
- Style payloads are too finicky inside `run-plan`.
- Formatting actions are still too contiguous-range oriented.
- Workbook- and sheet-level display polish is underpowered.
- The skill is better at deterministic mechanics than “make this sheet look good.”

## Product Goal

Make `workbook-action-executor` the default execution path when the user asks to:

- add a summary tab
- reorganize a workbook
- clean up a worksheet
- standardize workbook formatting
- build a model tab from scratch

without the LLM feeling that a one-off Python script is faster or more flexible.

## Improvement Areas

### 1. Fix `run-plan` Style Ergonomics

Problem:

- Styling in plans currently expects JSON strings in places where normal nested JSON objects would be more natural.
- This creates avoidable retries and makes the skill feel brittle.

Plan:

- Allow `run-plan` style actions to accept native JSON objects for `font`, `fill`, `border`, and `alignment`.
- Keep backward compatibility with the existing string-based payload format.
- Normalize the plan payload internally before dispatch.
- Improve validation messages so the plan says exactly what is malformed.

Success criteria:

- A plan author can write normal JSON objects in style payloads.
- No retry should be needed just because nested style data was not stringified.

### 2. Add Multi-Range Support

Problem:

- `set-style` and related formatting operations currently focus on one contiguous range at a time.
- This makes real cleanup work verbose and pushes the LLM toward ad hoc scripts.

Plan:

- Add support for multiple disjoint ranges in one action.
- Support this first in:
  - `set-style`
  - `format-range`
  - possibly `set-column-widths` and `set-row-heights` where appropriate
- Accept either repeated `--range` usage or a `ranges` array in plans.

Success criteria:

- One action can style several noncontiguous workbook areas cleanly.
- Cleanup plans shrink materially for formatting-heavy jobs.

### 3. Expand Workbook and Sheet Presentation Controls

Problem:

- Useful polish operations like gridlines and tab color are outside the exposed action set.
- This makes cosmetic cleanup feel incomplete.

Plan:

- Add workbook/sheet display actions for:
  - gridlines on/off
  - tab color
  - zoom scale
  - selected/active sheet state if feasible
  - print settings where easy and stable
- Add these as explicit executor commands and plan actions.

Success criteria:

- Common presentation polish does not require dropping into ad hoc code.

### 4. Add Reusable Style Presets

Problem:

- The skill has mechanics for style application but no opinionated formatting vocabulary.
- Cleanup and model-building requests naturally want concepts like “header row” or “final total.”

Plan:

- Introduce named style presets such as:
  - `section_header`
  - `table_header`
  - `input_cell`
  - `formula_cell`
  - `final_total`
  - `note_cell`
- Let presets be applied directly or overridden with additional style keys.
- Keep the initial preset set small and practical.

Success criteria:

- The LLM can express common workbook styling intent without fully specifying colors, fonts, and borders every time.

### 5. Add Theme Tokens

Problem:

- Repeated style definitions are noisy and fragile.
- The skill lacks a compact way to reuse workbook color/style choices.

Plan:

- Support simple theme tokens in plans and direct commands.
- Start with a small theme object containing:
  - accent colors
  - neutral fills
  - header font color
  - border color
- Allow preset styles to resolve through the active theme.

Success criteria:

- A workbook cleanup or build can define colors once and reuse them across many actions.

### 6. Add Higher-Level Cleanup Commands

Problem:

- The executor is still mostly an action API.
- It needs a few higher-level commands that match actual user intent.

Plan:

- Add at least one cleanup-oriented composite command, likely:
  - `cleanup-sheet`
- Candidate behaviors:
  - standardize title and section headers
  - improve spacing
  - freeze sensible panes
  - align labels and numeric areas
  - apply consistent table/header styling
  - reduce visual noise
- Keep this configurable rather than fully automatic magic.

Success criteria:

- For a normal “clean this tab up” request, the skill feels like the natural first choice.

### 7. Improve Plan Authoring Workflow

Problem:

- `run-plan` is powerful, but still verbose for formatting-heavy jobs.

Plan:

- Add cleaner plan examples in `SKILL.md`.
- Add a reusable example plan file in `examples/`.
- Consider a lightweight “plan template” format for style-heavy work.
- Improve `validate-plan` output so it acts like a real authoring assistant.

Success criteria:

- Multi-step formatting plans become easier to write correctly on the first try.

### 8. Tighten Runtime Confidence

Problem:

- Confidence drops quickly when install/runtime behavior is unclear.

Plan:

- Keep the installed `.codex/skills` copy aligned with the repo version.
- Document any dependency assumptions clearly in the skill.
- Add a small sync helper later if needed.
- Keep command examples accurate and runnable.

Success criteria:

- A model reading the skill has no reason to distrust the documented execution path.

## Priority Order

### Phase 1: Friction Removal

- Fix `run-plan` style payload handling
- Improve plan validation messaging
- Add multi-range support for style operations

### Phase 2: Cleanup Fit

- Add gridlines, tab color, zoom, and related presentation controls
- Add reusable style presets

### Phase 3: Better Abstractions

- Add theme tokens
- Add `cleanup-sheet` or similar higher-level cleanup command
- Improve plan examples and templates

## Definition of Done

This improvement cycle should be considered successful when:

- `workbook-action-executor` is still strong for structured build tasks
- the LLM is noticeably more likely to use it for cosmetic cleanup tasks
- style-heavy plans no longer feel brittle
- workbook polish actions no longer require falling back to direct `openpyxl`
- the skill surface feels more expressive than mechanical

## Accountability Note

This file is the reference plan for the next `workbook-action-executor` upgrade cycle.

Future changes should be judged against these outcomes, not just against whether more commands were added.

## Completion Check

Implemented in this cycle:

- `run-plan` now accepts native nested JSON objects for style payloads, while keeping string-based JSON compatibility.
- `validate-plan` now produces more specific payload-shape feedback and more actionable warnings.
- `set-style` and `format-range` now support multiple disjoint ranges in both CLI usage and JSON plans.
- Sheet-level presentation controls were added through `set-sheet-view`, including gridlines, tab color, zoom, and print settings.
- Reusable style presets were added: `section_header`, `table_header`, `input_cell`, `formula_cell`, `final_total`, and `note_cell`.
- Theme tokens were added and can be overridden through direct commands or plans.
- A higher-level `cleanup-sheet` command was added for cosmetic cleanup and presentation polish.
- `SKILL.md` now includes cleaner plan guidance and examples.
- A reusable example plan was added in `summary_cleanup_plan.json`.
- A repo-side sync helper was added at `skills/sync_excel_skills_to_codex.sh` to reduce runtime drift when refreshing the installed skill copy later.
