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

# Define the app layout with a consistent dark theme
app.layout = html.Div(children=[
    html.H1(
        children='Sales, Price, and Quantity Data Over Time',
        style={'textAlign': 'center', 'color': '#FFFFFF', 'marginBottom': '30px'}
    ),
    
    html.Div([
        dcc.RadioItems(
            id='region-radio',
            options=[{'label': 'All', 'value': 'All'},
                     {'label': 'North', 'value': 'North'},
                     {'label': 'East', 'value': 'East'},
                     {'label': 'South', 'value': 'South'},
                     {'label': 'West', 'value': 'West'}],
            value='All',
            labelStyle={'display': 'inline-block', 'color': '#FFFFFF', 'marginRight': '20px'},
            style={'textAlign': 'center', 'color': '#FFFFFF', 'marginBottom': '20px'}
        ),
    ]),

    dcc.Graph(id='sales-price-graph', style={'backgroundColor': '#333'}),
    dcc.Graph(id='sales-quantity-graph', style={'backgroundColor': '#333'}),
], style={'backgroundColor': '#333', 'color': '#FFFFFF', 'height': '100vh'})

# Callback to update graphs
@app.callback(
    [Output('sales-price-graph', 'figure'),
     Output('sales-quantity-graph', 'figure')],
    [Input('region-radio', 'value')]
)
def update_graph(selected_region):
    try:
        print(f"Selected region: {selected_region}")
        # Filter data based on selected region
        if selected_region == 'All':
            filtered_data = sales_data
        else:
            filtered_data = sales_data[sales_data['region'].str.lower() == selected_region.lower()]
            print(f"Filtered data: {filtered_data.head()}")  # Debug print

        # Check if there is any data to plot after filtering
        if filtered_data.empty:
            raise ValueError(f"No data found for region: {selected_region}")

        # Aggregating sales, price, and quantity by date
        aggregated_data = filtered_data.groupby('date').agg({'sales': 'sum', 'price': 'mean', 'quantity': 'sum'}).reset_index()

        # Sales and Price Graph
        sales_price_fig = create_sales_price_figure(aggregated_data)

        # Sales and Quantity Graph
        sales_quantity_fig = create_sales_quantity_figure(aggregated_data)

            # Apply the dark theme
        for fig in (sales_price_fig, sales_quantity_fig):
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                xaxis=dict(color='#FFFFFF', linecolor='#FFFFFF'),
                yaxis=dict(color='#FFFFFF', linecolor='#FFFFFF'),
                legend=dict(font=dict(color='#CCCCCC')),
        )

        return sales_price_fig, sales_quantity_fig
    
    except Exception as e:
        print(f"Error updating graphs: {e}")
        # Return empty figures in case of error
        return go.Figure(), go.Figure()
    

# Function to create sales and price figure
def create_sales_price_figure(aggregated_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=aggregated_data['date'], y=aggregated_data['sales'],
                             name='Sales', mode='lines+markers',
                             line=dict(width=2, color='blue'),
                             marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=aggregated_data['date'], y=aggregated_data['price'],
                             name='Price', mode='lines+markers',
                             line=dict(width=2, color='red'), yaxis='y2',
                             marker=dict(size=6)))
    # Add rectangle to highlight specific date
    fig.add_vrect(x0="2021-01-14", x1="2021-01-16", fillcolor="LightSalmon", opacity=0.5,
                  layer="below", line_width=0, annotation_text="Price effect on 15 Jan 2021",
                  annotation_position="top right")
    # Update layout
    fig.update_layout(title='Sales and Price Over Time Across All Regions', xaxis_title='Date',
                      yaxis_title='Sales', yaxis2=dict(title='Price', overlaying='y', side='right'),
                      margin=dict(l=100, r=100, t=100, b=50), hovermode='closest')
    return fig


# Function to create sales and quantity figure
# Function to create sales and quantity figure
def create_sales_quantity_figure(aggregated_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=aggregated_data['date'],
        y=aggregated_data['quantity'],
        name='Quantity',
        mode='lines+markers',
        line=dict(width=2, color='green'),
        marker=dict(size=6)))

    fig.add_trace(go.Scatter(
        x=aggregated_data['date'],
        y=aggregated_data['price'],
        name='Price',
        mode='lines+markers',
        line=dict(width=2, color='red'),
        yaxis='y2',
        marker=dict(size=6)))

    # Add rectangle to highlight specific date
    fig.add_vrect(
        x0="2021-01-14",
        x1="2021-01-16",
        fillcolor="LightGreen",
        opacity=0.5,
        layer="below",
        line_width=0,
        annotation_text="Quantity vs. Price on 15 Jan 2021",
        annotation_position="top right")

    # Update the layout to use a dark theme
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        title={
            'text': "Quanity and Price Over Time",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Date",
        yaxis_title="Quantity",
        legend_title="Legend Title",
        hovermode="closest",
    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

