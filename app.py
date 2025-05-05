import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import os
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# Rest of your app code remains the same...
# [Keep all your existing layout and callback code]
# Custom colors
colors = {
    'background': '#121212',
    'text': '#FFFFFF',
    'gold': '#FFD700',
    'card': '#1E1E1E'
}

# Top 20 cryptocurrencies
CRYPTO_LIST = [
    {'label': 'Bitcoin (BTC)', 'value': 'bitcoin'},
    {'label': 'Ethereum (ETH)', 'value': 'ethereum'},
    {'label': 'Tether (USDT)', 'value': 'tether'},
    {'label': 'BNB (BNB)', 'value': 'binancecoin'},
    {'label': 'Solana (SOL)', 'value': 'solana'},
    {'label': 'XRP (XRP)', 'value': 'ripple'},
    {'label': 'USDC (USDC)', 'value': 'usd-coin'},
    {'label': 'Cardano (ADA)', 'value': 'cardano'},
    {'label': 'Dogecoin (DOGE)', 'value': 'dogecoin'},
    {'label': 'Shiba Inu (SHIB)', 'value': 'shiba-inu'},
    {'label': 'Avalanche (AVAX)', 'value': 'avalanche-2'},
    {'label': 'Polkadot (DOT)', 'value': 'polkadot'},
    {'label': 'TRON (TRX)', 'value': 'tron'},
    {'label': 'Chainlink (LINK)', 'value': 'chainlink'},
    {'label': 'Polygon (MATIC)', 'value': 'matic-network'},
    {'label': 'Toncoin (TON)', 'value': 'toncoin'},
    {'label': 'Bitcoin Cash (BCH)', 'value': 'bitcoin-cash'},
    {'label': 'Litecoin (LTC)', 'value': 'litecoin'},
    {'label': 'Uniswap (UNI)', 'value': 'uniswap'},
    {'label': 'Dai (DAI)', 'value': 'dai'}
]

# Navigation Bar
navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                    dbc.Col(dbc.NavbarBrand("CRYPTO PREDICT PRO", className="ml-2")),
                ],
                align="center",
                className="g-0",
            ),
            href="#home",
            style={"textDecoration": "none"},
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="#home", id="home-link"),
                    dbc.NavLink("Market Data", href="#market-data", id="market-data-link"),
                    dbc.NavLink("About", href="#about", id="about-link"),
                ],
                className="ml-auto",
                navbar=True,
            ),
            id="navbar-collapse",
            navbar=True,
        ),
    ],
    color="dark",
    dark=True,
    sticky="top",
)

# Main Dashboard Content
main_content = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Cryptocurrency Selection", style={
                    'backgroundColor': colors['gold'],
                    'color': 'black',
                    'fontWeight': 'bold'
                }),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='crypto-selector',
                        options=CRYPTO_LIST,
                        value='bitcoin',
                        clearable=False,
                        style={'color': 'black'}
                    ),
                    html.Div(id='current-price', className="mt-3", style={
                        'fontSize': '24px',
                        'color': colors['gold']
                    })
                ])
            ], className="mb-4", style={'backgroundColor': colors['card']}),
            
            dbc.Card([
                dbc.CardHeader("Price Prediction", style={
                    'backgroundColor': colors['gold'],
                    'color': 'black',
                    'fontWeight': 'bold'
                }),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Predict Next 30 Days", 
                                      id="predict-button", 
                                      color="warning",
                                      className="w-100")
                        ], width=6),
                        dbc.Col([
                            dcc.Dropdown(
                                id='model-selector',
                                options=[
                                    {'label': 'LSTM Model', 'value': 'lstm'},
                                    {'label': 'Linear Regression', 'value': 'linear'},
                                    {'label': 'Prophet', 'value': 'prophet'},
                                ],
                                value='lstm',
                                clearable=False
                            )
                        ], width=6)
                    ]),
                    dcc.Loading(
                        id="loading",
                        type="circle",
                        children=html.Div(id="loading-output"),
                        color=colors['gold']
                    ),
                    dcc.Graph(id="price-chart"),
                    dcc.Interval(
                        id='price-updater',
                        interval=60*1000,
                        n_intervals=0
                    )
                ])
            ], style={'backgroundColor': colors['card']}),
        ], width=12)
    ])
])

# Market Data Content
market_data_content = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Market Overview", style={
                    'backgroundColor': colors['gold'],
                    'color': 'black',
                    'fontWeight': 'bold'
                }),
                dbc.CardBody([
                    html.Div(id='market-data-table')
                ])
            ])
        ], width=12)
    ])
])

