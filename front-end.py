import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load the sales data
data_path = 'data/daily_sales_data.csv' 
sales_data = pd.read_csv(data_path)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Sales, Price, and Quantity Data Over Time', style={'textAlign': 'center'}),

    dcc.Graph(id='sales-price-graph'),
    dcc.Graph(id='sales-quantity-graph'),  # Additional graph for sales and quantity

    html.Label('Select a Region:', style={'marginTop': 20}),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': 'All Regions', 'value': 'All'}] +
                [{'label': i, 'value': i} for i in sales_data['region'].unique()],
        value='All'
    )
])

@app.callback(
    [Output('sales-price-graph', 'figure'),
     Output('sales-quantity-graph', 'figure')],  # Two outputs for the two graphs
    [Input('region-dropdown', 'value')]
)
def update_graph(selected_region):
    if selected_region == 'All':
        filtered_data = sales_data
    else:
        filtered_data = sales_data[sales_data['region'] == selected_region]
    
    # Aggregating sales, price, and quantity by date
    aggregated_data = filtered_data.groupby('date').agg({'sales': 'sum', 'price': 'mean', 'quantity': 'sum'}).reset_index()

    # Sales and Price Graph
    sales_price_fig = go.Figure()

    sales_price_fig.add_trace(go.Scatter(x=aggregated_data['date'], y=aggregated_data['sales'],
                                         name='Sales', mode='lines+markers',
                                         line=dict(width=2, color='blue')))

    sales_price_fig.add_trace(go.Scatter(x=aggregated_data['date'], y=aggregated_data['price'],
                                         name='Price', mode='lines+markers',
                                         line=dict(width=2, color='red'), yaxis='y2'))

    sales_price_fig.update_layout(
        title=f'Sales and Price Over Time {"Across All Regions" if selected_region == "All" else "in " + selected_region}',
        xaxis_title='Date',
        yaxis_title='Sales',
        yaxis2=dict(
            title='Price',
            overlaying='y',
            side='right'
        ),
        margin=dict(l=100, r=100, t=100, b=50),
        hovermode='closest'
    )

    # Sales and Quantity Graph
    sales_quantity_fig = go.Figure()

    sales_quantity_fig.add_trace(go.Scatter(x=aggregated_data['date'], y=aggregated_data['sales'],
                                            name='Sales', mode='lines+markers',
                                            line=dict(width=2, color='blue')))

    sales_quantity_fig.add_trace(go.Scatter(x=aggregated_data['date'], y=aggregated_data['quantity'],
                                            name='Quantity', mode='lines+markers',
                                            line=dict(width=2, color='green'), yaxis='y2'))

    sales_quantity_fig.update_layout(
        title=f'Sales and Quantity Over Time {"Across All Regions" if selected_region == "All" else "in " + selected_region}',
        xaxis_title='Date',
        yaxis_title='Sales',
        yaxis2=dict(
            title='Quantity',
            overlaying='y',
            side='right'
        ),
        margin=dict(l=100, r=100, t=100, b=50),
        hovermode='closest'
    )

    return sales_price_fig, sales_quantity_fig

if __name__ == '__main__':
    app.run_server(debug=True)