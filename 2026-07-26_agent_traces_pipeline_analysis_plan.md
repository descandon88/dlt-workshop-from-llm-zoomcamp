# Analysis Plan: agent_traces_pipeline

## Connection
pipeline: agent_traces_pipeline
dataset: agent_traces_20260726040935
destination: duckdb

## Profile Summary
| table | rows | key columns | notes |
|-------|------|-------------|-------|
| logs | 100000 | type, timestamp, session_id, cwd, message__model, usage__input_tokens, usage__output_tokens | 12,446 sessions, 5 projects, time range 2026-01-01 to 2026-01-09 (synthetic/uniformly distributed test data). No PII. |
| logs__message__content | 98567 | type, name | Nested content blocks: `text` (65,715) and `tool_use` (32,852, `name` = tool name, 8 distinct tools) |

## Questions
1. [x] How does activity trend day over day? → Chart 1
2. [x] How does token usage trend over time? → Chart 2
3. [x] Which projects have the most activity? → Chart 3
4. [x] Which tools are used most often? → Chart 4
5. [x] Which models are used most? → Chart 5
6. [x] Which model uses the most tokens per message on average? → Chart 6
7. [x] What's the split between user and assistant messages? → Chart 7

## Data Gaps
(none)

## Chart 1: Daily Activity Trend
question: How does activity trend day over day?
type: line
x: day (daily)
y: count(*)
source: logs

```sql
SELECT
    DATE_TRUNC('day', timestamp) AS day,
    count(*) AS event_count
FROM logs
GROUP BY 1
ORDER BY 1
```

```altair
alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("day:T", title="Day"),
    y=alt.Y("event_count:Q", title="Events"),
    tooltip=["day:T", "event_count:Q"]
).properties(title="Daily Activity Trend")
```

## Chart 2: Token Usage Over Time
question: How does token usage trend over time?
type: line
x: day (daily)
y: sum(input_tokens), sum(output_tokens)
source: logs

```sql
SELECT
    DATE_TRUNC('day', timestamp) AS day,
    sum(usage__input_tokens) AS input_tokens,
    sum(usage__output_tokens) AS output_tokens
FROM logs
WHERE type = 'assistant'
GROUP BY 1
ORDER BY 1
```

```altair
_df_long = df.melt(id_vars=["day"], value_vars=["input_tokens", "output_tokens"], var_name="token_type", value_name="tokens")
alt.Chart(_df_long).mark_line(point=True).encode(
    x=alt.X("day:T", title="Day"),
    y=alt.Y("tokens:Q", title="Tokens"),
    color=alt.Color("token_type:N", title="Token Type"),
    tooltip=["day:T", "token_type:N", "tokens:Q"]
).properties(title="Token Usage Over Time")
```

## Chart 3: Activity by Project
question: Which projects have the most activity?
type: bar
x: project (cwd)
y: count(*)
source: logs

```sql
SELECT
    cwd AS project,
    count(*) AS event_count
FROM logs
GROUP BY cwd
ORDER BY event_count DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("event_count:Q", title="Events"),
    y=alt.Y("project:N", sort="-x", title="Project"),
    tooltip=["project:N", "event_count:Q"]
).properties(title="Activity by Project")
```

## Chart 4: Most-Used Tools
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

## Chart 5: Model Usage Breakdown
question: Which models are used most?
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
).properties(title="Model Usage Breakdown")
```

## Chart 6: Avg Tokens per Model
question: Which model uses the most tokens per message on average?
type: bar
x: model
y: avg(input_tokens + output_tokens)
source: logs

```sql
SELECT
    message__model AS model,
    avg(usage__input_tokens + usage__output_tokens) AS avg_tokens
FROM logs
WHERE type = 'assistant' AND message__model IS NOT NULL
GROUP BY message__model
ORDER BY avg_tokens DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("avg_tokens:Q", title="Avg Tokens per Message"),
    y=alt.Y("model:N", sort="-x", title="Model"),
    tooltip=["model:N", "avg_tokens:Q"]
).properties(title="Avg Tokens per Model")
```

## Chart 7: User vs Assistant Messages
question: What's the split between user and assistant messages?
type: bar
x: type
y: count(*)
source: logs

```sql
SELECT
    type,
    count(*) AS messages
FROM logs
GROUP BY type
ORDER BY messages DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("messages:Q", title="Messages"),
    y=alt.Y("type:N", sort="-x", title="Message Type"),
    tooltip=["type:N", "messages:Q"]
).properties(title="User vs Assistant Messages")
```
