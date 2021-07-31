import dash

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                requests_pathname_prefix="/interface/",
                external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css'])
server = app.server
