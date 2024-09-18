from dash import html, dcc
import plotly.express as px
from .reports import register_report

@register_report("A")
def demo_top_level_report(structure, data):
    # Aggregate metrics for all children of "A"
    total_metric_1 = sum(data[node]["Metric 1"] for node in ["C1", "C2", "C3", "C4"])
    total_metric_2 = sum(data[node]["Metric 2"] for node in ["C1", "C2", "C3", "C4"])

    # Create a simple bar chart to visualize the aggregated metrics
    fig = px.bar(
        x=["Metric 1", "Metric 2"],
        y=[total_metric_1, total_metric_2],
        labels={'x': 'Metrics', 'y': 'Total Value'},
        title="Aggregated Metrics for Level A",
        text=[total_metric_1, total_metric_2]
    )
    
    fig.update_layout(paper_bgcolor='#222222', plot_bgcolor='#222222', font=dict(color='white'))

    return html.Div([
        html.H4("Top-Level Report for A"),
        dcc.Graph(figure=fig)
    ])
