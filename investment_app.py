# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from eda import heroku_eda
from eda import get_ma_df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Query data
df = heroku_eda()

app.layout = html.Div(children=[
    html.H1(children='Investment Portfolio'),

    html.H4(children='''
        Choose company name & moving average method:
    '''),

    html.Div([

    dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x}
                     for x in df['name'].unique()],
        value=df['name'][1],
        clearable=True,
    ),

    html.H4('Select Operation:'),
    dcc.RadioItems(
        id='operations',
        options=[
            {'label': 'Moving Averages', 'value': 'MA'},
            {'label': 'ML Predictions', 'value': 'ML'}
        ],
        value='MA'
    ),

    html.Div([
            # html.H4('Select Moving Average Method:'),
            dcc.Dropdown(
                id="moving_avg",
                options=[{"label": x, "value": x}
                             for x in ['Weighted Moving Average',
                                       'Exponential Moving Average',
                                       'Simple Moving Average']],
                value='Simple Moving Average',
                clearable=True,
            )
            ], style={'display':'block'}),

    html.Div([
            # html.H6('Short-term Period {9 to 22}'),
            dcc.Input(
                id="period_1",
                type="number",
                placeholder="Short term period",
                min=9,
                max=22,
                value=9
            )
            ], style={'display':'block'}),

    html.Div([
            # html.H6('Short-term Period {11 to 24}'),
            dcc.Input(
                id="period_2",
                type="number",
                placeholder="Long term period",
                min=11,
                max=24,
                value=11
            )
            ], style={'display':'block'}),

        dcc.Graph(id="time-series-chart"),
        dcc.Graph(id="candlestick-chart"),

    ])

])

@app.callback(
    Output('moving_avg', 'style'),
    [Input('operations', 'value')])
def show_hide_elements(visibility_state):
    if visibility_state == 'MA':
        return {'display': 'block'}
    if visibility_state == 'ML':
        return {'display': 'none'}

@app.callback(
    Output('period_1', 'style'),
    [Input('operations', 'value')])
def show_hide_elements(visibility_state):
    if visibility_state == 'MA':
        return {'display': 'block'}
    if visibility_state == 'ML':
        return {'display': 'none'}

@app.callback(
    Output('period_2', 'style'),
    [Input('operations', 'value')])
def show_hide_elements(visibility_state):
    if visibility_state == 'MA':
        return {'display': 'block'}
    if visibility_state == 'ML':
        return {'display': 'none'}

@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"),
    Input("moving_avg", "value"),
    Input("period_1", "value"),
    Input("period_2", "value"),
    Input('operations', 'value'))
def display_time_series(ticker, moving_avg, period_1, period_2, operations):

    temp = df.loc[df['name']==ticker].copy()
    temp = get_ma_df(temp, 'high', period_1, period_2)

    if operations=='MA':
        if moving_avg=='Weighted Moving Average':
            fig = px.line(temp, x='date', y=['high', 'wma_{}'.format(period_1), 'wma_{}'.format(period_2)])
        elif moving_avg=='Exponential Moving Average':
            fig = px.line(temp, x='date', y=['high', 'ema_{}'.format(period_1), 'ema_{}'.format(period_2)])
        else:
            fig = px.line(temp, x='date', y=['high', 'sma_{}'.format(period_1), 'sma_{}'.format(period_2)])
    elif operations=='ML':
        fig = px.line(temp, x='date', y='high')

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        yaxis_title="{} - High ($)".format(ticker)
    )

    return fig

@app.callback(
    Output("candlestick-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):
    temp = df.loc[df['name']==ticker].copy()
    fig_1 = go.Figure(data=[go.Candlestick(x=temp['date'],
                      open=temp['open'], high=temp['high'],
                      low=temp['low'], close=temp['close'])
                      ])

    fig_1.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig_1.update_layout(
        yaxis_title="{} - Stock Price ($)".format(ticker)
    )

    return fig_1

if __name__ == '__main__':
    app.run_server(debug=True)
