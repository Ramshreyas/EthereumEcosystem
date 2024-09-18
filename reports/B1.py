from dash import html, dcc
import plotly.express as px
from .reports import register_report

@register_report("B1")
def demo_mid_level_report(structure, data):
    # Aggregate metrics for children of "B1"
    total_metric_1 = sum(data[node]["Metric 1"] for node in ["C1", "C2"])
    total_metric_2 = sum(data[node]["Metric 2"] for node in ["C1", "C2"])

    # Create a simple pie chart to visualize the aggregated metrics
    fig = px.pie(
        names=["Metric 1", "Metric 2"],
        values=[total_metric_1, total_metric_2],
        title="Aggregated Metrics for Level B1"
    )
    
    fig.update_layout(paper_bgcolor='#222222', plot_bgcolor='#222222', font=dict(color='white'))

    return html.Div([
        html.H4("Mid-Level Report for B1"),
        dcc.Graph(figure=fig)
    ])
