import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf
import os
from dotenv import load_dotenv


app = dash.Dash(__name__)

load_dotenv()
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
col = db["companies"]

company_list = []
get_tickers = col.find({}, {"data.ticker": 1, "_id": 0})

for tick in get_tickers:
    company_list.append(
        {"label": tick["data"]["ticker"], "value": tick["data"]["ticker"]}
    )


# print(company_list)


# df = create_df("FESCO")


app.layout = html.Div(
    [
        html.H1(children="JAMAICA STOCK EXCHANGE CHARTS"),
        html.Div("A web application to view data from the Jamaica Stock Exchange."),
        html.Label("Select a company"),
        dcc.Dropdown(
            id="drop-selection",
            options=company_list,
            value="138SL",
        ),
        html.Label("Select type of graph"),
        dcc.RadioItems(
            id="chart-type",
            options=[
                {"label": "Line", "value": "line"},
                {"label": "Candle Stick", "value": "candle"},
                {"label": "OHLC", "value": "ohlc"},
            ],
            value="line",
        ),
        dcc.Graph(id="stock-chart"),
    ]
)


@app.callback(
    Output("stock-chart", "figure"),
    Input("drop-selection", "value"),
    Input("chart-type", "value"),
)
def update_ticker(ticker, chart_type):
    items = col.find({"data.ticker": ticker}, {"pv": 1, "_id": 0})
    df = pd.DataFrame(
        data=list(items)[0]["pv"],
        columns=("unix_date", "open", "high", "low", "close", "volume"),
    )
    df["date"] = pd.to_datetime(df["unix_date"], unit="ms")
    # df.set_index("unix_date", inplace=True)

    if chart_type == "line":
        return go.Figure(
            data=[
                go.Scatter(
                    x=df.date, y=df.close, mode="lines+markers", name="lines+markers"
                )
            ]
        )
    elif chart_type == "candle":
        return go.Figure(
            data=[
                go.Candlestick(
                    x=df.date, open=df.open, high=df.high, low=df.low, close=df.close
                )
            ]
        )
    elif chart_type == "ohlc":
        return go.Figure(
            data=[
                go.Ohlc(
                    x=df.date, open=df.open, high=df.high, low=df.low, close=df.close
                )
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)
