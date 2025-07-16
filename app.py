import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from viz import choroplet_score, heat_area_action, internet_access, cpi_bar, summary
from dash import callback_context as ctx

FONT_LINK = "https://fonts.googleapis.com/css2?family=Roboto&display=swap"

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    FONT_LINK,
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
    dbc.icons.FONT_AWESOME,
    dbc.icons.BOOTSTRAP,
]

config = {
    "displaylogo": False,
    "modeBarButtonsToAdd": [
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
    ],
    "responsive": True,
}

df_map = pd.read_csv("Datasets/map_indicators.csv", sep=";")
df_areas = pd.read_csv("Datasets/areas_score.csv", sep=";")


def get_plots(template):
    return [
        choroplet_score.graph(df_map, template=template),
        heat_area_action.graph(
            df_areas.copy(),
            template=template,
        ),
        internet_access.graph(
            df_areas.copy(),
            template=template,
        ),
        cpi_bar.graph(
            df_areas.copy(),
            template=template,
        ),
        summary.graph(
            template=template,
        ),
    ]


app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="GDB Challenge 2025",
    assets_folder="assets",
    update_title=None,
    suppress_callback_exceptions=True,
)

app.layout = dbc.Container(
    [
        dcc.Store(id="theme-store", data="dark"),
        html.Div(
            [
                html.H4(
                    "Data Reality in Latin America and the Caribbean: Insights and Opportunities",
                    id="header-title",
                    style={"fontWeight": "700"},
                    className="container pt-4 pb-1",
                ),
                html.Div(
                    [
                        dbc.Button(
                            html.I(className="fa-solid fa-circle-info"),
                            id="btn-info",
                            color="link",
                            className="me-2 p-0 text-secondary",
                            title="About",
                        ),
                        dbc.Button(
                            html.I(className="fa-solid fa-download"),
                            id="btn-download",
                            color="link",
                            className="me-2 px-1 p-0 text-secondary",
                            title="Datasets",
                        ),
                        dbc.Button(
                            html.I(className="fa-solid fa-expand"),
                            id="fullscreen-btn",
                            color="link",
                            className="me-2 p-0 text-secondary",
                            title="Fullscreen",
                        ),
                        dbc.Button(
                            html.I(id="icon-theme", className="fa-solid fa-moon"),
                            id="btn-theme-switch",
                            className="me-2 p-0 text-secondary",
                            color="link",
                            title="Theme",
                            n_clicks=0,
                        ),
                    ],
                    id="icon-buttons",
                    style={"display": "flex", "alignItems": "center"},
                    className="pt-1",
                ),
            ],
            id="header-container",
            style={
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "flex-start",
                "fontFamily": "'Roboto', sans-serif",
            },
            className="container",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Progress(
                            value=0,
                            style={"height": "4px"},
                            color="primary",
                            className="mb-1 w-100",
                            id="id-counter",
                        ),
                    ],
                    className="my-0 py-0 pb-1",
                    id="slider-plot-container",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Button(
                                            html.I(id="icon-prev"),
                                            className="rounded-pill btn-link px-0 col",
                                            id="prev",
                                            color="link",
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            html.I(id="icon-next"),
                                            className="rounded-pill btn-link px-0 col my-0 py-0",
                                            id="next",
                                            color="link",
                                            n_clicks=0,
                                        ),
                                    ],
                                    className="row py-0 my-0 flex",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Small(
                                                    id="count-plot",
                                                    className="text-start mx-3 fw-bold my-0 py-0",
                                                    style={"fontSize": "10px"},
                                                ),
                                            ],
                                            className="py-0 my-0",
                                        ),
                                    ],
                                    className="d-flex py-0 my-0 container",
                                    id="sub-controls-container",
                                ),
                            ],
                            className="px-1",
                        ),
                        html.Div(
                            [
                                html.H5(
                                    id="title-plot",
                                    className="px-2 my-0 py-0 fw-bold pb-1 pt-1",
                                    style={"fontSize": "18px"},
                                ),
                                html.H6(
                                    id="sub-title-plot",
                                    className="px-2 my-0 py-0 text-wrap text-sm-nowrap",
                                    style={"fontSize": "14px", "width": "900px"},
                                ),
                            ],
                            className="my-0 px-3",
                        ),
                    ],
                    className="d-flex text-secondary my-0 py-0 container",
                    id="carousel-container",
                    style={"width": "100%"},
                ),
                html.Hr(className="container my-0 py-0 text-seecondary"),
            ],
            id="main-content-container",
            style={
                "width": "100%",
                "fontFamily": "'Roboto', sans-serif",
                "height": "100%",
                "width": "100%",
                "flexGrow": 1,
            },
            className="container pt-2 py-0 my-0 b",
        ),
        html.Div(
            [
                dcc.Loading(
                    id="id-plots",
                    color="#018E99",
                    type="cube",
                    style={"marginTop": "120px"},
                )
            ],
            id="plot-container",
            className="container ",
            style={
                "height": "100%",
                "width": "100%",
                "flexGrow": 1,
                "overflow": "auto",
            },
        ),
        html.Div(
            [
                html.Span("© - 2025 UD.", style={"flex": "1", "textAlign": "left"}),
                html.Span(
                    "Global Data Barometer - Data Visualization Challenge 2025",
                    style={"flex": "1", "textAlign": "right"},
                ),
            ],
            className="container",
            style={
                "fontSize": "12px",
                "color": "#888",
                "padding": "8px",
                "marginTop": "20px",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
            },
        ),
        dbc.Offcanvas(
            id="info-offcanvas",
            title="Global Data Barometer - Data Visualization Challenge 2025",
            placement="start",
            is_open=False,
            children=[
                html.Div(
                    [
                        html.P(
                            [
                                "The Global Data Barometer (GDB) is an independent project providing a snapshot of the state of data for public good worldwide. ",
                                html.A(
                                    "Learn more",
                                    href="https://globaldatabarometer.org",
                                    target="_blank",
                                ),
                                ".",
                            ],
                            className="small",
                        ),
                        html.H6("How to use this tool:", className="small fw-bold"),
                        html.Ul(
                            [
                                html.Li(
                                    [
                                        "Press the ",
                                        html.Span("▶️ forward", className="fw-bold"),
                                        " and ",
                                        html.Span("◀️ back", className="fw-bold"),
                                        " buttons to navigate between visualizations.",
                                    ]
                                ),
                                html.Li(
                                    [
                                        "Click ",
                                        html.Span("⬇️ Download", className="fw-bold"),
                                        " to access datasets.",
                                    ]
                                ),
                                html.Li(
                                    [
                                        "Use the ",
                                        html.Span(
                                            "🌙 / ☀️ theme toggle", className="fw-bold"
                                        ),
                                        " for better readability.",
                                    ]
                                ),
                                html.Li(
                                    [
                                        "Click ",
                                        html.Span("⛶ Fullscreen", className="fw-bold"),
                                        " for immersive visualization.",
                                    ]
                                ),
                                html.Li(
                                    [
                                        "Charts are ",
                                        html.Span("interactive", className="fw-bold"),
                                        ": zoom, hover, and explore data details.",
                                    ]
                                ),
                            ],
                            className="small",
                        ),
                        html.P(
                            "Official results are available directly within this platform.",
                            className="small",
                        ),
                        html.P(
                            [
                                "Built with ",
                                html.Span("Dash", className="fw-bold"),
                                " and ",
                                html.Span("Plotly Python", className="fw-bold"),
                                " for interactive data visualization.",
                            ],
                            className="small",
                        ),
                    ]
                )
            ],
        ),
        dbc.Modal(
            id="download-modal",
            size="lg",
            is_open=False,
            centered=True,
            children=[
                dbc.ModalHeader(dbc.ModalTitle("Download Dataset", className="small")),
                dbc.ModalBody(
                    html.Div(
                        [
                            html.Ul(
                                [
                                    html.Li(
                                        "Global Data Barometer’s data exploration hub"
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Result by country"),
                                            html.Li("Data by Region"),
                                            html.Li("General scores"),
                                        ]
                                    ),
                                    html.Br(),
                                    html.Li("World Bank’s Open Data"),
                                    html.Ul(
                                        [
                                            html.Li(
                                                html.A(
                                                    "Individuals using the Internet",
                                                    href="https://data.worldbank.org/indicator/IT.NET.USER.ZS",
                                                    target="_blank",
                                                )
                                            ),
                                        ]
                                    ),
                                    html.Br(),
                                    html.Li("Transparency International"),
                                    html.Ul(
                                        [
                                            html.Li(
                                                html.A(
                                                    "Corruption Perceptions Index",
                                                    href="https://www.transparency.org/en/cpi/2024/index/dnk",
                                                    target="_blank",
                                                )
                                            ),
                                        ]
                                    ),
                                ]
                            )
                        ],
                        className="small",
                    )
                ),
                dbc.ModalFooter(
                    dbc.Alert(
                        [
                            "Global Data Barometer – To download, please visit the official site: ",
                            html.A(
                                "globaldatabarometer.org/explore-the-results/",
                                href="https://globaldatabarometer.org/explore-the-results/",
                                target="_blank",
                                className="alert-link",
                            ),
                        ],
                        color="warning",
                        className="mb-0 w-100 small",
                        dismissable=False,
                    )
                ),
            ],
        ),
    ],
    fluid=True,
    id="page-container",
    style={
        "backgroundColor": "#f8f9fa",
        "color": "#212529",
        "minHeight": "100vh",
        "maxHeight": "180vh",
        "fontFamily": "'Roboto', sans-serif",
        "height": "100%",
        "width": "100%",
        "flexGrow": 1,
    },
)


