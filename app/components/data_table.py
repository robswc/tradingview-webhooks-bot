import dash_html_components as html
import dash_core_components as dcc


class DataTableInterface:
    def __init__(self):
        self.data_tables = []

    def create_tables(self, events):
        for event in events:
            self.data_tables.append(DataTable(event))

    def get_event_table(self, event_name):
        """
        Gets a datatable with event, given name.
        :param event_name:
        :return:
        """
        for table in self.data_tables:
            if table.event.name == event_name:
                return table


class DataTable:
    def __init__(self, event):
        self.event = event

    def render(self):
        def render_td(idx, t_data, tid):
            # special key 'confirmation', handles rendering of confirmation button.
            if table_data.get('headers')[idx] == 'confirmation':
                if tid in self.event.confirmation_queue.keys():
                    return html.Div([html.Button('Confirm', className='btn btn-success', style={'marginRight': '1rem'},
                                                 id={'type': 'confirmation-action', 'action': 'confirm', 'tid': tid,
                                                     'event': self.event.name}),
                                     html.Button('Reject', className='btn btn-danger',
                                                 id={'type': 'confirmation-action', 'action': 'reject', 'tid': tid,
                                                     'event': self.event.name})])
                else:
                    return html.Div('Processed', className='bg-info p-1', style={'textAlign': 'center'})

            # if no special just render td normally
            return t_data

        # start render
        data = self.event.format_trigger_log()
        if data is None:
            return [
                html.Div('Event has not been triggered yet!'),
                html.Hr(),
                dcc.Link('Refresh', className='btn btn-primary', refresh=True, href='')
            ]

        tables = []
        for table_data in data:
            def is_key(idx):
                return table_data.get('headers')[idx] == 'key'

            table_header = html.Tr([html.Th(i) for i in table_data.get('headers')])
            table_rows = [
                html.Tr(
                    [html.Td(render_td(idx, j, i[-1]), className='td-key' if is_key(idx) else 'td-normal') for idx, j in
                     enumerate(i)]) for
                i in table_data.get('rows')]

            tables.append(
                html.Table([html.Thead(table_header), html.Tbody(table_rows)], className='table table-striped')
            )

        return html.Div(

            children=[
                html.Div(id='null'),
                html.Div(self.event.confirmation_queue),
                dcc.Interval(
                    id='interval-component',
                    interval=10 * 1000,
                    n_intervals=0
                ),
                html.Div([
                    html.Div([
                        html.H1('{} - {}'.format(self.event.name, 'datatable')),
                        html.H2('(Session)', className='text-muted')
                    ], className='card-header',
                        style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                    html.Div(tables, className='card-body'),
                    html.I('Warning: Reloading the server will clear data table content.',
                           className='text-muted card-footer')
                ], className='card')
            ]
        )


di = DataTableInterface()
