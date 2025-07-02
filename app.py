import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Page configuration
st.set_page_config(
    page_title="E-commerce Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Generate realistic sample e-commerce data"""
    np.random.seed(42)
    
    # Generate date range for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Product categories and names
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty']
    products = {
        'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Tablet', 'Smart Watch'],
        'Clothing': ['T-Shirt', 'Jeans', 'Sneakers', 'Jacket', 'Dress'],
        'Home & Garden': ['Coffee Maker', 'Plant Pot', 'Bed Sheets', 'Lamp', 'Vacuum'],
        'Sports': ['Running Shoes', 'Yoga Mat', 'Dumbbell', 'Basketball', 'Bicycle'],
        'Books': ['Fiction Novel', 'Cookbook', 'Self-Help', 'Biography', 'Textbook'],
        'Beauty': ['Moisturizer', 'Lipstick', 'Shampoo', 'Sunscreen', 'Perfume']
    }
    
    # Generate sales data
    sales_data = []
    customer_id_counter = 1000
    
    for date in date_range:
        # Seasonal patterns - higher sales in Nov-Dec, lower in Jan-Feb
        seasonal_multiplier = 1.0
        if date.month in [11, 12]:  # Holiday season
            seasonal_multiplier = 1.5
        elif date.month in [1, 2]:  # Post-holiday drop
            seasonal_multiplier = 0.7
        
        # Weekend boost
        weekend_multiplier = 1.2 if date.weekday() >= 5 else 1.0
        
        # Number of transactions per day
        base_transactions = 15
        daily_transactions = max(1, int(base_transactions * seasonal_multiplier * weekend_multiplier * np.random.normal(1, 0.3)))
        
        for _ in range(daily_transactions):
            category = np.random.choice(categories)
            product = np.random.choice(products[category])
            
            # Price based on category
            price_ranges = {
                'Electronics': (50, 1200),
                'Clothing': (15, 150),
                'Home & Garden': (10, 300),
                'Sports': (20, 400),
                'Books': (8, 50),
                'Beauty': (5, 80)
            }
            
            min_price, max_price = price_ranges[category]
            unit_price = round(np.random.uniform(min_price, max_price), 2)
            quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.6, 0.1, 0.1, 0.15, 0.04, 0.01])
            total_amount = round(unit_price * quantity, 2)
            
            # Customer location (US states)
            states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI', 
                     'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
            location = np.random.choice(states)
            
            # Customer ID (mix of new and returning)
            if np.random.random() < 0.3 or customer_id_counter <= 1000:  # 30% new customers OR if no existing customers
                customer_id = customer_id_counter
                customer_id_counter += 1
            else:  # 70% returning customers (only if we have existing customers)
                customer_id = np.random.randint(1000, customer_id_counter)
            
            sales_data.append({
                'date': date,
                'product_name': product,
                'category': category,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': total_amount,
                'customer_id': customer_id,
                'customer_location': location
            })
    
    return pd.DataFrame(sales_data)

def process_data(df):
    """Process and clean the uploaded data"""
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Calculate additional metrics
    df['month'] = df['date'].dt.to_period('M')
    df['week'] = df['date'].dt.to_period('W')
    df['day_of_week'] = df['date'].dt.day_name()
    
    return df

def create_sales_trend_chart(df):
    """Create sales trend visualization"""
    daily_sales = df.groupby('date')['total_amount'].sum().reset_index()
    
    fig = px.line(daily_sales, x='date', y='total_amount',
                  title='Daily Sales Trend',
                  labels={'total_amount': 'Sales ($)', 'date': 'Date'})
    
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        height=400
    )
    
    return fig

def create_product_performance_chart(df):
    """Create top products chart"""
    product_sales = df.groupby('product_name')['total_amount'].sum().sort_values(ascending=True).tail(10)
    
    fig = px.bar(x=product_sales.values, y=product_sales.index,
                 orientation='h',
                 title='Top 10 Products by Revenue',
                 labels={'x': 'Revenue ($)', 'y': 'Product'})
    
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        height=500
    )
    
    return fig

def create_category_pie_chart(df):
    """Create category distribution pie chart"""
    category_sales = df.groupby('category')['total_amount'].sum()
    
    fig = px.pie(values=category_sales.values, names=category_sales.index,
                 title='Sales by Category')
    
    fig.update_layout(
        title_font_size=20,
        height=400
    )
    
    return fig