@app.callback(
    [
        Output("id-plots", "children"),
        Output("title-plot", "children"),
        Output("sub-title-plot", "children"),
        Output("prev", "disabled"),
        Output("next", "disabled"),
        Output("count-plot", "children"),
        Output("prev", "n_clicks"),
        Output("next", "n_clicks"),
        Output("id-counter", "value"),
        Output("page-container", "style"),
        Output("header-title", "style"),
        Output("icon-prev", "className"),
        Output("icon-next", "className"),
        Output("icon-theme", "className"),
    ],
    [
        Input("prev", "n_clicks"),
        Input("next", "n_clicks"),
        Input("btn-theme-switch", "n_clicks"),
        Input("btn-info", "n_clicks"),
        Input("btn-download", "n_clicks"),
    ],
    [
        State("prev", "n_clicks"),
        State("next", "n_clicks"),
        State("id-counter", "value"),
        State("page-container", "style"),
        State("header-title", "style"),
    ],
)
def update_ui(
    prev_clicks,
    next_clicks,
    switch_value,
    info_clicks,
    download_clicks,
    prev_state,
    next_state,
    progress_val,
    page_style,
    header_style,
):
    if switch_value is None:
        switch_value = 0
    theme = "light" if switch_value % 2 == 0 else "dark"
    template = "plotly_dark" if theme == "dark" else "plotly"
    plots = get_plots(template)
    max_index = len(plots) - 1

    trigger_id = ctx.triggered_id
    index = int(round((progress_val / 100) * len(plots))) - 1 if progress_val else 0
    index = max(0, min(index, max_index))

    if trigger_id == "next" and index < max_index:
        index += 1
    elif trigger_id == "prev" and index > 0:
        index -= 1

    active_prev = index == 0
    active_next = index == max_index

    progreso_porcentual = ((index + 1) / len(plots)) * 100
    count_text = f"{index + 1} of {len(plots)}"

    page_bg = "#121212" if theme == "dark" else "#f8f9fa"
    text_color = "white" if theme == "dark" else "#212529"

    new_page_style = page_style.copy() if page_style else {}
    new_page_style.update({"backgroundColor": page_bg, "color": text_color})

    new_header_style = header_style.copy() if header_style else {}
    new_header_style.update({"color": text_color, "fontWeight": "700"})

    prev_class = f"fa-solid fa-circle-arrow-left fa-xl {'text-white' if theme == 'dark' else 'text-dark'}"
    next_class = f"fa-solid fa-circle-arrow-right fa-3x {'text-white' if theme == 'dark' else 'text-dark'}"
    icon_theme = "fa-solid fa-moon" if theme == "dark" else "fa-solid fa-sun"

    return (
        html.Div(
            [
                dcc.Graph(
                    figure=plots[index][0],
                    config=config,
                    style={"height": "100%", "width": "100%"},
                )
            ],
            className="flex-grow-1 d-flex overflow-auto p-2",
            style={"height": "100%", "width": "100%"},
        ),
        plots[index][1],
        plots[index][2],
        active_prev,
        active_next,
        count_text,
        prev_clicks,
        next_clicks,
        progreso_porcentual,
        new_page_style,
        new_header_style,
        prev_class,
        next_class,
        icon_theme,
    )


@app.callback(
    Output("info-offcanvas", "is_open"),
    Input("btn-info", "n_clicks"),
    State("info-offcanvas", "is_open"),
)
def toggle_info_offcanvas(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("download-modal", "is_open"),
    Input("btn-download", "n_clicks"),
    State("download-modal", "is_open"),
)
def toggle_download_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


server = app.server

if __name__ == "__main__":
    app.run(debug=True)
