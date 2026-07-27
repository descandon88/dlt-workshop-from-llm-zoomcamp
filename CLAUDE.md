# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A [dlthub](https://dlthub.com) workspace, scaffolded via `uvx dlthub-init@latest`. dlthub is the AI/agent-oriented layer on top of `dlt` (data load tool) for building, deploying, and managing data pipelines. The workspace is currently empty (no pipelines, sources, or notebooks have been added yet) — `__deployment__.py` has an empty `__all__` list waiting for pipelines/notebooks to be imported and registered.

Project name (from `pyproject.toml`): `dlthub-workspace`. Requires Python >=3.10; dependency management is via `uv` (`uv.lock` is present).

## Working in this repo: use the skills, not ad-hoc code

This repo is designed to be driven through the installed skills rather than hand-written pipeline code from scratch:

- **`.claude/skills/dlthub-router`** — entry point. Routes a stated goal (build a pipeline from a REST API, ingest from SQL, load CSVs from S3, build reports, add data quality checks, deploy/schedule) to the right toolkit, installs it via `dlthub --non-interactive ai toolkit install <name>`, then hands off to that toolkit's entry skill. Use this first when no matching toolkit is installed yet.
- **`.claude/skills/setup-secrets`** — the *only* sanctioned way to manage credentials. Secrets live in `.dlt/secrets.toml` (or profile-scoped `.dlt/<profile>.secrets.toml`). **Never read secrets files directly.** Prefer the `dlt-workspace-mcp` MCP tools (`secrets_list`, `secrets_view_redacted`, `secrets_update_fragment`); fall back to `dlthub ai secrets ...` CLI commands documented in `.claude/skills/setup-secrets/cli-reference.md` when MCP isn't connected. Only ever write placeholder values through tooling — real secret values are filled in by the user directly in the file.
- **`.claude/skills/improve-skills`** — run at the end of a session (or on request) to capture debugging patterns/data quirks/workflow fixes learned that session back into the relevant SKILL.md files. Read the target skill first, keep edits lean (a bullet or a few lines), and get user approval before editing.

Both `.claude/skills/` and `.agents/skills/` contain identical copies of these skills (agent-specific install locations); treat them as mirrors, not independent sources of truth.

## Secrets file conventions

When adding credentials to `.dlt/secrets.toml`, scope them under the source/destination name:

```toml
[sources.<source_name>]
api_key = "<paste-your-api-key-here>"

[destination.<destination_name>.credentials]
host = "localhost"
port = 5432
database = "analytics"
username = "loader"
password = "<paste-your-password-here>"
```

In pipeline code, read secrets/config via `dlt.secrets` / `dlt.config` using the same TOML dotted path (e.g. `dlt.secrets["sources.github.api_key"]`) rather than importing the TOML file directly.

## Configuration

- `.dlt/config.toml` — non-secret runtime config (e.g. `runtime.log_level`).
- `.dlt/secrets.toml` — secrets (gitignored via `secrets.toml` / `*.secrets.toml` patterns in `.gitignore`).
- `.dlt/.workspace` — marks this directory as a dlthub workspace root.
- `__deployment__.py` — the deployment manifest; import pipelines/notebooks here and list them in `__all__` for them to be deployed.
