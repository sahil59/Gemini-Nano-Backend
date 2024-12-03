def extract_data_recursive(data, level=0):
    extracted_data = ""
    indent = "  " * level  # Indentation for readability

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "userEnteredValue":  # Specific key for cell data
                extracted_data += indent + f"{value.get('stringValue', '')}\t"
            else:
                extracted_data += extract_data_recursive(value, level + 1)
        if "values" in data:  # Add a newline after processing a row of values
            extracted_data += "\n"
    elif isinstance(data, list):
        for item in data:
            extracted_data += extract_data_recursive(item, level)

    return extracted_data

# Wrapper function to process entire JSON
def process_sheets(data):
    spreadsheet_id = data.get("spreadsheetId")
    sheets = data.get("sheets", [])
    extracted_data = f"Spreadsheet ID: {spreadsheet_id}\n\n"

    for sheet in sheets:
        sheet_props = sheet.get("properties", {})
        title = sheet_props.get("title", "Untitled")
        sheet_id = sheet_props.get("sheetId", "Unknown")

        extracted_data += f"Sheet Title: {title}\n  Sheet ID: {sheet_id}\n\n"

        # Recursively extract data
        sheet_data = sheet.get("data", [])
        extracted_data += extract_data_recursive(sheet_data)
        extracted_data += "\n"

    return extracted_data.strip()