import os
from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter


def main():
    # Setup paths relative to your MacBook Desktop
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_path, 'data', 'sales_data.txt')

    print("--- 🚀 Sales Analytics System ---")

    # 1. READ (Task 1.1)
    raw_lines = read_sales_data(input_file)
    if not raw_lines:
        return

    # 2. PARSE (Task 1.2)
    transactions = parse_transactions(raw_lines)

    # 3. ANALYZE FOR USER (Filter Display Requirements)
    # Get available regions for the user to choose from
    regions = sorted(list(set(t['Region'] for t in transactions)))
    print(f"\nAvailable Regions: {', '.join(regions)}")

    # Calculate min/max transaction amounts for the user
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    print(f"Transaction Amount Range: ${min(amounts):,.2f} - ${max(amounts):,.2f}")

    # 4. VALIDATE & FILTER (Task 1.3)
    # Example: You can prompt the user for input, or set defaults
    selected_region = input("\nEnter region to filter by (or press Enter for all): ").strip() or None

    # Passing None to the filter function if the user didn't type anything
    valid_data, invalid_count, summary = validate_and_filter(
        transactions,
        region=selected_region
    )

    # 5. FINAL REPORT
    print("\n--- Process Summary ---")
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    main()
