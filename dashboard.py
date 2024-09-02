import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

# Dummy Stack Data
ethereum_stack = {
    'Protocol Layer': {
        'Ethereum Mainnet': {
            'Consensus Layer': {
                'Proof of Stake': {}
            },
            'Execution Layer': {
                'EVM': {
                    'Smart Contracts': {
                        'ERC-20': {},
                        'ERC-721': {}
                    }
                }
            }
        }
    },
    'Application Layer': {
        'DeFi': {
            'Uniswap': {},
            'Aave': {}
        }
    },
    'Infrastructure Layer': {
        'Nodes': {
            'Geth': {},
            'Parity': {}
        },
        'Oracles': {
            'Chainlink': {}
        }
    }
}

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

    st.plotly_chart(fig,use_container_width=True,height=800)
    
    return fig

# Function to display information about the node
def display_node_info(node_name):
    st.sidebar.subheader("Node Information")
    st.sidebar.write(f"Selected Node: **{node_name}**")

# JavaScript code to handle hover events
def generate_hover_script(fig_json):
    return f"""
        <div id="plotly-chart"></div>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            var graphDiv = document.getElementById('plotly-chart');
            var data = {fig_json};

            Plotly.newPlot(graphDiv, data.data, data.layout, {{displayModeBar: true}});

            graphDiv.on('plotly_hover', function(eventdata) {{
                var hoveredNode = eventdata.points[0].label;
                if (hoveredNode) {{
                    Streamlit.setComponentValue(hoveredNode);
                }}
            }});
        </script>
    """

# Main Streamlit Application
def main():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        .title-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 10px;
            border-bottom: 1px solid #ddd;
            width: 100%;
        }
        .title-bar h1 {
            font-size: 1.5rem;
            margin: 0;
        }
        .stApp {
            margin: 0;
            padding: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="title-bar">
            <h1>Ethereum Ecosystem</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Side Panel
    selected_layer = st.sidebar.selectbox(
        "Select Layer",
        ["All Layers", "Protocol Layer", "Application Layer", "Infrastructure Layer"]
    )

    # Main Panel (with visualization)
    col1, col2 = st.columns([2, 1])  # Treemap takes 2/3 width, summary takes 1/3

    # Column 1: Treemap Visualization
    with col1:
        fig = None
        if selected_layer == "All Layers":
            fig = visualize_stack_plotly(ethereum_stack)
        elif selected_layer == "Protocol Layer":
            fig = visualize_stack_plotly({'Protocol Layer': ethereum_stack['Protocol Layer']})
        elif selected_layer == "Application Layer":
            fig = visualize_stack_plotly({'Application Layer': ethereum_stack['Application Layer']})
        elif selected_layer == "Infrastructure Layer":
            fig = visualize_stack_plotly({'Infrastructure Layer': ethereum_stack['Infrastructure Layer']})

        if fig:
            fig_json = fig.to_json()
            hover_script = generate_hover_script(fig_json)
            selected_node = components.html(hover_script, height=800)

    # Column 2: Data Summary Panel
    with col2:
        st.subheader("Data Summary")
        st.write("This is a placeholder for the data summary.")
        st.write("Hover over nodes in the treemap to see more details.")

        # Display dummy data for now
        st.write("Summary of the selected node would appear here.")
        st.write("E.g., Node: Ethereum Mainnet")
        st.write("Details: Example details about the node would be displayed here.")

if __name__ == "__main__":
    main()
