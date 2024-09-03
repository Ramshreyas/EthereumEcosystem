from dash import html, dcc
import plotly.express as px
from .reports import register_report

@register_report("Protocol Layer")
def protocol_layer_report(structure, data):
    # Dummy data for visualization
    consensus_data = {
        'Consensus Mechanism': ['Proof of Stake', 'Proof of Work', 'Delegated PoS'],
        'Percentage': [70, 20, 10]
    }

    evm_data = {
        'Metric': ['Gas Used', 'Transactions', 'Smart Contracts'],
        'Value': [80000000, 2000000, 300000]
    }

    # Pie chart for Consensus Mechanism distribution
    fig_pie = px.pie(consensus_data, names='Consensus Mechanism', values='Percentage',
                     title='Consensus Mechanism Distribution',
                     color_discrete_sequence=px.colors.sequential.RdBu)

    # Bar chart for EVM metrics
    fig_bar = px.bar(evm_data, x='Metric', y='Value',
                     title='EVM Metrics Overview',
                     color='Metric',
                     color_discrete_sequence=px.colors.sequential.Plasma)

    # Apply dark theme and compact style to both charts
    fig_pie.update_layout(
        paper_bgcolor='#222222',
        plot_bgcolor='#222222',
        font=dict(color='white', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    fig_bar.update_layout(
        paper_bgcolor='#222222',
        plot_bgcolor='#222222',
        font=dict(color='white', size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=300
    )

    # Layout for the Protocol Layer report in dark mode
    return html.Div([
        html.H4("Protocol Layer Report", style={"color": "white", "textAlign": "center", "marginBottom": "20px"}),

        # Adding the pie chart
        dcc.Graph(figure=fig_pie, style={"marginBottom": "20px"}),

        # Adding the bar chart
        dcc.Graph(figure=fig_bar),

        # Additional insights or components
        html.P(
            "This report provides an overview of the Ethereum Protocol Layer, "
            "including the distribution of consensus mechanisms and key EVM metrics. "
            "These visualizations help in understanding the network's current state and performance.",
            style={"color": "white", "fontSize": "12px", "textAlign": "center"}
        )
    ], style={"backgroundColor": "#222222", "padding": "10px", "borderRadius": "10px", "height": "100%", "boxSizing": "border-box"})
