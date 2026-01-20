import requests

def fetch_exchange_rates():
    """Fetches USD to EUR rate from a public API."""
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            rate = response.json()['rates']['EUR']
            print(f"\n[API] Current USD -> EUR Rate: {rate}")
            return rate
    except:
        print("\n[API] Could not fetch exchange rate.")
    return None