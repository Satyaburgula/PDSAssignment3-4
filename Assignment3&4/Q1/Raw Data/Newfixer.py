import requests
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__)

# Define Fixer.io API endpoint and your API access key
API_KEY = "40826a1371121d0d3e1145778b7c659d"
BASE_URL = "http://data.fixer.io/api/latest"
PARAMS = {"access_key": API_KEY}

# Fetch data from Fixer.io API
def fetch_data():
    try:
        response = requests.get(BASE_URL, params=PARAMS)
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching data:", e)
        return None

# Create Dash layout
app.layout = html.Div([
    html.H1("Currency Exchange Rates"),
    html.Div(id='live-update-text'),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])

# Update currency rates every 10 seconds
@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_currency_rates(n):
    data = fetch_data()
    if data:
        rates = data.get('rates')
        if rates:
            return html.Div([
                html.P(f"{currency}: {rate}") for currency, rate in rates.items()
            ])
        else:
            return "No currency data available."
    else:
        return "Failed to fetch currency data. Check your API key and internet connection."


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
