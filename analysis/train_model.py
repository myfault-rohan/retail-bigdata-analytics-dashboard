import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

def main():
    # Load the dataset from data/sales_data.csv
    try:
        df = pd.read_csv('data/sales_data.csv', encoding='unicode_escape')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Map dataset columns to requested names if they differ
    col_mapping = {
        'QUANTITYORDERED': 'Quantity',
        'PRICEEACH': 'UnitPrice',
        'COUNTRY': 'Country'
    }
    df.rename(columns={'QUANTITYORDERED': 'Quantity', 'PRICEEACH': 'UnitPrice', 'COUNTRY': 'Country'}, inplace=True)

    # Create a new column called Sales calculated as: Quantity * UnitPrice
    df['Sales'] = df['Quantity'] * df['UnitPrice']

    # Aggregate total sales per country
    country_sales = df.groupby('Country')['Sales'].sum().reset_index()
    country_sales.rename(columns={'Sales': 'total_sales'}, inplace=True)

    # To predict total_sales based on Quantity and UnitPrice,
    # we use the transaction-level data and map Sales -> total_sales
    df['total_sales'] = df['Sales']
    
    # Drop rows with missing values in our training columns to ensure fit() works correctly
    df = df.dropna(subset=['Quantity', 'UnitPrice', 'total_sales'])
    
    X = df[['Quantity', 'UnitPrice']]
    y = df['total_sales']

    # Train the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Save the trained model using pickle as: analysis/sales_model.pkl
    os.makedirs('analysis', exist_ok=True)
    with open('analysis/sales_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Print "Model trained successfully"
    print("Model trained successfully")

if __name__ == '__main__':
    main()
