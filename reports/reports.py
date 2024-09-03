from dash import html

# A dictionary to hold the custom report functions
custom_reports = {}

# Decorator to register a custom report for a specific node
def register_report(node_name):
    def decorator(func):
        custom_reports[node_name] = func
        return func
    return decorator

# Function to get a custom report if it exists
def get_custom_report(node_name, structure, data):
    report_func = custom_reports.get(node_name)
    if report_func:
        return report_func(structure, data)
    return None

# Example custom report for the "Protocol Layer" node
@register_report("Protocol Layer")
def protocol_layer_report(structure, data):
    # More detailed visualization for the Protocol Layer
    return html.Div([
        html.H4("Protocol Layer Report"),
        html.P("Network Size: 10,000 nodes"),
        html.P("Transaction Volume: 500,000 transactions"),
        # Example of adding more detailed insights and components
        html.P("This report could include charts, graphs, and other insights relevant to the Protocol Layer.")
    ])

# Example custom report for the "DeFi" node
@register_report("DeFi")
def defi_report(structure, data):
    # More detailed visualization for the DeFi node
    return html.Div([
        html.H4("DeFi Report"),
        html.P("Liquidity Pools: 200"),
        html.P("Total Trading Volume: $100,000,000"),
        # Example of adding more detailed insights and components
        html.P("This report could include market analysis, risk assessments, and trending DeFi projects.")
    ])

# Example custom report for the "Uniswap" node
@register_report("Uniswap")
def uniswap_report(structure, data):
    # More detailed visualization for Uniswap
    return html.Div([
        html.H4("Uniswap Report"),
        html.P("Active Liquidity Pools: 150"),
        html.P("Total Volume Locked: $50,000,000"),
        # Example of adding more detailed insights and components
        html.P("This report could include liquidity trends, fee distribution, and user adoption metrics.")
    ])
