import json
import random
import time
import os
from datetime import datetime

# List of allowed countries based on requirements
COUNTRIES = ['UK', 'Germany', 'France', 'Spain', 'Netherlands']
LIVE_DATA_FILE = "data/live_sales.jsonl"

def generate_transaction():
    """Generates a single random retail transaction simulating real-time activity."""
    country = random.choice(COUNTRIES)
    quantity = random.randint(1, 10)
    # Using random.uniform for price to get a realistic float value (e.g. 15.99)
    # and rounding it to 2 decimal places
    unit_price = round(random.uniform(1.0, 100.0), 2)
    
    # Adding a timestamp field as it's typically useful for streaming data processing
    timestamp = datetime.utcnow().isoformat() + "Z"

    transaction = {
        "timestamp": timestamp,
        "Country": country,
        "Quantity": quantity,
        "UnitPrice": unit_price
    }
    
    return transaction

def main():
    print("Starting simulated retail sales data stream...")
    print(f"Writing live data to {LIVE_DATA_FILE}")
    print("Press Ctrl+C to stop.\n")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(LIVE_DATA_FILE), exist_ok=True)
    
    # If the file exists, we'll append to it. 
    # If it gets too large in the future, we might want a truncate strategy, 
    # but for this demo appending is fine.
    try:
        while True:
            # Generate the random data
            data = generate_transaction()
            
            # Print to console for visibility
            json_data = json.dumps(data)
            print(json_data)
            
            # Write to the JSON Lines file
            with open(LIVE_DATA_FILE, 'a') as f:
                f.write(json_data + '\n')
            
            # Continuously generate data every 2 seconds
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nStreaming stopped by user.")

if __name__ == "__main__":
    main()
