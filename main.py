import os
from utils.file_handler import read_file, save_to_csv
from utils.data_processor import clean_data, analyze_data
from utils.api_handler import fetch_exchange_rates


def main():
    # Setup paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_path, 'data', 'sales_data.txt')
    output_file = os.path.join(base_path, 'output', 'cleaned_sales_report.csv')

    print("--- Starting Sales Analytics System ---")

    # 1. Read
    raw_data = read_file(input_file)
    if not raw_data: return

    # 2. Clean
    df = clean_data(raw_data)

    if not df.empty:
        # 3. Analyze
        analyze_data(df)

        # 4. API Check
        rate = fetch_exchange_rates()
        if rate:
            total_eur = df['TotalSales'].sum() * rate
            print(f"Total Revenue in EUR: €{total_eur:,.2f}")

        # 5. Save
        save_to_csv(df, output_file)
    else:
        print("No valid data found.")


if __name__ == "__main__":
    main()