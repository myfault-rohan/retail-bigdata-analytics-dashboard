import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define file paths relative to project root
DATA_PATH = "data/processed_sales.csv"
PREDICTION_PATH = "data/sales_predictions.csv"

# Show a page title: "Retail Big Data Analytics Dashboard"
st.title("Retail Big Data Analytics Dashboard")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    # --- Historical Data Section ---
    df = load_data(DATA_PATH)

    st.sidebar.header("Historical Metrics")
    sales_col = 'total_sales'

    if sales_col in df.columns:
        total_global_sales = df[sales_col].sum()
        st.sidebar.markdown(f"**Total Global Sales:** ${total_global_sales:,.2f}")
    
    if 'Country' in df.columns:
        num_countries = df['Country'].nunique()
        st.sidebar.markdown(f"**Number of Countries:** {num_countries}")
    else:
        st.sidebar.warning("Historical dataset missing 'Country' column.")

    st.subheader("Processed Dataset Overview")
    st.dataframe(df)

    if 'Country' in df.columns and sales_col in df.columns:
        chart_data = df.groupby('Country')[sales_col].sum().reset_index()
        chart_data = chart_data.sort_values(by=sales_col, ascending=False)
        
        top_n = 10
        top_n_data = chart_data.head(top_n)

        st.subheader(f"Top {top_n} Countries vs Total Sales")
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        ax_bar.bar(top_n_data['Country'], top_n_data[sales_col], color='royalblue', edgecolor='midnightblue')
        
        plt.xticks(rotation=45, ha='right')
        ax_bar.set_xlabel("Country")
        ax_bar.set_ylabel("Total Sales")
        ax_bar.set_title(f"Top {top_n} Countries by Total Sales")
        plt.tight_layout()
        st.pyplot(fig_bar)

        st.subheader(f"Sales Distribution (Top {top_n} Countries)")
        fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
        ax_pie.pie(
            top_n_data[sales_col], 
            labels=top_n_data['Country'], 
            autopct='%1.1f%%', 
            startangle=140,
            colors=plt.cm.Paired.colors
        )
        ax_pie.set_title(f"Sales Distribution for Top {top_n} Countries")
        st.pyplot(fig_pie)
    else:
        st.error(f"Could not generate historical charts. Expected columns 'Country' and '{sales_col}' in dataset.")

    st.markdown("---")  # Add a visual separator

    # --- AI Prediction Section ---
    st.header("AI Sales Prediction")
    
    try:
        pred_df = load_data(PREDICTION_PATH)
        
        # 3. Display predicted sales for each country.
        st.subheader("Predicted Sales Data")
        st.dataframe(pred_df[['Country', 'Predicted_Sales']])
        
        # 5. Allow user to select a country and see its predicted value.
        st.subheader("Country Prediction Lookup")
        countries_list = pred_df['Country'].sort_values().unique()
        selected_country = st.selectbox("Select a country to view its predicted sales:", countries_list)
        
        if selected_country:
            country_pred = pred_df[pred_df['Country'] == selected_country]['Predicted_Sales'].values[0]
            st.success(f"Predicted Sales for **{selected_country}**: **${country_pred:,.2f}**")
        
        # 4. Show a bar chart of predicted sales.
        st.subheader("Predicted Sales by Country (Top 10)")
        
        # Sort predictions and take top 10 for readability in the chart
        top_pred_data = pred_df.sort_values(by='Predicted_Sales', ascending=False).head(10)
        
        fig_pred_bar, ax_pred_bar = plt.subplots(figsize=(10, 6))
        # Use a different color (like green) to distinguish predictions from historical data
        ax_pred_bar.bar(top_pred_data['Country'], top_pred_data['Predicted_Sales'], color='mediumseagreen', edgecolor='darkgreen')
        
        plt.xticks(rotation=45, ha='right')
        ax_pred_bar.set_xlabel("Country")
        ax_pred_bar.set_ylabel("Predicted Sales")
        ax_pred_bar.set_title("Top 10 Countries by Predicted Sales")
        plt.tight_layout()
        st.pyplot(fig_pred_bar)
        
    except FileNotFoundError:
        st.warning(f"Prediction data not found at `{PREDICTION_PATH}`. Please run the sales prediction script first.")

except FileNotFoundError:
    st.error(f"Error: Historical data file not found at path `{DATA_PATH}`. Please make sure the file exists.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
