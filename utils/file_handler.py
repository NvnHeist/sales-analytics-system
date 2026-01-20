import os


def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return []

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                # Skip the header row and remove empty lines
                next(f)
                raw_lines = [line.strip() for line in f if line.strip()]
            break  # Success, exit encoding loop
        except (UnicodeDecodeError, Exception):
            continue

    return raw_lines