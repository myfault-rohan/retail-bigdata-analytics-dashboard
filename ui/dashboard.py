import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import json
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import warnings
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import time
import subprocess
import os

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Set page configuration
st.set_page_config(page_title="Retail AI Analytics Platform", layout="wide")

# Define file paths
DATA_PATH = "data/processed_sales.csv"
MODEL_PATH = "analysis/sales_model.pkl"
LIVE_DATA_FILE = "data/live_sales.csv"

# Global Branding
def show_branding():
    st.markdown('<h1 style="text-align: center; color: #4A90E2; font-family: \'Inter\', sans-serif; font-weight: 800; font-size: 3.5rem; margin-bottom: 0px;">Retail AI Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #B0B0B0; margin-top: 0px; margin-bottom: 2rem; font-size: 1.2rem;">Advanced Retail Solutions</p>', unsafe_allow_html=True)

# Load configuration
with open('ui/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize Authenticator
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stForm"] {
        border: 2px solid #4A90E2;
        border-radius: 15px;
        padding: 30px;
        background-color: #1E1E1E;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .main .block-container {
        padding-top: 3rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .login-title { text-align: center; color: #4A90E2; font-weight: 800; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .login-subtitle { text-align: center; color: #B0B0B0; font-size: 1.2rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_raw_retail_data():
    raw_path = "data/online_retail.csv"
    if os.path.exists(raw_path):
        # We only load necessary columns to save memory and time
        return pd.read_csv(raw_path, usecols=['InvoiceNo', 'Quantity', 'UnitPrice', 'Country'])
    return pd.DataFrame()

# --- Page Functions ---

def page_overview(df_processed):
    st.title("Platform Overview")
    st.header("Global Business Metrics")
    
    # Load raw data for high-precision metrics
    raw_df = load_raw_retail_data()
    
    if not raw_df.empty:
        # 1. Total Revenue: sum(quantity * unitprice)
        total_revenue = (raw_df['Quantity'] * raw_df['UnitPrice']).sum()
        
        # 2. Total Orders: count of unique InvoiceNo
        total_orders = raw_df['InvoiceNo'].nunique()
        
        # 3. Active Countries: count distinct Country
        active_countries = raw_df['Country'].nunique()
        
        # 4. Average Order Value: Total Revenue / Total Orders
        aov = total_revenue / total_orders if total_orders > 0 else 0
        
        # Display in 4 columns
        col1, col2, col3, col4 = st.columns(4)
        
        def metric_card(title, value, icon):
            return f"""
            <div style="background-color: #1E1E1E; border: 1px solid #4A90E2; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
                <h3 style="color: #B0B0B0; font-size: 1.2rem; margin-bottom: 5px; font-weight: normal;">{icon} {title}</h3>
                <h1 style="color: #4A90E2; font-size: 2.5rem; margin: 0; font-weight: bold;">{value}</h1>
            </div>
            """
            
        col1.markdown(metric_card("Total Revenue", f"${total_revenue:,.2f}", "💰"), unsafe_allow_html=True)
        col2.markdown(metric_card("Total Orders", f"{total_orders:,}", "📦"), unsafe_allow_html=True)
        col3.markdown(metric_card("Active Countries", str(active_countries), "🌍"), unsafe_allow_html=True)
        col4.markdown(metric_card("Avg Order Value", f"${aov:,.2f}", "📊"), unsafe_allow_html=True)
    else:
        st.warning("Raw business metrics unavailable. Ensure `data/online_retail.csv` exists.")

    st.markdown("---")
    st.subheader("Historical Data Insights")
    st.markdown("This section provides a high-level view of the processed historical retail data.")
    st.dataframe(df_processed.head(100), use_container_width=True)

def page_live_monitor():
    st.title("Real-Time Sales Monitor")
    st.markdown("Tracking live transactions as they happen.")
    
    try:
        live_df_full = load_data(LIVE_DATA_FILE)
        if not live_df_full.empty:
            # Compatibility mapping
            if 'country' in live_df_full.columns:
                live_df_full = live_df_full.rename(columns={
                    'country': 'Country', 
                    'price': 'Sales', 
                    'timestamp': 'Time',
                    'product': 'Product',
                    'quantity': 'Quantity'
                })
            
            # Display Table
            st.subheader("Latest 20 Transactions")
            live_df_reversed = live_df_full.iloc[::-1].reset_index(drop=True)
            st.dataframe(live_df_reversed.head(20), use_container_width=True)
            
            # Trend Chart
            st.subheader("Live Sales Trend")
            
            # Convert 'Time' to datetime if needed or just use it directly
            trend_data = live_df_full.groupby('Time')['Sales'].sum().reset_index()
            fig_trend = px.line(trend_data, x='Time', y='Sales', title="Live Sales Trend", template="plotly_dark", markers=True)
            st.plotly_chart(fig_trend, width='stretch')
            
            # Charts
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("Live Sales by Country")
                country_data = live_df_full.groupby('Country')['Sales'].sum().reset_index()
                fig_c = px.bar(country_data, x='Country', y='Sales', color='Country', title="Live Sales by Country", template="plotly_dark")
                st.plotly_chart(fig_c, width='stretch')
                
            with c2:
                st.subheader("Live Sales by Product")
                product_data = live_df_full.groupby('Product')['Sales'].sum().reset_index()
                fig_p = px.bar(product_data, x='Product', y='Sales', color='Product', title="Live Sales by Product", template="plotly_dark")
                st.plotly_chart(fig_p, width='stretch')
                
            st.info(f"Total live transactions captured: {len(live_df_full)}")
        else:
            st.info("Waiting for live data... Please ensure the simulator is running.")
    except Exception as e:
        st.error(f"Error accessing live stream: {e}")

def page_analytics(df):
    st.title("Sales Analytics")
    
    # Sidebar Filters
    st.sidebar.header("Analytics Filters")
    if not df.empty and 'Country' in df.columns:
        all_countries = df['Country'].unique().tolist()
        selected_countries = st.sidebar.multiselect("Select Countries", options=all_countries, default=all_countries)
        top_n = st.sidebar.slider("Top Countries to Display", 5, 20, 10)
        
        filtered_df = df[df['Country'].isin(selected_countries)] if selected_countries else df
        sales_col = 'total_sales'
        
        # Map
        chart_data = filtered_df.groupby('Country')[sales_col].sum().reset_index()
        fig_map = px.choropleth(
            chart_data, 
            locations="Country", 
            locationmode="country names", 
            color=sales_col,
            hover_name="Country",
            hover_data={sales_col: ':$,.2f', 'Country': False},
            color_continuous_scale="Plasma", 
            template="plotly_dark",
            title="Global Sales Distribution"
        )
        fig_map.update_layout(
            title_x=0.5,
            title_font_size=24,
            geo=dict(showframe=False, projection_type='natural earth'),
            height=650,
            margin=dict(l=0, r=0, t=60, b=0)
        )
        
        # Center the chart on the page
        map_col1, map_col2, map_col3 = st.columns([1, 8, 1])
        with map_col2:
            st.plotly_chart(fig_map, width='stretch')
        
        # Charts
        c1, c2 = st.columns(2)
        top_n_data = chart_data.sort_values(by=sales_col, ascending=False).head(top_n)
        
        with c1:
            st.subheader(f"Top {top_n} Countries")
            fig_bar = px.bar(top_n_data, x='Country', y=sales_col, color=sales_col, color_continuous_scale="Viridis", template="plotly_dark")
            st.plotly_chart(fig_bar, width='stretch')
        with c2:
            st.subheader("Regional Allocation")
            fig_pie = px.pie(chart_data, names='Country', values=sales_col, template="plotly_dark")
            st.plotly_chart(fig_pie, width='stretch')
    else:
        st.error("No data available for analytics.")

def page_predictions():
    st.title("ML Demand Predictions")
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        st.subheader("Sales Forecasting Tool")
        c1, c2 = st.columns(2)
        qty = c1.number_input("Input Quantity", min_value=1, value=10)
        price = c2.number_input("Unit Price", min_value=0.01, value=5.0)
        
        if st.button("Generate Prediction"):
            input_df = pd.DataFrame([[qty, price]], columns=['Quantity', 'UnitPrice'])
            pred = model.predict(input_df)[0]
            pred = max(pred, 0)
            st.success(f"Estimated Sales Value: ${pred:,.2f}")
            
    except FileNotFoundError:
        st.warning("Prediction model not found. Please train the model first.")

def page_reports():
    st.title("Business Reports")
    st.markdown("Generate and download comprehensive analytics reports.")
    
    if st.button("Run Report Generator"):
        with st.spinner("Processing reports..."):
            subprocess.run(["python", "analysis/report_generator.py"])
        st.success("Reports are ready for download!")

    if os.path.exists("sales_report.pdf") and os.path.exists("sales_report.xlsx"):
        c1, c2 = st.columns(2)
        with c1:
            with open("sales_report.pdf", "rb") as f:
                st.download_button("Download PDF Report", f, "sales_report.pdf", "application/pdf")
        with c2:
            with open("sales_report.xlsx", "rb") as f:
                st.download_button("Download Excel Report", f, "sales_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("No reports found. Click the button above to generate them.")

# --- Main App Logic ---

if not st.session_state.get("authentication_status"):
    show_branding()
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="login-title">Platform Login</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Secure Access Required</p>', unsafe_allow_html=True)
        authenticator.login()
        if st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.info('Please enter your credentials.')

if st.session_state.get("authentication_status"):
    # Clear login view variables if needed or show loading
    if 'spinner_shown' not in st.session_state:
        with st.spinner("Initializing analytics platform..."):
            time.sleep(2)
        st.session_state['spinner_shown'] = True

    # Sidebar Navigation
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.markdown(f"**User:** {st.session_state['name']}")
    st.sidebar.divider()
    
    page = st.sidebar.selectbox(
        "Navigation Menu",
        ["Overview", "Live Sales Monitor", "Sales Analytics", "ML Predictions", "Business Reports"]
    )
    
    show_branding()
    
    # Dynamic refresh based on page
    if page == "Live Sales Monitor":
        st_autorefresh(interval=2000, key="live_refresh")
    else:
        st_autorefresh(interval=10000, key="global_refresh")
    
    df_hist = load_data(DATA_PATH)

    if page == "Overview":
        page_overview(df_hist)
    elif page == "Live Sales Monitor":
        page_live_monitor()
    elif page == "Sales Analytics":
        page_analytics(df_hist)
    elif page == "ML Predictions":
        page_predictions()
    elif page == "Business Reports":
        page_reports()

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888888; font-size: 0.85rem; margin-top: 2rem;'>
            <b>Retail AI Analytics Platform</b><br>
            Built with Python, Apache Spark, and Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
