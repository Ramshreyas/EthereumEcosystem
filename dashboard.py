from dash import Dash, dcc, html, Input, Output, State
from treemap import visualize_stack_plotly
from summary import generate_summary, display_aggregated_data, validate_structure_and_data
from reports.reports import get_custom_report
import json
import os

# Load ecosystem mappings from ecosystems.json
def load_ecosystems():
    with open("data/ecosystems.json", "r") as f:
        return json.load(f)

# Function to dynamically load the selected structure file
def load_structure(structure_file):
    with open(f"data/{structure_file}", "r") as f:
        return json.load(f)

# Load available ecosystems
ecosystems = load_ecosystems()

# Load the default data.json file
def load_data():
    with open("data/data.json", "r") as f:
        return json.load(f)

# Initialize Dash app
app = Dash(__name__)

# Dash layout with dark mode styling and a dropdown
app.layout = html.Div(
    style={"backgroundColor": "#111111", "color": "white", "height": "100vh", "width": "100vw"},
    children=[
        # Title and dropdown container
        html.Div(
            style={"padding": "20px", "borderBottom": "1px solid #444", "display": "flex", "flexDirection": "column", "alignItems": "flex-start"},
            children=[
                # Title fixed as "Ethereum Ecosystem"
                html.H1("Ethereum Ecosystem", id='dashboard-title', style={"margin": "0", "fontSize": "2rem", "fontWeight": "normal"}),
                
                # Dropdown positioned underneath the title
                dcc.Dropdown(
                    id='ecosystem-dropdown',
                    options=[{"label": label, "value": filename} for label, filename in ecosystems.items()],
                    value='financial_structure.json',  # Default selection
                    clearable=False,
                    style={"backgroundColor": "#2222", "color": "black", "width": "300px", "padding-top": "10px"},
                    className="dropdown-class"
                )
            ]
        ),
        
        # Two columns: Treemap on the left, summary on the right (50% each)
        html.Div(
            style={"display": "flex", "flexDirection": "row", "padding": "20px"},
            children=[
                # Treemap Column (50% width)
                html.Div(
                    style={"width": "50%", "paddingRight": "20px"},
                    children=[
                        dcc.Graph(id='treemap-chart', style={"height": "800px"})
                    ]
                ),
                
                # Summary Column (50% width)
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

# Callback to update the dashboard title and load the selected ecosystem structure
@app.callback(
    [Output('dashboard-title', 'children'), Output('treemap-chart', 'figure')],
    [Input('ecosystem-dropdown', 'value')]
)
def update_dashboard(selected_structure):
    # Load the selected structure file
    structure = load_structure(selected_structure)
    
    # Load the data for aggregation or reporting
    data = load_data()

    # Generate the treemap for the selected structure
    treemap_fig = visualize_stack_plotly(structure, data)
    
    # Update the dashboard title
    title = [key for key, value in ecosystems.items() if value == selected_structure][0]
    
    # Return title and figure separately (not as an array)
    return title, treemap_fig


# Dash callback to update the data summary based on the clicked node
@app.callback(
    [Output('summary-title', 'children'), Output('node-info', 'children')],
    [Input('treemap-chart', 'clickData'), State('ecosystem-dropdown', 'value')]
)
def display_node_info(clickData, selected_structure):
    if clickData and 'label' in clickData['points'][0]:
        node_name = clickData['points'][0]['label']
        
        # Load the selected structure
        structure = load_structure(selected_structure)
        
        # Check for a custom report first
        custom_report = get_custom_report(node_name, structure, load_data())
        if custom_report:
            return node_name, custom_report
        
        # If no custom report, fall back to the aggregation
        aggregated_data = generate_summary(node_name, structure, load_data())
        table = display_aggregated_data(aggregated_data)
        return node_name, table
    
    return "Data Summary", "Click on a node to see details here."

# Custom CSS to adjust the dropdown text color when closed
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
