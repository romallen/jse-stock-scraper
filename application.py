import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pandas_ta as ta
import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "JSE CHART VIEWER"

uri = os.environ.get("DB_URL") or os.environ.get("MONGODB_URI")
load_dotenv()

client = pymongo.MongoClient(uri)

db = client["jse"]
col = db["companies"]

company_list = []
get_tickers = col.find({}, {"data.ticker": 1, "_id": 0})

for tick in get_tickers:
    company_list.append(
        {"label": tick["data"]["ticker"], "value": tick["data"]["ticker"]}
    )


# df = create_df("FESCO")

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    "JAMAICA STOCK EXCHANGE CHARTS",
                ),
            ],
            className="banners",
        ),
        html.Div(
            "A web application to view data from the Jamaica Stock Exchange.",
            className="banners",
        ),
        html.Div(
            children=[
                html.Label("Select a company:"),
                dcc.Dropdown(
                    id="drop-selection",
                    options=company_list,
                    value="138SL",
                ),
            ]
        ),
        html.Div(
            children=[
                html.Label("Select a chart type:"),
                dcc.RadioItems(
                    id="chart-type",
                    options=[
                        {"label": "Line", "value": "line"},
                        {"label": "Candle Stick", "value": "candle"},
                        {"label": "OHLC", "value": "ohlc"},
                    ],
                    value="line",
                ),
            ]
        ),
        dcc.Graph(id="stock-chart"),
    ],
    className="container",
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
    df["date"] = pd.to_datetime(df["unix_date"], origin="unix", unit="ms")
    df.set_index("unix_date", inplace=True)
    # print(df.tail(1).date)

    df["rsi_10"] = ta.rsi(close=df.close, length=10)
    df["sma_10"] = df.ta.sma(10)
    df["sma_50"] = df.ta.sma(50)
    df["sma_100"] = df.ta.sma(100)
    df["ema_10"] = ta.ema(close=df.close, length=10)
    df["ema_10"] = ta.ema(close=df.close, length=10)
    df["ema_50"] = ta.ema(close=df.close, length=50)
    df["ema_200"] = ta.ema(close=df.close, length=200)
    initial_range = [
        (datetime.today() - relativedelta(months=+3)).strftime("%Y-%m-%d"),
        datetime.today().strftime("%Y-%m-%d"),
    ]
    # print(df)
    layout = dict(
        height=550,
        # width="80%",
        title=ticker,
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
            range=initial_range,
        ),
    )

    if chart_type == "line":
        return go.Figure(
            data=[
                go.Scatter(x=df.date, y=df.close, yaxis="y1", name="close"),
                # go.Bar(x=df.date, y=df.volume, yaxis="y2", name="Volume"),
            ],
            layout=layout,
        )
    elif chart_type == "candle":
        return go.Figure(
            data=[
                go.Candlestick(
                    x=df.date, open=df.open, high=df.high, low=df.low, close=df.close
                )
            ],
            layout=layout,
        )
    elif chart_type == "ohlc":
        return go.Figure(
            data=[
                go.Ohlc(
                    x=df.date, open=df.open, high=df.high, low=df.low, close=df.close
                )
            ],
            layout=layout,
        )


if __name__ == "__main__":
    app.run_server(debug=True)