# About Page Content
about_content = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🔍 About CRYPTO PREDICT PRO", style={
                    'backgroundColor': colors['gold'],
                    'color': 'black',
                    'fontWeight': 'bold'
                }),
                dbc.CardBody([
                    dcc.Markdown('''
**CRYPTO PREDICT PRO** is a cryptocurrency price prediction dashboard powered by machine learning. 

---

### 🧠 Key Features
- 📈 Live cryptocurrency price charts (Top 20 coins)
- 🧮 ML-based future price predictions
- 📊 Interactive Plotly charts
- ☁️ Uses data from CoinGecko API
- 📡 Real-time updates every minute

### 🧰 Technology Stack
- **Frontend**: Dash, Plotly  
- **Backend**: Python, Pandas  
- **Machine Learning**: LSTM, Prophet  
- **Data**: CoinGecko API

### ⚠️ Disclaimer
This tool is for educational purposes only. Cryptocurrency investments are volatile - please do your own research.
                    ''')
                ])
            ], style={'backgroundColor': colors['card']})
        ], width=12)
    ])
])

# Main app layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0
    )
], fluid=True, style={'backgroundColor': colors['background'], 'minHeight': '100vh'})

# Callbacks
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'hash')]
)
def display_page(hash):
    if hash == '#market-data':
        return market_data_content
    elif hash == '#about':
        return about_content
    else:
        return main_content

@app.callback(
    Output('current-price', 'children'),
    [Input('crypto-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_current_price(selected_crypto, n):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={selected_crypto}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url).json()
        
        price = response[selected_crypto]['usd']
        change = response[selected_crypto]['usd_24h_change']
        change_color = '#2ECC71' if change >= 0 else '#E74C3C'
        
        display_name = next(item['label'] for item in CRYPTO_LIST if item['value'] == selected_crypto)
        
        return [
            html.Span(f"{display_name}: ", style={'fontWeight': 'bold'}),
            html.Span(f"${price:,.2f}", style={'fontWeight': 'bold'}),
            html.Span(f" ({change:.2f}%)", style={'color': change_color, 'marginLeft': '10px'})
        ]
    except:
        return "Loading current price..."

@app.callback(
    Output("price-chart", "figure"),
    [Input("predict-button", "n_clicks"),
     Input('crypto-selector', 'value'),
     Input("model-selector", "value")],
    [State('interval-component', 'n_intervals')]
)
def update_chart(n_clicks, selected_crypto, model_type, n):
    if n_clicks is None and n is None:
        raise PreventUpdate
        
    try:
        end_date = datetime.now().strftime('%d-%m-%Y')
        start_date = (datetime.now() - timedelta(days=365*2)).strftime('%d-%m-%Y')
        
        url = f"https://api.coingecko.com/api/v3/coins/{selected_crypto}/market_chart/range?vs_currency=usd&from={start_date}&to={end_date}"
        response = requests.get(url).json()
        
        prices = pd.DataFrame(response['prices'], columns=['timestamp', 'price'])
        prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
        prices.set_index('date', inplace=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=prices.index,
            y=prices['price'],
            name='Historical Price',
            line=dict(color=colors['gold'], width=2),
            hovertemplate='%{x|%b %d, %Y}<br>Price: $%{y:,.2f}<extra></extra>'
        ))
        
        if n_clicks:
            future_dates = [datetime.now() + timedelta(days=x) for x in range(30)]
            predicted_prices = [prices['price'].iloc[-1]] * 30  # Placeholder - replace with actual prediction
            
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=predicted_prices,
                name='Predicted Price',
                line=dict(color='#FFFFFF', dash='dot', width=2),
                hovertemplate='%{x|%b %d, %Y}<br>Predicted: $%{y:,.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            plot_bgcolor=colors['card'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            margin=dict(l=50, r=50, b=50, t=80, pad=4)
        )
        
        return fig
    except:
        return go.Figure()

@app.callback(
    Output('market-data-table', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_market_table(n):
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1"
        response = requests.get(url).json()
        
        table_header = [
            html.Thead(html.Tr([
                html.Th("Rank"),
                html.Th("Coin"),
                html.Th("Price"),
                html.Th("24h Change"),
                html.Th("Market Cap")
            ]))
        ]
        
        table_rows = []
        for coin in response:
            change = coin['price_change_percentage_24h']
            change_color = '#2ECC71' if change >= 0 else '#E74C3C'
            
            table_rows.append(html.Tr([
                html.Td(coin['market_cap_rank']),
                html.Td([
                    html.Img(src=coin['image'], height="20px", className="mr-2"),
                    html.Span(coin['name'])
                ]),
                html.Td(f"${coin['current_price']:,.2f}"),
                html.Td(f"{change:.2f}%", style={'color': change_color}),
                html.Td(f"${coin['market_cap']:,.0f}")
            ]))
        
        return dbc.Table(table_header + [html.Tbody(table_rows)], 
                        bordered=True, 
                        hover=True, 
                        responsive=True,
                        style={'color': colors['text']})
    except:
        return html.Div("Loading market data...", style={'color': colors['gold']})

if __name__ == '__main__':
    app.run(debug=True)