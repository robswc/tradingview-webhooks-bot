import dash_html_components as html
from dash.dependencies import Output
from dash_core_components import Input
import dash_core_components as dcc

from components.settings import interface_base


class EventTile:
    def __init__(self, event):
        self.event = event

    def render(self):
        """
        Renders event tile object.
        :return: rendered event tile object.
        """
        table_data = []
        action_list = [html.Li(str(a.name), className='badge bg-success') for a in self.event.actions]
        if action_list == []:
            action_list = html.A('No actions found (click to learn how to add actions)',
                                 href='https://github.com/robswc/tradingview-webhooks-bot/wiki/Adding-actions-to-event')
        tile = html.Div(
            children=[
                html.Header(
                    children=[
                        html.H3(self.event.name), html.Details(
                            [html.Summary('key'), self.event.key]
                            , className='muted', style={'paddingLeft': '1rem'}),

                    ],
                    className='flex-h'
                ),
                html.Hr(),
                html.Div([html.H5('Actions'), html.Div('all', className='header-subtitle')],
                         className='header-container'),
                html.Ul(action_list, className='no-style-list'),
                html.Div([html.H5('Data'), html.Div('latest', className='header-subtitle')],
                         className='header-container'),
                dcc.Link('Data Table', href='datatable/{}'.format(self.event.name), className='badge bg-info',
                         refresh=True),
                html.P(),
                html.Div([html.H5('Log'), html.Div('clear', className='header-subtitle')],
                         className='header-container'),
                html.Div([html.Div(line) for line in reversed(self.event.get_log()[-25:])], className='log-area')
            ],
            className='tile shadow'
        )
        return tile
