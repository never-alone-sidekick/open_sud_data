"""
Open SUD Data - Dash Web Application

A data visualization dashboard for substance use disorder data
from open public databases.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Open SUD Data",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

server = app.server

app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(
                    dbc.NavLink("About", href="/about"),
                ),
            ],
            brand="Open SUD Data",
            brand_href="/",
            color="primary",
            dark=True,
            className="mb-4",
        ),
        dash.page_container,
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)
