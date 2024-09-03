import json
from dash import dash_table

# Function to display aggregated data as a table
def display_aggregated_data(aggregated_data):
    if not aggregated_data:
        return "No data to display"

    # Extract the column headers from the aggregated data
    columns = [{"name": col, "id": col} for col in aggregated_data[0].keys()]

    # Return the table component
    return dash_table.DataTable(
        data=aggregated_data,
        columns=columns,
        style_cell={'textAlign': 'left', 'backgroundColor': '#333', 'color': 'white'},
        style_header={'backgroundColor': '#444', 'fontWeight': 'bold'},
        style_table={'overflowX': 'auto'},
        fill_width=True
    )

# Function to get all leaf nodes from a subgraph
def get_leaf_nodes(subgraph):
    leaf_nodes = []
    for key, value in subgraph.items():
        if isinstance(value, dict) and value:
            leaf_nodes.extend(get_leaf_nodes(value))
        else:
            leaf_nodes.append(key)
    return leaf_nodes

# Aggregation function to recursively aggregate metrics at each level of the subgraph
def aggregate_node_data(node_name, structure, data):
    def recurse_aggregate(node, node_structure):
        # Get the subgraph for the current node
        subgraph = node_structure.get(node, {})
        
        # Get all leaf nodes for the current node
        leaf_nodes = get_leaf_nodes({node: subgraph})
        
        # Aggregate metrics for the current node
        total_metrics = {}
        
        for leaf in leaf_nodes:
            if leaf in data:
                metrics = data[leaf]
                for metric, value in metrics.items():
                    if metric in total_metrics:
                        total_metrics[metric] += value
                    else:
                        total_metrics[metric] = value
        
        # Prepare the result entry for the current node
        result = {
            "Node": node,
            **total_metrics
        }
        
        # Collect the results for the current node and its children
        results = [result]
        for child in subgraph:
            results.extend(recurse_aggregate(child, subgraph))
        
        return results

    # Start the recursive aggregation from the selected node
    return recurse_aggregate(node_name, structure)

# Function to generate the summary details
def generate_summary(node_name, structure, data):
    return aggregate_node_data(node_name, structure, data)

# Function to flatten the structure into a list of paths
def flatten_structure(structure, parent_key=''):
    paths = []
    for key, value in structure.items():
        new_key = f"{parent_key}/{key}" if parent_key else key
        paths.append(new_key)
        if isinstance(value, dict):
            paths.extend(flatten_structure(value, new_key))
    return paths

# Validation function to ensure that each element in the structure has corresponding data
def validate_structure_and_data(structure, data):
    def validate_node(node_name, node_structure):
        leaf_nodes = get_leaf_nodes({node_name: node_structure})
        for leaf in leaf_nodes:
            if leaf not in data:
                print(f"Warning: No data found for leaf node '{leaf}'")
    
    for root_node, node_structure in structure.items():
        validate_node(root_node, node_structure)
