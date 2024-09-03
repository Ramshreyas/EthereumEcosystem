import importlib
import os
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

# Function to dynamically discover and import all report modules
def register_all_reports():
    reports_directory = os.path.dirname(__file__)
    for filename in os.listdir(reports_directory):
        if filename.endswith(".py") and filename not in ["reports.py", "__init__.py"]:
            module_name = f"reports.{filename[:-3]}"
            importlib.import_module(module_name)

# Call the function to register all reports
register_all_reports()
