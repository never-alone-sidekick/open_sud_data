"""Home page - overview of available datasets."""

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Home")

layout = dbc.Container(
    [
        html.H1("Open SUD Data", className="mt-3"),
        html.P(
            "Exploring publicly available data on substance use disorder "
            "in the United States and beyond.",
            className="lead",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Data Sources"),
                            dbc.CardBody(
                                html.P(
                                    "Scrapers and pipelines that collect data from "
                                    "SAMHSA, CDC WONDER, NSDUH, and other open databases."
                                )
                            ),
                        ]
                    ),
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Visualizations"),
                            dbc.CardBody(
                                html.P(
                                    "Interactive charts and maps built with Plotly "
                                    "to explore trends in substance use disorder data."
                                )
                            ),
                        ]
                    ),
                    md=4,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Notebooks"),
                            dbc.CardBody(
                                html.P(
                                    "Jupyter notebooks documenting data analysis, "
                                    "methodology, and findings."
                                )
                            ),
                        ]
                    ),
                    md=4,
                ),
            ]
        ),
    ]
)
