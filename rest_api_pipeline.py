from typing import Any

import dlt
from dlt.hub import run
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="agent_traces")
def agent_traces_source(base_url: str = dlt.config.value) -> Any:
    """Load Claude Code agent logs from the agent-traces API.

    Args:
        base_url: API base URL. Auto-loaded from config.toml [sources.agent_traces].
    """
    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            # no auth required
        },
        "resources": [
            {
                "name": "logs",
                "endpoint": {
                    "path": "logs",
                    "paginator": {
                        "type": "offset",
                        "limit": 1000,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        "total_path": "total",
                        "maximum_offset": 100_000,  # ~100k row sample of the 1M available
                    },
                },
                "primary_key": "index",
            },
        ],
    }

    yield from rest_api_resources(config)


@run.pipeline("agent_traces_pipeline")
def load_agent_traces() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="agent_traces_pipeline",
        destination="warehouse",  # duckdb on dev profile, motherduck on prod profile
        dataset_name="agent_traces",
    )

    load_info = pipeline.run(
        agent_traces_source(),
        write_disposition="replace",
    )
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_agent_traces()
