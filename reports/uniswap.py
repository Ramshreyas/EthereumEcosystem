from dash import html, dcc
import plotly.express as px
from .reports import register_report

@register_report("Uniswap")
def uniswap_report(structure, data):
    # Dummy data for visualization
    liquidity_data = {
        'Pool': ['ETH/USD', 'BTC/USD', 'DAI/USDC'],
        'Liquidity': [50000000, 30000000, 20000000]
    }

    volume_data = {
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'Volume': [1000000, 1500000, 2000000, 2500000, 3000000]
    }

    # Bar chart for Liquidity in different pools
    fig_liquidity = px.bar(liquidity_data, x='Pool', y='Liquidity',
                           title='Liquidity by Pool',
                           color='Pool',
                           color_discrete_sequence=px.colors.sequential.Viridis)

    # Line chart for trading volume over the week
    fig_volume = px.line(volume_data, x='Day', y='Volume',
                         title='Trading Volume Over the Week',
                         markers=True,
                         color_discrete_sequence=px.colors.sequential.Viridis)

    # Apply dark theme and compact style to both charts
    fig_liquidity.update_layout(
        paper_bgcolor='#222222',
        plot_bgcolor='#222222',
        font=dict(color='white', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    fig_volume.update_layout(
        paper_bgcolor='#222222',
        plot_bgcolor='#222222',
        font=dict(color='white', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    # Layout for the Uniswap report in dark mode
    return html.Div([
        html.H4("Uniswap Report", style={"color": "white", "textAlign": "center", "marginBottom": "20px"}),

        # Adding the liquidity bar chart
        dcc.Graph(figure=fig_liquidity, style={"marginBottom": "20px"}),

        # Adding the trading volume line chart
        dcc.Graph(figure=fig_volume),

        # Additional insights or components
        html.P(
            "This report provides insights into Uniswap's liquidity distribution across different pools and "
            "the trading volume over the past week. These visualizations help in understanding market activity and liquidity trends.",
            style={"color": "white", "fontSize": "12px", "textAlign": "center"}
        )
    ], style={"backgroundColor": "#222222", "padding": "10px", "borderRadius": "10px", "height": "100%", "boxSizing": "border-box"})
