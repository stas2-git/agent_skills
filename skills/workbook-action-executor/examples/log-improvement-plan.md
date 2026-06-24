# Log Improvement Plan

Created: 2026-04-13

Purpose:
Keep a durable copy of the agreed logging and `llm_work` improvement plan in the skill examples folder so future implementation can be checked against it directly.

## Problem Summary

Observed issues from the workbook-skill test:

- The LLM created its own backup even though the skill stack already has a backup system.
- `excel-decompose` created an extra decomposition text copy in `llm_work`.
- `llm_work` currently has too much folder structure for practical agent use.
- `run_log.json` is useful as an audit trail but still too verbose relative to its purpose.

## Design Goal

`llm_work` should be optimized for agent consumption first, audit second.

That means:

- one obvious current-state area
- one historical runs area
- minimal duplicate files
- logs that point to artifacts instead of repeating them
- one governed backup path

## Planned Changes

### 1. Govern backup creation

Goal:
Avoid ad hoc workbook backups when the skill stack already supports managed backup behavior.

Plan:

- Add an explicit backup policy for edit workflows.
- Default edit workflows to a managed backup path.
- Log whether backup was:
  - `managed_by_skill`
  - `reused_existing`
  - `skipped`
- Update skill instructions so workbook edits should not create one-off backup files outside the managed backup flow when the skill stack supports backup handling.

### 2. Stop duplicate decomposition outputs

Goal:
Avoid writing the same decomposition content into multiple locations unnecessarily.

Current problem:

- explicit output file
- run-local decomposition copy
- mirrored current decomposition copy

Target behavior:

- keep one primary run artifact under `llm_work/runs/<run_id>/...`
- only write a separate explicit `--output` file when the caller truly wants a custom export
- replace full current copies with a compact pointer/manifest where possible

### 3. Flatten `llm_work/current`

Goal:
Give the LLM one obvious place to look first.

Target files:

- `llm_work/current/state.json`
- `llm_work/current/context.md`
- `llm_work/current/latest_run.json`

Purpose:

- `state.json`: structured machine-readable current state
- `context.md`: compact agent-facing workbook context
- `latest_run.json`: small pointer/index to the newest successful run

### 4. Simplify per-run artifact layout

Goal:
Keep audit history while reducing unnecessary folder nesting.

Current style:

- `runs/<run_id>/decomposition/...`
- `runs/<run_id>/summaries/...`
- `runs/<run_id>/plans/...`
- `runs/<run_id>/actions/...`

Target style:

- `runs/<run_id>/artifacts/`
- `runs/<run_id>/run_log.json`

Example artifact filenames:

- `decomposition.txt`
- `summary.md`
- `summary.json`
- `plan.md`
- `plan.json`
- `checklist.md`
- `checklist.json`
- `action-run-plan.json`
- `backup-map.json`

### 5. Make `run_log.json` a compact index

Goal:
The log should describe what happened, not duplicate the full payloads already stored in artifacts.

Target event shape:

- `event_id`
- `event_type`
- `started_at_utc`
- `timestamp_utc`
- `duration_ms`
- `status`
- `artifact_refs`
- compact `summary`

Rules:

- no large embedded result trees
- no repeated full artifact payloads
- logs should point to artifacts, not replace them

### 6. Add one canonical workbook state file

Goal:
Make one structured file the default entry point for future workbook sessions.

Target:

- `llm_work/current/state.json`

Suggested contents:

- workbook path
- workbook modified time
- latest successful run id
- latest decomposition artifact
- latest summary artifact
- latest plan artifact
- latest checklist artifact
- latest action artifact
- latest backup map
- active warnings
- task fingerprint when available

### 7. Add artifact reuse and freshness logic

Goal:
Reduce unnecessary reruns and repeated file generation.

Reuse signals:

- workbook modified time
- workbook file size
- file hash later if needed
- task fingerprint for plan/checklist artifacts

Log field:

- `reused_existing_artifact: true/false`

## Implementation Priority

Recommended order:

1. Centralize backup policy
2. Remove duplicate decomposition/current copies
3. Add `llm_work/current/state.json`
4. Flatten run artifact layout
5. Standardize compact logs across helper scripts
6. Add freshness and reuse logic

## First Prototype Recommendation

Best first implementation slice:

- redesign `excel-decompose` output behavior
- create `llm_work/current/state.json`
- stop mirroring full decomposition files into `current/`
- make logs reference artifacts instead of duplicating them

## Accountability Note

This file is the reference plan to evaluate the follow-up implementation work.
Future changes should be checked against this plan explicitly rather than against an informal memory of the discussion.
