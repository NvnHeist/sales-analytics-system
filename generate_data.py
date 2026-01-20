import random


def generate_sample_data():
    header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region\n"
    data = [header]

    regions = ['North', 'South', 'East', 'West']
    products = [('P101', 'Laptop'), ('P102', 'Mouse,Wireless'), ('P103', 'Keyboard'), ('P104', 'Monitor')]

    # Generate 70 VALID records
    for i in range(1, 71):
        t_id = f"T{100 + i:03d}"
        p_id, p_name = random.choice(products)
        qty = random.randint(1, 5)
        price = random.randint(50, 1500)
        c_id = f"C{500 + i:03d}"
        region = random.choice(regions)
        data.append(f"{t_id}|2024-12-{random.randint(1, 28):02d}|{p_id}|{p_name}|{qty}|{price}|{c_id}|{region}\n")

    # Generate 10 INVALID records (to meet the ~10 requirement)
    invalid_examples = [
        "X999|2024-12-01|P101|Laptop|1|500|C001|North\n",  # Wrong TransactionID start
        "T999|2024-12-01|Z101|Laptop|1|500|C001|North\n",  # Wrong ProductID start
        "T998|2024-12-01|P101|Laptop|0|500|C001|North\n",  # Zero Quantity
        "T997|2024-12-01|P101|Laptop|2|-50|C001|North\n",  # Negative Price
        "T996|2024-12-01|P101|Laptop|1|500||South\n",  # Missing CustomerID
        "T995|2024-12-01|P101|Laptop|1|500|C002|\n",  # Missing Region
        "T994|2024-12-01|P101|Laptop|1|1,500|B001|East\n",  # Wrong CustomerID start
        "T993|2024-12-01|P101|Laptop|abc|500|C003|West\n",  # Non-numeric Quantity
        "T992|2024-12-01|P101|Laptop|1|500\n",  # Missing Columns
        " \n"  # Empty line
    ]
    data.extend(invalid_examples)

    with open('data/sales_data.txt', 'w', encoding='latin-1') as f:
        f.writelines(data)
    print("Successfully generated data/sales_data.txt with 80 records.")


if __name__ == "__main__":
    generate_sample_data()