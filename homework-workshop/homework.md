# Homework: Instrumenting and tracing agents

## Question 1. Instrument the agent with Logfire

Query: "How do I run Ollama locally?"

**Answer: 4 spans**

```
faq_agent run                    <- 1 root span (the whole agent run)
  chat llama-3.1-8b-instant      <- LLM call #1 (decides to search)
  running tool: search           <- 1 tool call
  chat llama-3.1-8b-instant      <- LLM call #2 (writes final answer from the search result)
```

1 agent-run span + 2 LLM-call spans + 1 tool-call span = 4 spans total. This varies run to run
depending on how many searches the model decides to make (1 search here).

## Question 2. Load traces into DuckDB with dlt

**Answer: 24 tables**

```sql
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'agent_traces';
-- 24
```

Built with `homework-workshop/logfire_pipeline.py` — a dlt REST API pipeline that POSTs a SQL
query to the Logfire Query API (`/v2/query`) against the `records` table (one row per span) and
loads the result into DuckDB, dataset `agent_traces`.

Tables created:
- `records` — main span table
- 20 child tables from flattening the nested `records.attributes` JSON (LLM input/output
  messages and their `.parts`/`.parts.result` sub-levels, tool definitions/calls, token usage
  and cost metrics, scrubbed-field paths, function-tool schemas)
- `_dlt_loads`, `_dlt_version`, `_dlt_pipeline_state` — dlt's internal bookkeeping tables

## Question 3. Query traces with an agent

Trace for the Q1 run (`019fc52f9d57a880fd04f0c758279149`), summing
`gen_ai.usage.input_tokens` across its 2 `chat` spans:

| span | input_tokens |
|---|---|
| chat #1 (before search) | 384 |
| chat #2 (after search, final answer) | 1,450 |
| **Total** | **1,834** |

**Answer: 1500 - 5000**
