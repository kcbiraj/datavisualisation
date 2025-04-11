import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Automobile Statistics Dashboard"

# List of years
year_list = sorted(data["Year"].unique())

# App Layout
app.layout = html.Div(
    [
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "30px"},
        ),
        dcc.Tabs(
            id="tabs",
            value="Yearly Statistics",
            children=[
                dcc.Tab(label="Yearly Statistics", value="Yearly Statistics"),
                dcc.Tab(
                    label="Recession Period Statistics",
                    value="Recession Period Statistics",
                ),
            ],
            style={"fontSize": "18px"},
        ),
        html.Div(id="controls-container"),
        html.Div(id="charts-container"),
    ],
    style={"padding": "20px", "fontFamily": "Arial, sans-serif"},
)


# Callback for controls based on tab selection
@app.callback(Output("controls-container", "children"), Input("tabs", "value"))
def render_controls(tab):
    if tab == "Yearly Statistics":
        return html.Div(
            [
                html.Label("Select a Year:"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{"label": str(year), "value": year} for year in year_list],
                    value=year_list[0],
                    style={"width": "50%"},
                ),
            ]
        )
    return None


# Callback to render charts
@app.callback(
    Output("charts-container", "children"),
    [Input("tabs", "value"), Input("year-dropdown", "value")],
    prevent_initial_call=True,
)
def render_charts(tab, selected_year):
    if tab == "Yearly Statistics" and selected_year:
        yearly_data = data[data["Year"] == selected_year]

        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        monthly_sales = (
            yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        )
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        )
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        return html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.line(
                                yas,
                                x="Year",
                                y="Automobile_Sales",
                                title="Yearly Average Sales",
                            )
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.line(
                                monthly_sales,
                                x="Month",
                                y="Automobile_Sales",
                                title=f"Monthly Sales in {selected_year}",
                            )
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.bar(
                                avr_vdata,
                                x="Vehicle_Type",
                                y="Automobile_Sales",
                                title="Avg. Vehicles Sold by Type",
                            )
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.pie(
                                exp_data,
                                values="Advertising_Expenditure",
                                names="Vehicle_Type",
                                title="Ad Expenditure by Vehicle Type",
                            )
                        )
                    ],
                    className="card",
                ),
            ],
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
        )

    elif tab == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        )
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        unemployment_data = (
            recession_data.groupby("Vehicle_Type")["unemployment_rate"]
            .mean()
            .reset_index()
        )

        return html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.line(
                                yearly_rec,
                                x="Year",
                                y="Automobile_Sales",
                                title="Sales During Recession Years",
                            )
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.bar(
                                average_sales,
                                x="Vehicle_Type",
                                y="Automobile_Sales",
                                title="Avg Sales by Type During Recession",
                            )
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.pie(
                                exp_rec,
                                values="Advertising_Expenditure",
                                names="Vehicle_Type",
                                title="Ad Spend During Recession",
                            )
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            figure=px.bar(
                                unemployment_data,
                                x="Vehicle_Type",
                                y="unemployment_rate",
                                title="Unemployment Rate by Vehicle Type",
                            )
                        )
                    ],
                    className="card",
                ),
            ],
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px"},
        )

    return None


# CSS-style card-like layout (if using external CSS this can be removed)
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .card {
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Run app
if __name__ == "__main__":
    app.run(debug=True)
