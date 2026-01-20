import os


def read_file(file_path):
    """Reads the raw file, handling encoding issues."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []

    try:
        # 'latin-1' is used to handle the non-UTF-8 requirement
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def save_to_csv(df, output_path):
    """Saves the final clean data to CSV."""
    try:
        df.to_csv(output_path, index=False)
        print(f"Success! Processed data saved to: {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")