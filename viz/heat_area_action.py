import plotly.express as px
import pandas as pd
import numpy as np


def add_separators_and_annotations(fig, df, ordered_cols, norm_matrix):
    total_columns = len(ordered_cols)
    num_rows = len(df["country"])
    lines_positions = [2.5, 9.5]
    for pos_line in lines_positions:
        fig.add_shape(
            type="line",
            x0=pos_line,
            x1=pos_line,
            y0=-1.8,
            y1=num_rows + 0.5,
            line=dict(color="grey", width=2),
            xref="x",
            yref="y",
        )

    fig.add_annotation(
        x=1,
        y=-2.5,
        text="LAC - High Development",
        showarrow=False,
        font=dict(size=12, color="grey"),
        xref="x",
        yref="y",
    )

    fig.add_annotation(
        x=6.25,
        y=-2.5,
        text="LAC - Medium Development",
        showarrow=False,
        font=dict(size=12, color="grey"),
        xref="x",
        yref="y",
    )

    fig.add_annotation(
        x=(10 + total_columns) / 2,
        y=-2.5,
        text="LAC - Low Development",
        showarrow=False,
        font=dict(size=12, color="grey"),
        xref="x",
        yref="y",
    )

    column_means = norm_matrix.mean(axis=0)
    for idx, mean_value in enumerate(column_means):
        fig.add_annotation(
            x=idx,
            y=-1.3,
            text=f"{mean_value:.2f}",
            showarrow=False,
            font=dict(size=10, color="grey"),
            xref="x",
            yref="y",
        )


def graph(df, template):
    title = "Action Areas by Country: Uneven Efforts in Building Capacities"
    description = "Shows the status of each action area by country, revealing priorities and gaps in capacity development across the region."
    exclude_cols = ["cpi", "internet_access", "country"]
    data_cols = [col for col in df.columns if col not in exclude_cols]

    ordered_cols = df[data_cols].sum().sort_values(ascending=False).index.tolist()

    data_matrix = df[ordered_cols].to_numpy()
    norm_matrix = (data_matrix - np.min(data_matrix)) / (
        np.max(data_matrix) - np.min(data_matrix) + 1e-9
    )

    hovertext = []
    for i, country in enumerate(df["country"]):
        row = []
        for j, col in enumerate(ordered_cols):
            val = data_matrix[i][j]
            row.append(f"Country: {country}<br>{col}: {val:.2f}")
        hovertext.append(row)

    fig = px.imshow(
        norm_matrix,
        labels=dict(x="Action area", y="Country", color="Score"),
        x=ordered_cols,
        y=df["country"],
        aspect="auto",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        template=template,
        height=500,
        margin=dict(l=40, r=40, t=5, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(title="Score", thickness=10),
    )

    add_separators_and_annotations(fig, df, ordered_cols, norm_matrix)

    fig.update_yaxes(ticksuffix="  ")
    fig.update_traces(hoverinfo="text", hovertext=hovertext)
    fig.update_xaxes(showline=False, zeroline=False)
    fig.update_yaxes(showline=False, zeroline=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return [fig, title, description]
