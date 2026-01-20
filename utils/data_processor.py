import pandas as pd


def clean_data(raw_lines):
    valid_records = []
    total_parsed = 0
    invalid_count = 0

    # Skip the header row if it exists
    start_index = 1 if raw_lines and 'TransactionID' in raw_lines[0] else 0

    for line in raw_lines[start_index:]:
        line = line.strip()
        if not line: continue

        total_parsed += 1
        parts = line.split('|')

        # Basic structural check (Must have 8 columns)
        if len(parts) < 8:
            invalid_count += 1
            continue

        # Unpack the row
        t_id, date, p_id, p_name, qty_str, price_str, c_id, region = parts[:8]
        is_valid = True

        # --- VALIDATION RULES ---
        # 1. Transaction ID must start with 'T'
        if not t_id.startswith('T'): is_valid = False

        # 2. CustomerID and Region cannot be empty
        if not c_id.strip() or not region.strip(): is_valid = False

        # 3. Handle Numbers (Quantity & Price)
        try:
            # Remove commas (e.g., "1,500" -> 1500)
            clean_qty = int(qty_str.replace(',', '').strip())
            clean_price = float(price_str.replace(',', '').strip())

            # Rule: Must be positive numbers
            if clean_qty <= 0 or clean_price <= 0:
                is_valid = False
        except ValueError:
            is_valid = False  # Failed to convert to number

        if is_valid:
            # Clean Product Name (Remove commas)
            clean_p_name = p_name.replace(',', '')

            valid_records.append({
                'TransactionID': t_id,
                'Date': date,
                'ProductID': p_id,
                'ProductName': clean_p_name,
                'Quantity': clean_qty,
                'UnitPrice': clean_price,
                'CustomerID': c_id,
                'Region': region,
                'TotalSales': clean_qty * clean_price
            })
        else:
            invalid_count += 1

    # --- REQUIRED OUTPUT ---
    print(f"\nTotal records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return pd.DataFrame(valid_records)


def analyze_data(df):
    """Prints basic sales insights."""
    if df.empty: return

    print("\n--- Sales Analysis ---")
    print(f"Total Revenue: ${df['TotalSales'].sum():,.2f}")

    # Best selling product by Quantity
    best_product = df.groupby('ProductName')['Quantity'].sum().idxmax()
    print(f"Best Selling Product: {best_product}")

    # Revenue by Region
    print("\nRevenue by Region:")
    print(df.groupby('Region')['TotalSales'].sum())