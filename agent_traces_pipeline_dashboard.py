import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import dlt

    return alt, dlt, mo


@app.cell
def _(dlt):
    pipeline = dlt.attach("agent_traces_pipeline")
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(mo):
    mo.md("""
    # Agent Traces Report
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Daily Activity Trend
    """)
    return


@app.cell
def _(dataset):
    df_chart1 = dataset("""
        SELECT
            DATE_TRUNC('day', timestamp) AS day,
            count(*) AS event_count
        FROM logs
        GROUP BY 1
        ORDER BY 1
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1):
    _chart = alt.Chart(df_chart1).mark_line(point=True).encode(
        x=alt.X("day:T", title="Day"),
        y=alt.Y("event_count:Q", title="Events"),
        tooltip=["day:T", "event_count:Q"]
    ).properties(title="Daily Activity Trend")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Token Usage Over Time
    """)
    return


@app.cell
def _(dataset):
    df_chart2 = dataset("""
        SELECT
            DATE_TRUNC('day', timestamp) AS day,
            sum(usage__input_tokens) AS input_tokens,
            sum(usage__output_tokens) AS output_tokens
        FROM logs
        WHERE type = 'assistant'
        GROUP BY 1
        ORDER BY 1
    """).df()
    return (df_chart2,)


@app.cell
def _(df_chart2):
    df_chart2_long = df_chart2.melt(
        id_vars=["day"],
        value_vars=["input_tokens", "output_tokens"],
        var_name="token_type",
        value_name="tokens",
    )
    return (df_chart2_long,)


@app.cell
def _(alt, df_chart2_long):
    _chart = alt.Chart(df_chart2_long).mark_line(point=True).encode(
        x=alt.X("day:T", title="Day"),
        y=alt.Y("tokens:Q", title="Tokens"),
        color=alt.Color("token_type:N", title="Token Type"),
        tooltip=["day:T", "token_type:N", "tokens:Q"]
    ).properties(title="Token Usage Over Time")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Activity by Project
    """)
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        SELECT
            cwd AS project,
            count(*) AS event_count
        FROM logs
        GROUP BY cwd
        ORDER BY event_count DESC
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3):
    _chart = alt.Chart(df_chart3).mark_bar().encode(
        x=alt.X("event_count:Q", title="Events"),
        y=alt.Y("project:N", sort="-x", title="Project"),
        tooltip=["project:N", "event_count:Q"]
    ).properties(title="Activity by Project")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Most-Used Tools
    """)
    return


@app.cell
def _(dataset):
    df_chart4 = dataset("""
        SELECT
            name AS tool_name,
            count(*) AS uses
        FROM logs__message__content
        WHERE type = 'tool_use' AND name IS NOT NULL
        GROUP BY name
        ORDER BY uses DESC
    """).df()
    return (df_chart4,)


@app.cell
def _(alt, df_chart4):
    _chart = alt.Chart(df_chart4).mark_bar().encode(
        x=alt.X("uses:Q", title="Uses"),
        y=alt.Y("tool_name:N", sort="-x", title="Tool"),
        tooltip=["tool_name:N", "uses:Q"]
    ).properties(title="Most-Used Tools")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Model Usage Breakdown
    """)
    return


@app.cell
def _(dataset):
    df_chart5 = dataset("""
        SELECT
            message__model AS model,
            count(*) AS messages
        FROM logs
        WHERE type = 'assistant' AND message__model IS NOT NULL
        GROUP BY message__model
        ORDER BY messages DESC
    """).df()
    return (df_chart5,)


@app.cell
def _(alt, df_chart5):
    _chart = alt.Chart(df_chart5).mark_bar().encode(
        x=alt.X("messages:Q", title="Assistant Messages"),
        y=alt.Y("model:N", sort="-x", title="Model"),
        tooltip=["model:N", "messages:Q"]
    ).properties(title="Model Usage Breakdown")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Avg Tokens per Model
    """)
    return


@app.cell
def _(dataset):
    df_chart6 = dataset("""
        SELECT
            message__model AS model,
            avg(usage__input_tokens + usage__output_tokens) AS avg_tokens
        FROM logs
        WHERE type = 'assistant' AND message__model IS NOT NULL
        GROUP BY message__model
        ORDER BY avg_tokens DESC
    """).df()
    return (df_chart6,)


@app.cell
def _(alt, df_chart6):
    _chart = alt.Chart(df_chart6).mark_bar().encode(
        x=alt.X("avg_tokens:Q", title="Avg Tokens per Message"),
        y=alt.Y("model:N", sort="-x", title="Model"),
        tooltip=["model:N", "avg_tokens:Q"]
    ).properties(title="Avg Tokens per Model")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## User vs Assistant Messages
    """)
    return


@app.cell
def _(dataset):
    df_chart7 = dataset("""
        SELECT
            type,
            count(*) AS messages
        FROM logs
        GROUP BY type
        ORDER BY messages DESC
    """).df()
    return (df_chart7,)


@app.cell
def _(alt, df_chart7):
    _chart = alt.Chart(df_chart7).mark_bar().encode(
        x=alt.X("messages:Q", title="Messages"),
        y=alt.Y("type:N", sort="-x", title="Message Type"),
        tooltip=["type:N", "messages:Q"]
    ).properties(title="User vs Assistant Messages")
    _chart
    return


if __name__ == "__main__":
    app.run()
