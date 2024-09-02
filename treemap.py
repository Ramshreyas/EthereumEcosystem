import plotly.graph_objects as go
import json

# Load the data from the JSON file
def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

# Function to convert nested dictionary to a list format for Plotly
def prepare_plotly_data(stack_dict, parent_name=''):
    labels = []
    parents = []
    ids = []
    for key, value in stack_dict.items():
        labels.append(key)
        parents.append(parent_name)
        ids.append(key)
        if isinstance(value, dict):
            sub_labels, sub_parents, sub_ids = prepare_plotly_data(value, key)
            labels.extend(sub_labels)
            parents.extend(sub_parents)
            ids.extend(sub_ids)
    return labels, parents, ids

# Function to visualize stack using Plotly Treemap
def visualize_stack_plotly(stack_dict):
    labels, parents, ids = prepare_plotly_data(stack_dict)
    
    fig = go.Figure(go.Treemap(
        labels = labels,
        parents = parents,
        ids = ids,
        textinfo = "label+value+percent parent+percent entry",
        textfont=dict(size=18, color="white"),  # White text color
    ))
    
    fig.update_layout(
        paper_bgcolor='black',  # Set background to black
        plot_bgcolor='black',   # Set plot background to black
        margin = dict(t=20, l=10, r=10, b=10),  # Reduced margins for more space
        height=800,  # Height adjustment for large display
        autosize=True,
        treemapcolorway=["#00aaff", "#ffaa00", "#aa00ff", "#ff00aa"],  # Optional: Color customization
        modebar_add=["fullscreen"],  # Ensures fullscreen mode is available
    )

    return fig
