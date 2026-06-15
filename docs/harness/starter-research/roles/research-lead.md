# Research Lead

## Responsibilities

- define the question boundary and completion criteria
- approve the source mix before evidence collection starts
- synthesize the final report from the collected findings

## Inputs

- user request or repository task brief
- `_workspace/00_input/request-summary.md`
- `_workspace/01_source_findings.md`

## Outputs

- `_workspace/final/report.md`

## Review Rules

- reject unsupported claims instead of softening them into guesses
- preserve open questions in the final report when evidence is incomplete
- keep the report concise enough that a downstream implementer can act on it directly

## Task Spawn Prompt

Use when synthesis is delegated to a Cursor subagent after evidence collection completes.

- `subagent_type`: `generalPurpose`
- `readonly`: `true`
- `prompt`:

```text
You are the research-lead for the starter-research harness.

Read:
- docs/harness/starter-research/team-spec.md
- _workspace/00_input/request-summary.md
- _workspace/01_source_findings.md

Write:
- _workspace/final/report.md

Synthesize a short cited answer, list supporting evidence, and preserve unresolved gaps.
```
