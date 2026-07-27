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
    pipeline = dlt.attach("claude_logs_pipeline")
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(mo):
    mo.md("""
    # Claude Logs Report
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Top 5 Projects by Activity
    """)
    return


@app.cell
def _(dataset):
    df_chart1 = dataset("""
        SELECT
            LOWER(cwd) AS project,
            count(*) AS event_count
        FROM logs
        WHERE cwd IS NOT NULL
        GROUP BY LOWER(cwd)
        ORDER BY event_count DESC
        LIMIT 5
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1):
    _chart = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X("event_count:Q", title="Events"),
        y=alt.Y("project:N", sort="-x", title="Project"),
        tooltip=["project:N", "event_count:Q"]
    ).properties(title="Top 5 Projects by Activity")
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
    df_chart2 = dataset("""
        SELECT
            name AS tool_name,
            count(*) AS uses
        FROM logs__message__content
        WHERE type = 'tool_use' AND name IS NOT NULL
        GROUP BY name
        ORDER BY uses DESC
    """).df()
    return (df_chart2,)


@app.cell
def _(alt, df_chart2):
    _chart = alt.Chart(df_chart2).mark_bar().encode(
        x=alt.X("uses:Q", title="Uses"),
        y=alt.Y("tool_name:N", sort="-x", title="Tool"),
        tooltip=["tool_name:N", "uses:Q"]
    ).properties(title="Most-Used Tools")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Assistant Messages by Model
    """)
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        SELECT
            message__model AS model,
            count(*) AS messages
        FROM logs
        WHERE type = 'assistant' AND message__model IS NOT NULL
        GROUP BY message__model
        ORDER BY messages DESC
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3):
    _chart = alt.Chart(df_chart3).mark_bar().encode(
        x=alt.X("messages:Q", title="Assistant Messages"),
        y=alt.Y("model:N", sort="-x", title="Model"),
        tooltip=["model:N", "messages:Q"]
    ).properties(title="Assistant Messages by Model")
    _chart
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
