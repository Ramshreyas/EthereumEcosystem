import plotly.graph_objects as go
import json

# Load the data from the JSON file
def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

# Function to prepare Plotly data and check for missing leaf nodes in data.json
def prepare_plotly_data(stack_dict, data, parent_name=''):
    labels = []
    parents = []
    ids = []

    for key, value in stack_dict.items():
        # If it's a leaf node (no children), check if it exists in data.json
        if isinstance(value, dict) and not value:
            if key not in data:
                raise ValueError(f"Missing data for leaf node '{key}' in data.json.")
        
        # Add the node to the treemap structure
        labels.append(key)
        parents.append(parent_name)
        ids.append(key)

        # Recursively prepare data for children
        if isinstance(value, dict):
            sub_labels, sub_parents, sub_ids = prepare_plotly_data(value, data, key)
            labels.extend(sub_labels)
            parents.extend(sub_parents)
            ids.extend(sub_ids)

    return labels, parents, ids


# Function to visualize stack using Plotly Treemap
def visualize_stack_plotly(structure, data):
    # Prepare labels, parents, and ids, and check if leaf nodes exist in data.json
    labels, parents, ids = prepare_plotly_data(structure, data)

    # Print the treemap structure
    print("Labels:", labels)
    print("Parents:", parents)
    print("IDs:", ids)
    
    # Create the treemap figure
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        ids=ids,
        textinfo="label",
        textfont=dict(size=18, color="white"),  # White text color
    ))
    
    fig.update_layout(
        paper_bgcolor='black',  # Set background to black
        plot_bgcolor='black',   # Set plot background to black
        margin=dict(t=20, l=10, r=10, b=10),  # Reduced margins for more space
        height=800,  # Height adjustment for large display
        autosize=True,
        treemapcolorway=["#00aaff", "#ffaa00", "#aa00ff", "#ff00aa"],  # Optional: Color customization
        modebar_add=["fullscreen"],  # Ensures fullscreen mode is available
    )
    
    return fig
