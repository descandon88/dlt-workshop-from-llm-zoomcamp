from typing import Any

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="logfire")
def logfire_source(
    base_url: str = dlt.config.value,
    read_token: str = dlt.secrets.value,
    min_timestamp: str = "2020-01-01T00:00:00Z",
) -> Any:
    """Load span/trace records from the Pydantic Logfire Query API.

    Logfire has no REST "list traces" endpoint — instead you POST a SQL query
    to /v2/query and it runs it against the `records` table (one row per
    span). Each row's `attributes` column is deeply nested JSON (LLM
    messages, tool calls, token usage, ...), which dlt flattens into child
    tables on load.

    Args:
        base_url: Logfire region base URL. Auto-loaded from config.toml [sources.logfire].
        read_token: Logfire read token (Settings > Read tokens). Auto-loaded from secrets.toml [sources.logfire].
        min_timestamp: Lower bound for the query (ISO8601). Logfire requires this on every request.
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "auth": {
                "type": "bearer",
                "token": read_token,
            },
        },
        "resources": [
            {
                "name": "records",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "json": {
                        "sql": "SELECT * FROM records ORDER BY start_timestamp",
                        "min_timestamp": min_timestamp,
                        "limit": 10_000,
                    },
                    "data_selector": "data",
                },
                "primary_key": "span_id",
            },
        ],
    }

    yield from rest_api_resources(config)


def load_logfire_traces() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="logfire_pipeline",
        destination="duckdb",
        dataset_name="agent_traces",
    )

    load_info = pipeline.run(
        logfire_source(),
        write_disposition="replace",
    )
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_logfire_traces()
