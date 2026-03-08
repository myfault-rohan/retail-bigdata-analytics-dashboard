import pandas as pd
import time
import random
from datetime import datetime
import os

# Configuration
DATA_DIR = "data"
LIVE_DATA_FILE = os.path.join(DATA_DIR, "live_sales.csv")
COUNTRIES = ["USA", "UK", "India", "Germany", "France"]
PRODUCTS = ["Laptop", "Phone", "Tablet", "Headphones", "Camera"]

def generate_live_sales():
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # Check if file exists, if not write header: timestamp, country, product, quantity, price
    if not os.path.exists(LIVE_DATA_FILE):
        df_header = pd.DataFrame(columns=["timestamp", "country", "product", "quantity", "price"])
        df_header.to_csv(LIVE_DATA_FILE, index=False)

    print(f"Starting real-time sales simulation. Appending to {LIVE_DATA_FILE}...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            # Generate random record
            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "country": random.choice(COUNTRIES),
                "product": random.choice(PRODUCTS),
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(100.0, 2000.0), 2)
            }
            
            # Print to terminal as requested
            print(f"Generated Sale: {record['timestamp']} | {record['country']} | {record['product']} | Qty: {record['quantity']} | Price: ${record['price']}")
            
            # Append to CSV
            df = pd.DataFrame([record])
            df.to_csv(LIVE_DATA_FILE, mode='a', header=False, index=False)
            
            # Wait for 2 seconds
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    generate_live_sales()
