# -*- coding: utf-8 -*-
import dash.exceptions
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from flask_caching import Cache
import pandas as pd
import datetime
import uuid
import json
from lookups import countries
from scrape_players import get_players, get_player_stats_dfs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = Dash(__name__, external_stylesheets=external_stylesheets)
cache = Cache(dash_app.server, config={
    # 'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 50
})


def get_dataframe(session_id):
    @cache.memoize()
    def query_and_serialize_data(session_id):
        # expensive or user/session-unique data processing step goes here
        # simulate a user/session-unique data processing step by generating
        # data that is dependent on time
        now = datetime.datetime.now()
        countries_players = {country: get_players(country) for country in countries.keys()}
        return json.dumps(countries_players)

    return pd.read_json(query_and_serialize_data(session_id))


def serve_layout():
    session_id = str(uuid.uuid4())

    dash_app.layout = html.Div(
        html.Div([html.Div(dcc.Store(data=session_id, id='session-id')),
                  html.Div([html.H1(children='Cricket-Players-Basic-Viz', className='nine columns'),
                            html.H5(children='Data sourced from Cric-info', className='three columns',
                                    style={'margin-right': '10', 'color': 'green'})], className='row'),
                  html.Div([html.Div([
                      html.P('Choose Country'),
                      dcc.Dropdown(
                          id='countries',
                          options=[{'label': i, 'value': i} for i in countries.keys()],
                          value='india')], style={'margin-top': '10'}, className='six columns'
                  )]),
                  html.Div([
                      html.Div(
                          [html.P('Choose Player'),
                           dcc.Dropdown(
                               id='players',
                               # options=[{'label': i, 'value': i} for i in countries.keys()],
                               value='Virat Kohli')], style={'margin-top': '10'}, className='six columns'
                      )], className='row'),

                  html.Div([html.Div([dcc.Graph(id='example-graph1', className='six columns'),
                                      dcc.Graph(id='example-graph2', className='six columns')], className='row')
                            ]),
                  # ], className='ten columns offset-by-one')
                  html.Div([html.Div([dcc.Graph(id='example-graph3', className='six columns'),
                                      dcc.Graph(id='example-graph4', className='six columns')],
                                     className='row')
                            ])
                  ], className='row')
    )
    return dash_app.layout


dash_app.layout = serve_layout


@dash_app.callback(
    Output('players', 'options'),
    [Input('countries', 'value'),
     Input('session-id', 'data')])
def set_players_for_country(selected_country, session_id):
    # current_players = get_players(selected_country, current=1, alltime=0)
    if selected_country:
        current_players = get_dataframe(session_id)
        current_players1 = current_players.loc[current_players[selected_country].notnull()].index
        # return [{'label': i, 'value': i} for i in current_players.keys()]
        return [{'label': i, 'value': i} for i in current_players1]
    else:
        raise dash.exceptions.PreventUpdate


@dash_app.callback(
    [Output('example-graph1', 'figure'),
     Output('example-graph2', 'figure'),
     Output('example-graph3', 'figure'),
     Output('example-graph4', 'figure')],
    [Input('countries', 'value'),
     Input('players', 'value'),
     Input('session-id', 'data')])
def update_graph1(selected_country, selected_player, session_id):
    if selected_country:
        data1 = []
        data2 = []
        # players = get_players(selected_country)
        pl_df = get_dataframe(session_id)
        players = pl_df.loc[pl_df[selected_country].notnull(), selected_country].to_dict()
        if selected_player in players:
            df = get_player_stats_dfs(selected_country, players=players, pid=players[selected_player], wtf=False)
            df_odi = df[df.MatchType.isin(['ODI', 'WODI'])]
            df_test = df[df.MatchType.isin(['Test', 'WTest'])]
            df_t20 = df[df.MatchType.isin(['T20I', 'WT20I'])]
            data1 = [{'x': df_odi.year, 'y': df_odi.Runs, 'type': 'bar', 'name': 'ODI'},
                     {'x': df_test.year, 'y': df_test.Runs, 'type': 'bar', 'name': 'TEST'},
                     {'x': df_t20.year, 'y': df_t20.Runs, 'type': 'bar', 'name': 'T20I'}]
            figure1 = {
                'data': data1,
                'layout': {
                    'title': "{} Runs Bar Plot".format(selected_player),
                    'xaxis': dict(
                        title='Year',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=15,
                            color='#7f7f7f'
                        )),
                    'yaxis': dict(
                        title='Total Runs',
                        titlefont=dict(
                            family='Helvetica, monospace',
                            size=15,
                            color='#7f7f7f'
                        )
                    )
                }
            }
            data2 = [{'x': df_odi.year, 'y': df_odi.Wkts, 'type': 'bar', 'name': 'ODI'},
                     {'x': df_test.year, 'y': df_test.Wkts, 'type': 'bar', 'name': 'TEST'},
                     {'x': df_t20.year, 'y': df_t20.Wkts, 'type': 'bar', 'name': 'T20I'}]
            figure2 = {
                'data': data2,
                'layout': {
                    'title': "{} Wkts Bar Plot".format(selected_player),
                    'xaxis': dict(
                        title='Year',
                        titlefont=dict(
                            family='Courier New, monospace',
                            size=15,
                            color='#7f7f7f'
                        )),
                    'yaxis': dict(
                        title='Total Wickets',
                        titlefont=dict(
                            family='Helvetica, monospace',
                            size=15,
                            color='#7f7f7f'
                        ))
                }
            }
            figure3 = px.scatter(df, x="Opposition", y="Runs", color="year", size='Runs', title="{} Runs Scatter Plot".
                                 format(selected_player),
                                 width=900, height=700)
            figure4 = px.scatter(df, x="Opposition", y="Wkts", color="year", size='Wkts', title="{} Wickets Scatter Plot".
                                 format(selected_player),
                                 width=900, height=700)
            return figure1, figure2, figure3, figure4
        else:
            raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    dash_app.run_server(debug=True)
