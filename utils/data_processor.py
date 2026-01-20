def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """
    transactions = []
    for line in raw_lines:
        parts = line.split('|')

        # Skip rows with incorrect number of fields (8 required)
        if len(parts) < 8:
            continue

        t_id, date, p_id, p_name, qty, price, c_id, region = parts[:8]

        # Clean commas and convert types
        clean_p_name = p_name.replace(',', '')
        try:
            clean_qty = int(qty.replace(',', ''))
            clean_price = float(price.replace(',', ''))
        except ValueError:
            continue

        transactions.append({
            'TransactionID': t_id,
            'Date': date,
            'ProductID': p_id,
            'ProductName': clean_p_name,
            'Quantity': clean_qty,
            'UnitPrice': clean_price,
            'CustomerID': c_id,
            'Region': region
        })
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    """
    valid_list = []
    invalid_count = 0
    stats = {'total_input': len(transactions), 'invalid': 0, 'filtered_by_region': 0, 'filtered_by_amount': 0}

    for t in transactions:
        # Validation Rules
        is_valid = (
                t['Quantity'] > 0 and
                t['UnitPrice'] > 0 and
                t['TransactionID'].startswith('T') and
                t['ProductID'].startswith('P') and
                t['CustomerID'].startswith('C')
        )

        if not is_valid:
            invalid_count += 1
            continue

        # Optional Filters
        total_val = t['Quantity'] * t['UnitPrice']
        if region and t['Region'] != region:
            stats['filtered_by_region'] += 1
            continue
        if (min_amount and total_val < min_amount) or (max_amount and total_val > max_amount):
            stats['filtered_by_amount'] += 1
            continue

        valid_list.append(t)

    stats['invalid'] = invalid_count
    stats['final_count'] = len(valid_list)

    # Required cleaning print output
    print(f"Total records parsed: {stats['total_input']}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_list)}")

    return valid_list, invalid_count, stats


def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions."""
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)


def region_wise_sales(transactions):
    """Analyzes sales by region, sorted by total sales descending."""
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        reg = t['Region']
        sales = t['Quantity'] * t['UnitPrice']
        if reg not in region_stats:
            region_stats[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        region_stats[reg]['total_sales'] += sales
        region_stats[reg]['transaction_count'] += 1

    for reg in region_stats:
        region_stats[reg]['percentage'] = round((region_stats[reg]['total_sales'] / total_revenue) * 100, 2)

    return dict(sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))


def daily_sales_trend(transactions):
    """Groups revenue and customer counts by date."""
    daily_data = {}
    for t in transactions:
        d = t['Date']
        if d not in daily_data:
            daily_data[d] = {'revenue': 0.0, 'transaction_count': 0, 'customers': set()}
        daily_data[d]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily_data[d]['transaction_count'] += 1
        daily_data[d]['customers'].add(t['CustomerID'])

    # Convert sets to unique counts and sort chronologically
    for d in daily_data:
        daily_data[d]['unique_customers'] = len(daily_data[d].pop('customers'))

    return dict(sorted(daily_data.items()))


def find_peak_sales_day(transactions):
    """Identifies the date with the highest revenue."""
    trend = daily_sales_trend(transactions)
    peak_date = max(trend, key=lambda x: trend[x]['revenue'])
    return peak_date, trend[peak_date]['revenue'], trend[peak_date]['transaction_count']
def get_product_metrics(transactions):
    """Helper to aggregate quantity and revenue by product name."""
    metrics = {}
    for t in transactions:
        name = t['ProductName']
        if name not in metrics:
            metrics[name] = {'qty': 0, 'rev': 0.0}
        metrics[name]['qty'] += t['Quantity']
        metrics[name]['rev'] += t['Quantity'] * t['UnitPrice']
    return metrics

def top_selling_products(transactions, n=5):
    """Returns top n products by quantity sold."""
    metrics = get_product_metrics(transactions)
    sorted_products = sorted(metrics.items(), key=lambda x: x[1]['qty'], reverse=True)
    return [(name, data['qty'], data['rev']) for name, data in sorted_products[:n]]

def low_performing_products(transactions, threshold=10):
    """Returns products with total quantity below threshold."""
    metrics = get_product_metrics(transactions)
    low_perf = [(n, d['qty'], d['rev']) for n, d in metrics.items() if d['qty'] < threshold]
    return sorted(low_perf, key=lambda x: x[1])


def customer_analysis(transactions):
    """Calculates spending habits per customer, sorted by total spent."""
    stats = {}
    for t in transactions:
        cid = t['CustomerID']
        amt = t['Quantity'] * t['UnitPrice']
        if cid not in stats:
            stats[cid] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        stats[cid]['total_spent'] += amt
        stats[cid]['purchase_count'] += 1
        stats[cid]['products'].add(t['ProductName'])

    for cid in stats:
        stats[cid]['avg_order_value'] = round(stats[cid]['total_spent'] / stats[cid]['purchase_count'], 2)
        stats[cid]['products_bought'] = list(stats[cid].pop('products'))

    return dict(sorted(stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))
