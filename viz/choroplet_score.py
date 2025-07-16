import pandas as pd
import plotly.graph_objects as go


def graph(df, template="plotly_dark"):
    title = "Regional Overview: The State of Data in Latin America and the Caribbean"
    description = "A snapshot of national scores across key data domains, highlighting current conditions and regional contrasts."

    columns = [
        "Overall Score",
        "Company Information",
        "Critical Competencies",
        "Equitable Access",
        "Governance Foundation",
        "Land Management",
        "Political Integrity",
        "Public Finance",
        "Public Procurement",
    ]

    column_mapping = {
        "Overall Score": "overall_score",
        "Company Information": "Company Information",
        "Critical Competencies": "Critical Competencies",
        "Equitable Access": "Equitable Access",
        "Governance Foundation": "Governance Foundation",
        "Land Management": "Land Management",
        "Political Integrity": "Political Integrity",
        "Public Finance": "Public Finance",
        "Public Procurement": "Public Procurement",
    }

    traces = []
    for col_name in columns:
        col_data = column_mapping[col_name]
        traces.append(
            go.Choropleth(
                locations=df["iso3"],
                z=df[col_data],
                text=df["country"],
                coloraxis="coloraxis",
                marker_line_color="white",
                marker_line_width=0.5,
                visible=(col_name == "Overall Score"),
                zmin=0,
                zmax=100,
                hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}%<extra></extra>",
            )
        )

    buttons = []
    for i, col_name in enumerate(columns):
        visible = [False] * len(columns)
        visible[i] = True
        buttons.append(
            dict(
                label=col_name,
                method="update",
                args=[
                    {"visible": visible},
                ],
            )
        )

    fig = go.Figure(data=traces)

    fig.update_layout(
        template=template,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=500,
        margin=dict(t=0, b=0, r=0, l=0),
        geo=dict(
            scope="world",
            projection_type="mercator",
            showlakes=False,
            bgcolor="rgba(0,0,0,0)",
            lonaxis=dict(range=[-140, -30]),
            lataxis=dict(range=[-60, 35]),
            showframe=False,
            showcoastlines=False,
        ),
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                x=0.01,
                xanchor="left",
                y=1.05,
                yanchor="top",
                font=dict(
                    size=18,
                    color="#8F8C8C",
                ),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=1,
            )
        ],
        coloraxis=dict(
            colorscale="Viridis",
            cmin=0,
            cmax=100,
            colorbar=dict(
                thickness=10,
                len=0.7,
                title=dict(text="Score (%)<br> <br>", side="top", font=dict(size=12)),
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
                ticks="outside",
                tickfont=dict(size=10, color="#aaa"),
            ),
        ),
    )

    return [fig, title, description]
