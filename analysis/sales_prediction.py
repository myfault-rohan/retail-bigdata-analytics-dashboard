import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import os

# Define file paths relative to project root
DATA_PATH = "data/processed_sales.csv"
OUTPUT_PATH = "data/sales_predictions.csv"

def main():
    print("Loading processed sales data...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find {DATA_PATH}. Please make sure the data exists.")
        return

    # 3. Use Country as categorical feature
    if 'Country' not in df.columns or 'total_sales' not in df.columns:
        print("Error: Required columns 'Country' and 'total_sales' not found in dataset.")
        return

    # Clean data - drop rows with missing values in our features/target
    df = df.dropna(subset=['Country', 'total_sales'])

    print("Encoding categorical features...")
    # 5. Encode Country using LabelEncoder
    le = LabelEncoder()
    # We create a new column 'Country_Encoded' to use as our feature (X)
    df['Country_Encoded'] = le.fit_transform(df['Country'])

    # Define our feature matrix (X) and target vector (y)
    # Using double brackets for X to ensure it's a 2D array/DataFrame as expected by sklearn
    X = df[['Country_Encoded']]
    
    # 4. Use total_sales as the target variable
    y = df['total_sales']

    print("Training Linear Regression model...")
    # 6. Train a Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    print("Generating predictions...")
    # 7. Predict sales for the next period
    # For a simple linear regression based solely on 'Country', 
    # we predict the sales based on the encoded countries we have.
    predictions = model.predict(X)

    # Create a DataFrame with the results
    results_df = pd.DataFrame({
        'Country': df['Country'],
        'Country_Encoded': df['Country_Encoded'],
        'Actual_Sales': y,
        'Predicted_Sales': predictions
    })

    # Drop duplicates to show one prediction per country 
    # (since the model only uses Country, the prediction is the same for a given country)
    unique_predictions = results_df.drop_duplicates(subset=['Country']).reset_index(drop=True)

    # 8. Print the predictions
    print("\n--- Sales Predictions by Country ---")
    print(unique_predictions[['Country', 'Predicted_Sales']].to_string(index=False))

    print(f"\nSaving predictions to {OUTPUT_PATH}...")
    # 9. Save predictions to: data/sales_predictions.csv
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    unique_predictions.to_csv(OUTPUT_PATH, index=False)
    print("Done!")

if __name__ == "__main__":
    main()
