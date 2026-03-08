import csv
import random
import time
import os

# List of allowed countries based on requirements
COUNTRIES = ['UK', 'Germany', 'France', 'Spain', 'Netherlands', 'Italy', 'USA']
LIVE_DATA_FILE = "data/live_sales.csv"

def generate_transaction():
    """Generates a single random retail transaction."""
    country = random.choice(COUNTRIES)
    quantity = random.randint(1, 10)
    # Using random.uniform for price to get a realistic float value
    # and rounding it to 2 decimal places
    unit_price = round(random.uniform(1.0, 100.0), 2)
    sales = round(quantity * unit_price, 2)

    transaction = {
        "Country": country,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Sales": sales
    }
    
    return transaction

def main():
    print("Starting simulated retail sales data stream...")
    print(f"Writing live data to {LIVE_DATA_FILE}")
    print("Press Ctrl+C to stop.\n")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(LIVE_DATA_FILE), exist_ok=True)
    
    # Check if the file exists to determine if we need to write headers
    file_exists = os.path.isfile(LIVE_DATA_FILE)
    
    # Define our CSV columns
    fieldnames = ['Country', 'Quantity', 'UnitPrice', 'Sales']
    
    try:
        # Open the file in append mode
        with open(LIVE_DATA_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # If the file does not exist, create it with headers
            if not file_exists:
                writer.writeheader()
                f.flush()
                
            while True:
                # Generate the random data
                data = generate_transaction()
                
                # Print each generated record in the terminal
                print(data)
                
                # Keep appending new records continuously
                writer.writerow(data)
                f.flush() # Ensure it's immediately written to disk
                
                # Generate data every 2 seconds
                time.sleep(2)
                
    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")

if __name__ == "__main__":
    main()
