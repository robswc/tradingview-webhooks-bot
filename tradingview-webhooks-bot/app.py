import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import datetime

def get_log():
    log = []
    with open('logs/log.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            log.append(row)
    return log

app = dash.Dash('tradingview-webhooks')

app.layout = html.Div([

    html.Img(src='https://github.com/Robswc/tradingview-webhooks-bot/raw/master/img/webhooks_bot_logo.png', style={'height': 50}),
    html.Hr(),
    html.Div([
        html.Table(),
    ], id='alerts-table'),
    html.Div(id='app-frame'),
    dcc.Interval(
        id='app-update',
        interval=1000,
        n_intervals=0),
    ], className="container", style={'width': '100%', 'max-width': 50000})

@app.callback(dash.dependencies.Output('alerts-table', 'children'), [dash.dependencies.Input('app-update', 'n_intervals')])
def update_app(intervals):
    table = []
    for i in get_log():
        table.append(html.Tr(i))
    return table


if __name__ == '__main__':
    app.run_server(debug=True)