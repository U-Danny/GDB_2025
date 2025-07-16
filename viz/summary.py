import plotly.graph_objects as go


def graph(template):
    texto = [
        "1. <b>Citizen digital infrastructure</b> is high, but it does not translate into <b>effective access to public data</b>.<br>",
        "2. <b>Institutional data accessibility</b> remains fragmented, limited by <b>policies and technical practices</b>.<br>",
        "3. <b>Institutional capacities</b> for control and transparency are weak, especially in <b>company registries and political financing</b>.",
    ]
    texto_formateado = "<br>".join(texto)
    title = "Summary: Findings and Opportunities in LAC"
    description = "Opinion based exclusively on the analysis of selected areas in LAC: digital and institutional accessibility, and control and transparency capacities."
    fig = go.Figure()

    fig.update_layout(
        annotations=[
            dict(
                text=texto_formateado,
                xref="paper",
                yref="paper",
                x=0.5,
                y=1,
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=18,
                ),
                align="left",
                xanchor="center",
            )
        ],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=80, b=80, l=60, r=60),
        template=template,
    )

    return [fig, title, description]
