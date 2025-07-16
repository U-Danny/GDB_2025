import plotly.graph_objects as go
import pandas as pd


def graph(df, template):
    title = "Corruption Perception and Institutional Capacity for Strategic Data Transparency and Control"
    description = "This chart contrasts perception of corruption (CPI) with institutional development focused on the publication, management, and control of strategic data: company registers, political transparency, and financial oversight."

    key_columns = [
        "Company Register",
        "Beneficial Ownership",
        "Interest and asset declarations",
        "Lobbying",
        "Political Finance",
        "cpi",
        "country",
    ]
    df = df[[col for col in key_columns if col in df.columns]].copy()
    cols_to_stack = [col for col in df.columns if col not in ["country", "cpi"]]
    df[cols_to_stack] = df[cols_to_stack].apply(pd.to_numeric, errors="coerce")
    df["cpi"] = pd.to_numeric(df["cpi"], errors="coerce")
    for col in cols_to_stack:
        df[col] = df[col] / 5
    df_sorted = df.sort_values("cpi", ascending=False)
    countries = df_sorted["country"].tolist()
    cpi_values = df_sorted["cpi"].tolist()
    base_rgba = "176, 196, 222"
    segment_colors = [
        f"rgba({base_rgba}, 1.0)",
        f"rgba({base_rgba}, 0.85)",
        f"rgba({base_rgba}, 0.70)",
        f"rgba({base_rgba}, 0.55)",
        f"rgba({base_rgba}, 0.40)",
    ]
    fig = go.Figure()

    for idx, col in enumerate(cols_to_stack):
        fig.add_trace(
            go.Bar(
                x=df_sorted[col],
                y=countries,
                orientation="h",
                marker=dict(color=segment_colors[idx]),
                name=col,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=cpi_values,
            y=countries,
            mode="lines+markers",
            line=dict(color="mediumorchid", width=3),
            name="CPI: 0 = highly corrupt, 100 = very clean",
            hovertemplate="CPI: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        height=500,
        template=template,
        margin=dict(l=220, r=120, t=30, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        barmode="stack",
        xaxis=dict(
            showgrid=True, range=[0, 100], title="Institutional Data Accessibility (%)"
        ),
        yaxis=dict(showgrid=False),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            title_text="Area",
        ),
    )

    return [fig, title, description]
