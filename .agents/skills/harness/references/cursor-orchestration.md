# Cursor Orchestration

Use this reference when the target runtime is Cursor. Cursor has no peer-to-peer agent messaging. Coordinate work with:

- the main agent following orchestrator skills and team specs
- the Task tool for bounded parallel subagent work
- deterministic `_workspace/` handoff files

Read this file before finalizing a Cursor-targeted harness.

## Pattern To Orchestration Mapping

| Pattern | Cursor coordination |
| --- | --- |
| Pipeline | Single agent runs sequential orchestrator phases and writes `_workspace/` handoffs |
| Fan-out/Fan-in | One message with N parallel Task calls, then a synthesis phase |
| Expert Pool | Team-spec routing table; load the matching specialist skill or launch a targeted Task |
| Producer-Reviewer | Producer writes artifact, reviewer skill or readonly Task reviews, bounded revision loop |
| Supervisor | Orchestrator skill reassigns work; spawn Task workers per backlog item when useful |
| Hierarchical Delegation | Shallow hierarchy only: orchestrator plus one downstream coordination layer |

Spawn Task workers only for bounded, clearly parallelizable slices. Prefer file handoffs for sequential dependent work. Use fan-out/fan-in when several independent slices can run in parallel before synthesis.

## Subagent Type Defaults

| Role type | `subagent_type` | `readonly` |
| --- | --- | --- |
| Codebase exploration | `explore` | `true` |
| Implementation or fix | `generalPurpose` | `false` |
| Shell, CI, or test execution | `shell` | `false` |
| Review or audit | `explore` or `generalPurpose` | `true` |

Keep role-specific overrides in `docs/harness/{domain}/roles/{role}.md`.

## Role Brief Template

Use role briefs when a stable role needs a Task spawn prompt without becoming a full skill.

```markdown
# {Role Name}

## Responsibilities
- ...

## Inputs
- ...

## Outputs
- `_workspace/{phase}_{role}_{artifact}.md`

## Task Spawn Prompt
Use when the orchestrator delegates this role to a subagent.

- `subagent_type`: `explore`
- `readonly`: `true`
- `prompt`:

\`\`\`text
You are the {role} for the {domain} harness.

Read:
- docs/harness/{domain}/team-spec.md
- {input artifacts}

Write:
- `_workspace/{phase}_{role}_{artifact}.md`

{role-specific instructions}
\`\`\`
```

## Parallel Fan-out Example

For Fan-out/Fan-in, launch all workers in one message:

```text
Task 1: subagent_type=explore, readonly=true, prompt from roles/source-a.md
Task 2: subagent_type=explore, readonly=true, prompt from roles/source-b.md
Task 3: subagent_type=explore, readonly=true, prompt from roles/source-c.md
```

After workers complete, the orchestrator or synthesis role reads all `_workspace/` outputs and writes the fan-in artifact.

## Phase 5 Cursor Checklist

1. Verify generated skills exist only under `.agents/skills/`.
2. Run `python3 scripts/mirror_skills.py --target <repo-root> --layout cursor`.
3. Create or update `.cursor/rules/harness-{domain}.mdc` when durable repo-wide constraints are needed.
4. Ensure `_workspace/` is gitignored unless the team spec documents opt-in experiment commits.
5. Confirm orchestrator skills use `user-invocable: true` and specialist skills use `disable-model-invocation: true`.

## Removable Cursor-Specific Logic

Keep Cursor Task spawn heuristics, retry wording, and model-specific recovery notes in this file or in role briefs. Do not weave them through portable team specs unless the target repository is Cursor-only.
