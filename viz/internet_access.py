import plotly.express as px
import pandas as pd


def graph(df, template):
    title = "Digital Access Components vs. Internet Availability"
    description = "This chart compares components of institutional data openness (normalized) against internet access rates. The stacked areas show each country's performance across different accessibility dimensions, while the line indicates their internet penetration rate."

    df = df.sort_values("internet_access", ascending=False)
    area_columns = [
        "Accessibility",
        "Language",
        "Data Sharing",
        "Political integrity interoperability",
    ]
    df_normalized = df[area_columns].div(4)
    df_normalized["country"] = df["country"]
    df_normalized["internet_access"] = df["internet_access"]
    line_color = "#5E35B1"
    axis_color = "#5E35B1"
    fig = px.area(
        df_normalized,
        x="country",
        y=area_columns,
        template=template,
        labels={
            "value": "Normalized Institutional Components (%)",
            "country": "Country",
            "variable": "Component",
        },
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.add_trace(
        px.line(df_normalized, x="country", y="internet_access", template=template)
        .update_traces(
            line=dict(color=line_color, width=3),
            name="Internet Access",
            yaxis="y2",
            hovertemplate="<span style='font-size:11px;color:gray'>Internet Access: %{y:.1f}%</span><extra></extra>",
        )
        .data[0]
    )
    fig.update_layout(
        margin=dict(l=180, r=180, t=30, b=30),
        yaxis=dict(
            title="Normalized Institutional Components (%)",
            range=[0, 50],
            showgrid=True,
            gridcolor="rgba(200,200,200,0.2)",
        ),
        yaxis2=dict(
            title="Internet Access (%)",
            range=[50, 100],
            overlaying="y",
            side="right",
            showgrid=False,
            titlefont=dict(color=axis_color),
            tickfont=dict(color=axis_color),
        ),
        xaxis=dict(title="Country", tickangle=45),
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h", yanchor="top", y=1.15, xanchor="center", x=0.5, title=None
        ),
        hoverlabel=dict(bgcolor="white", font_size=11, font_color="gray"),
        hovermode="x unified",
    )

    for trace in fig.data[:-1]:
        trace.hovertemplate = "<span style='font-size:11px;color:gray'>%{fullData.name}: %{y:.1f}%</span><extra></extra>"

    return [fig, title, description]
