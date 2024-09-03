from dash import Dash, dcc, html, Input, Output
from treemap import visualize_stack_plotly
from summary import generate_summary, display_aggregated_data, validate_structure_and_data
from reports.reports import get_custom_report
import json

# Load structure and data from JSON files in the data folder
def load_structure():
    with open("data/structure.json", "r") as f:
        return json.load(f)

def load_data():
    with open("data/data.json", "r") as f:
        return json.load(f)

# Load structure and data
structure = load_structure()
data = load_data()

# Validate structure and data
validate_structure_and_data(structure, data)

# Initialize Dash app
app = Dash(__name__)

# Dash layout with dark mode styling
app.layout = html.Div(
    style={"backgroundColor": "#111111", "color": "white", "height": "100vh", "width": "100vw"},
    children=[
        # Title
        html.Div(
            style={"textAlign": "left", "padding": "20px", "borderBottom": "1px solid #444"},
            children=[
                html.H1("Ethereum Ecosystem", style={"margin": "0", "fontSize": "2rem", "fontWeight": "normal"})
            ]
        ),
        
        # Two columns: Treemap on the left, summary on the right
        html.Div(
            style={"display": "flex", "flexDirection": "row", "padding": "20px"},
            children=[
                # Treemap Column
                html.Div(
                    style={"width": "50%", "paddingRight": "20px"},
                    children=[
                        dcc.Graph(id='treemap-chart', style={"height": "800px"})
                    ]
                ),
                
                # Summary Column
                html.Div(
                    style={"width": "50%", "paddingLeft": "20px", "backgroundColor": "#222", "borderRadius": "10px"},
                    children=[
                        html.H3(id="summary-title", style={"textAlign": "center", "fontSize": "1.5rem", "fontWeight": "normal"}, children="Data Summary"),
                        html.Div(
                            id='node-info',
                            style={"padding": "10px", "backgroundColor": "#333", "borderRadius": "10px"},
                            children="Click on a node to see details here."
                        )
                    ]
                )
            ]
        )
    ]
)

# Dash callback to update the treemap based on the selected layer (unchanged)
@app.callback(
    Output('treemap-chart', 'figure'),
    [Input('treemap-chart', 'id')]
)
def update_treemap(_):
    return visualize_stack_plotly(structure)

# Dash callback to update the data summary based on the clicked node
@app.callback(
    [Output('summary-title', 'children'), Output('node-info', 'children')],
    [Input('treemap-chart', 'clickData')]
)
def display_node_info(clickData):
    if clickData and 'label' in clickData['points'][0]:
        node_name = clickData['points'][0]['label']
        
        # Check for a custom report first
        custom_report = get_custom_report(node_name, structure, data)
        if custom_report:
            return node_name, custom_report
        
        # If no custom report, fall back to the aggregation
        aggregated_data = generate_summary(node_name, structure, data)
        table = display_aggregated_data(aggregated_data)
        return node_name, table
    
    return "Data Summary", "Click on a node to see details here."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
