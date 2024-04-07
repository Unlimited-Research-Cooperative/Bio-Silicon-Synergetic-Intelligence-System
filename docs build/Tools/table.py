import json
from mkdocs_macros import macro

@macro
def json_to_table(filepath: str = "./params.json"):
    # Load the JSON data
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Assuming data is a list of dictionaries
    headers = data[0].keys()
    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for row in data:
        markdown_table += "| " + " | ".join(str(row[h]) for h in headers) + " |\n"

    return markdown_table
