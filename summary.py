import json

# Aggregation function to extract data for a node and its children
def aggregate_node_data(node_name, structure, data):
    def recurse(node, node_structure, node_data, indent=0):
        details = " " * indent + f"- {node}\n"
        metrics = node_data.get("metrics", {})
        
        # Add metrics
        for metric, value in metrics.items():
            details += " " * (indent + 4) + f"{metric}: {value}\n"

        # Recursively add details for children
        for child, child_structure in node_structure.get(node, {}).items():
            child_data = node_data.get(child, {})
            details += recurse(child, child_structure, child_data, indent + 4)
        return details

    # Flatten structure and find relevant data
    flattened_subgraph = flatten_structure({node_name: structure.get(node_name, {})})
    aggregated_details = ""
    
    for path in flattened_subgraph:
        path_parts = path.split('/')
        current_node = path_parts[-1]
        node_structure = structure
        node_data = data

        # Traverse the path
        for part in path_parts:
            node_structure = node_structure.get(part, {})
            node_data = node_data.get(part, {})
        
        # Aggregate data for this node
        aggregated_details += recurse(current_node, node_structure, node_data)

    return aggregated_details

# Function to generate the summary details
def generate_summary(clickData, structure, data):
    if clickData and 'label' in clickData['points'][0]:
        node_name = clickData['points'][0]['label']
        details = aggregate_node_data(node_name, structure, data)
        return node_name, details
    return "Data Summary", "Click on a node to see details here."

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
    flat_structure = flatten_structure(structure)

    for path in flat_structure:
        path_parts = path.split('/')
        node_data = data
        valid = True

        # Traverse the path in the data dictionary
        for part in path_parts:
            if part in node_data:
                node_data = node_data[part]
            else:
                print(f"Warning: No data found for node '{path}'")
                valid = False
                break

        # Additional check to ensure that it's a valid leaf node or has metrics
        if valid and 'metrics' not in node_data:
            print(f"Warning: No metrics found for node '{path}'")

# Example usage of this validation within your app.py, before running the app:
# validate_structure_and_data(structure, data)
