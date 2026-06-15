# Cursor Compatibility

## Install Paths

- Shared project install: `.agents/skills/harness/`
- Shared user install: `~/.agents/skills/harness/`
- Cursor project mirror: `.cursor/skills/harness/`
- Cursor user mirror: `~/.cursor/skills/harness/`

## Install Commands

Project install with Cursor mirror (recommended symlink mode):

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout cursor --mode symlink
```

User-level install with Cursor mirror:

```shell
python3 scripts/install_harness.py --scope user --layout cursor --mode symlink
```

After generating domain skills under `.agents/skills/`, mirror them for Cursor discovery:

```shell
python3 scripts/mirror_skills.py --target /path/to/repo --layout cursor
```

Use `--mode copy` when symlinks are not supported.

## When To Use Shared Skills Vs Native Mirrors

- Use `.agents/skills/` as the canonical source for every generated skill.
- Use `.cursor/skills/` as the native discovery mirror for Cursor sessions.
- Keep reusable Harness workflow logic in the shared tree and mirror it into Cursor after generation.

## Role Representation

Cursor has no `.cursor/agents/` directory. Replace Claude agent definitions with:

- specialist skills under `.agents/skills/{specialist}/SKILL.md`
- role briefs under `docs/harness/{domain}/roles/{role}.md` with Task-tool spawn prompts
- team topology in `docs/harness/{domain}/team-spec.md`

Read [cursor-orchestration.md](../../.agents/skills/harness/references/cursor-orchestration.md) for pattern-to-orchestration mapping.

## Always-Loaded Guidance

- Keep a short repo-owned `AGENTS.md` for cross-runtime `WHAT / WHY / HOW`.
- Add `.cursor/rules/harness-{domain}.mdc` only for durable, enforceable repo-wide constraints such as verify commands, canonical paths, and artifact naming.
- Leave workflow playbooks in skills and team specs, not in always-loaded rules.

## Generated Skill Frontmatter

Orchestrator skills:

```yaml
---
name: {domain}-orchestrator
description: ...
user-invocable: true
---
```

Specialist skills:

```yaml
---
name: {specialist}
description: ...
disable-model-invocation: true
---
```

Expert Pool roles that users invoke directly may also set `user-invocable: true`.

Every generated `SKILL.md` must include at least `name` and `description`.

## `_workspace/` Git Policy

- Gitignore `_workspace/` by default in the target repository.
- Treat phase handoffs as session-local working state.
- Document opt-in commit for experiment ledgers under `_workspace/experiments/` when a harness uses autonomous experimentation.

## Related Runtimes

| Runtime | Repo / install |
| --- | --- |
| Claude Code | [revfactory/harness](https://github.com/revfactory/harness) |
| Cursor | [tsonmiramar/harness](https://github.com/tsonmiramar/harness) with `--layout cursor` |
| Codex | [SaehwanPark/meta-harness](https://github.com/SaehwanPark/meta-harness) with `--layout codex` |
