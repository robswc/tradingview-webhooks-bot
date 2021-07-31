import ast
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate

from components.event_interface import ei
from components.data_table import di
from bot import bot
from components.dash_app import app
from components.settings import interface_base

# set events
ei.events = bot.events

# set data tables
di.create_tables(bot.events)

# set nav elements
nav_elements = [dcc.Link('Event Dashboard', href='/{}/events'.format(interface_base), refresh=True)]

app.title = 'Tradingview-Webhooksbot'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Ul([html.Li(item, className='nav-item nav-link link-item') for item in nav_elements],
            className='navbar-nav navbar-dark bg-dark navbar-expand-lg navbar'),

    html.Br(),
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,
        n_intervals=0
    ),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname'),
               dash.dependencies.Input('interval-component', 'n_intervals')])
def display_page(pathname, n_intervals):
    content = html.Div([
        html.Div([
            html.Div([
                html.H1('Tradingview-Webhooksbot Interface'),
                html.Hr(),
                html.P('Welcome to the TVWB GUI.  Using the interface can help you organize your actions and events!'),
                html.A('Visit the Github Wiki for more info!',
                       href='https://github.com/robswc/tradingview-webhooks-bot/wiki/Interface-GUI'),
                html.Hr(),
                html.H1('Index'),
                html.A('Event Dashboard', href='/interface/events')
            ])
        ], className='row')
    ], className='container')

    if pathname == '/{}/events'.format(interface_base):
        content = html.Div(ei.render_events(), className='tile-container')

    if pathname.split('/')[2] == 'datatable':
        content = html.Div(di.get_event_table(pathname.split('/')[3]).render(), className='container')

    return html.Div(content)


# datatable confirmation callback
@app.callback(
    Output('null', 'children'),
    Input({'type': 'confirmation-action', 'action': ALL, 'tid': ALL, 'event': ALL}, 'n_clicks')
)
def display_output(values):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0].replace("'", '"')
    # if the trigger is a confirmation button
    if trigger:
        trigger = json.loads(trigger)
        # reject
        if trigger.get('action') == 'reject':
            ei.get(trigger.get('event')).reject(trigger.get('tid'))
        # confirm
        if trigger.get('action') == 'confirm':
            ei.get(trigger.get('event')).confirm(trigger.get('tid'))

    raise PreventUpdate()


server = app.server
# set server
if __name__ == '__main__':
    app.run_server(debug=True)
