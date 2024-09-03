from dash import html, dcc
import plotly.express as px
from .reports import register_report

@register_report("DeFi")
def defi_report(structure, data):
    # Dummy data for visualization
    defi_data = {
        'Protocol': ['Uniswap', 'Aave', 'Compound', 'MakerDAO'],
        'Total Value Locked': [50000000, 40000000, 30000000, 20000000]
    }

    risk_data = {
        'Risk Factor': ['Smart Contract', 'Market Volatility', 'Liquidity', 'Governance'],
        'Impact Score': [8, 7, 5, 6]
    }

    # Bar chart for Total Value Locked in DeFi protocols
    fig_tvl = px.bar(defi_data, x='Protocol', y='Total Value Locked',
                     title='Total Value Locked in DeFi Protocols',
                     color='Protocol',
                     color_discrete_sequence=px.colors.sequential.Inferno)

    # Bar chart for Risk Factors in DeFi
    fig_risk = px.bar(risk_data, x='Risk Factor', y='Impact Score',
                      title='DeFi Risk Factors and Impact',
                      color='Risk Factor',
                      color_discrete_sequence=px.colors.sequential.Inferno)

    # Apply dark theme and compact style to both charts
    fig_tvl.update_layout(
        paper_bgcolor='#222222',
        plot_bgcolor='#222222',
        font=dict(color='white', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    fig_risk.update_layout(
        paper_bgcolor='#222222',
        plot_bgcolor='#222222',
        font=dict(color='white', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    # Layout for the DeFi report in dark mode
    return html.Div([
        html.H4("DeFi Report", style={"color": "white", "textAlign": "center", "marginBottom": "20px"}),

        # Adding the TVL bar chart
        dcc.Graph(figure=fig_tvl, style={"marginBottom": "20px"}),

        # Adding the risk factors bar chart
        dcc.Graph(figure=fig_risk),

        # Additional insights or components
        html.P(
            "This report provides a comprehensive overview of the Total Value Locked (TVL) in major DeFi protocols and "
            "the key risk factors impacting the DeFi space. These visualizations are crucial for assessing the stability and potential risks in DeFi.",
            style={"color": "white", "fontSize": "12px", "textAlign": "center"}
        )
    ], style={"backgroundColor": "#222222", "padding": "10px", "borderRadius": "10px", "height": "100%", "boxSizing": "border-box"})