def create_geographic_chart(df):
    """Create geographic sales distribution"""
    geo_sales = df.groupby('customer_location')['total_amount'].sum().sort_values(ascending=False).head(15)
    
    fig = px.bar(x=geo_sales.index, y=geo_sales.values,
                 title='Sales by State (Top 15)',
                 labels={'x': 'State', 'y': 'Revenue ($)'})
    
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        height=400
    )
    
    return fig

def calculate_kpis(df):
    """Calculate key performance indicators"""
    total_revenue = df['total_amount'].sum()
    total_orders = len(df)
    unique_customers = df['customer_id'].nunique()
    avg_order_value = df['total_amount'].mean()
    
    # Calculate month-over-month growth
    monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum()
    if len(monthly_sales) >= 2:
        mom_growth = ((monthly_sales.iloc[-1] - monthly_sales.iloc[-2]) / monthly_sales.iloc[-2]) * 100
    else:
        mom_growth = 0
    
    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'unique_customers': unique_customers,
        'avg_order_value': avg_order_value,
        'mom_growth': mom_growth
    }

def generate_pdf_report(df, kpis):
    """Generate PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("E-commerce Sales Dashboard Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # KPIs
    kpi_text = f"""
    <b>Key Performance Indicators:</b><br/>
    • Total Revenue: ${kpis['total_revenue']:,.2f}<br/>
    • Total Orders: {kpis['total_orders']:,}<br/>
    • Unique Customers: {kpis['unique_customers']:,}<br/>
    • Average Order Value: ${kpis['avg_order_value']:.2f}<br/>
    • Month-over-Month Growth: {kpis['mom_growth']:.1f}%<br/>
    """
    
    kpi_para = Paragraph(kpi_text, styles['Normal'])
    story.append(kpi_para)
    story.append(Spacer(1, 12))
    
    # Top products
    top_products = df.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).head(5)
    products_text = "<b>Top 5 Products:</b><br/>"
    for i, (product, revenue) in enumerate(top_products.items(), 1):
        products_text += f"{i}. {product}: ${revenue:,.2f}<br/>"
    
    products_para = Paragraph(products_text, styles['Normal'])
    story.append(products_para)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 E-commerce Sales Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Dashboard Controls")
    
    # Data source selection
    data_source = st.sidebar.radio(
        "Choose Data Source:",
        ["Use Sample Data", "Upload Your Data"]
    )
    
    # Load data based on selection
    if data_source == "Use Sample Data":
        df = load_sample_data()
        st.sidebar.success("✅ Sample data loaded successfully!")
        st.sidebar.info("This demo uses 12 months of realistic e-commerce data with seasonal patterns.")
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload your sales data (CSV or Excel)",
            type=['csv', 'xlsx'],
            help="File should contain columns: date, product_name, category, quantity, unit_price, total_amount, customer_id, customer_location"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                df = process_data(df)
                st.sidebar.success("✅ Data uploaded successfully!")
            except Exception as e:
                st.sidebar.error(f"Error loading file: {str(e)}")
                df = load_sample_data()  # Fallback to sample data
        else:
            df = load_sample_data()  # Default to sample data
    
    # Date range filter
    if not df.empty:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    
    # Main dashboard
    if not df.empty:
        # Calculate KPIs
        kpis = calculate_kpis(df)
        
        # Display KPIs
        st.subheader("📈 Key Performance Indicators")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
        with col2:
            st.metric("Total Orders", f"{kpis['total_orders']:,}")
        with col3:
            st.metric("Unique Customers", f"{kpis['unique_customers']:,}")
        with col4:
            st.metric("Avg Order Value", f"${kpis['avg_order_value']:.2f}")
        with col5:
            st.metric("MoM Growth", f"{kpis['mom_growth']:.1f}%", 
                     delta=f"{kpis['mom_growth']:.1f}%")
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_sales_trend_chart(df), use_container_width=True)
            st.plotly_chart(create_category_pie_chart(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_product_performance_chart(df), use_container_width=True)
            st.plotly_chart(create_geographic_chart(df), use_container_width=True)
        
        # Data table
        st.subheader("📋 Recent Transactions")
        st.dataframe(df.sort_values('date', ascending=False).head(100), use_container_width=True)
        
        # Export functionality
        st.subheader("📥 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download CSV Data"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📄 Generate PDF Report"):
                pdf_buffer = generate_pdf_report(df, kpis)
                st.download_button(
                    label="💾 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
    
    else:
        st.error("No data available. Please upload a file or use sample data.")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🚀 <strong>Professional E-commerce Analytics Dashboard</strong></p>
        <p>Built with Streamlit & Plotly | Need a custom dashboard? <a href='mailto:your-email@example.com'>Contact us</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()