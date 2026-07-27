# Analysis Plan: claude_logs_pipeline

## Connection
pipeline: claude_logs_pipeline
dataset: claude_logs_20260726033100
destination: duckdb

## Profile Summary
| table | rows | key columns | notes |
|-------|------|-------------|-------|
| logs | 4638 | type, timestamp, session_id, cwd, message__role, message__model, message__usage__input_tokens, message__usage__output_tokens | 10 sessions, 11 raw cwd values (7 after case-normalizing), time range 2026-05-18 to 2026-07-26. `cwd` has mixed drive-letter casing (`d:\...` vs `D:\...`) — normalize with LOWER(). No classic PII columns; file paths include local username, expected for personal log data. |
| logs__message__content | 2928 | type, name, tool_use_id | Nested content blocks per assistant/user message: `text`, `thinking`, `tool_use` (tool calls, `name` = tool name), `tool_result` |

## Questions
1. [x] Which projects have the most Claude Code activity (top 5)? → Chart 1
2. [x] Which tools are used most often? → Chart 2
3. [x] Which models are generating the assistant responses? → Chart 3

## Data Gaps
(none)

## Chart 1: Top 5 Projects by Activity
question: Which projects have the most Claude Code activity?
type: bar
x: project (LOWER(cwd))
y: count(*)
source: logs

```sql
SELECT
    LOWER(cwd) AS project,
    count(*) AS event_count
FROM logs
WHERE cwd IS NOT NULL
GROUP BY LOWER(cwd)
ORDER BY event_count DESC
LIMIT 5
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("event_count:Q", title="Events"),
    y=alt.Y("project:N", sort="-x", title="Project"),
    tooltip=["project:N", "event_count:Q"]
).properties(title="Top 5 Projects by Activity")
```

## Chart 2: Most-Used Tools
question: Which tools are used most often?
type: bar
x: tool_name
y: count(*)
source: logs__message__content

```sql
SELECT
    name AS tool_name,
    count(*) AS uses
FROM logs__message__content
WHERE type = 'tool_use' AND name IS NOT NULL
GROUP BY name
ORDER BY uses DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("uses:Q", title="Uses"),
    y=alt.Y("tool_name:N", sort="-x", title="Tool"),
    tooltip=["tool_name:N", "uses:Q"]
).properties(title="Most-Used Tools")
```

## Chart 3: Assistant Messages by Model
question: Which models are generating the assistant responses?
type: bar
x: model
y: count(*)
source: logs

```sql
SELECT
    message__model AS model,
    count(*) AS messages
FROM logs
WHERE type = 'assistant' AND message__model IS NOT NULL
GROUP BY message__model
ORDER BY messages DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("messages:Q", title="Assistant Messages"),
    y=alt.Y("model:N", sort="-x", title="Model"),
    tooltip=["model:N", "messages:Q"]
).properties(title="Assistant Messages by Model")
```
