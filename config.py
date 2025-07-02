"""Configuration settings for the e-commerce dashboard"""

# App configuration
APP_TITLE = "E-commerce Sales Dashboard"
APP_ICON = "📊"
LAYOUT = "wide"

# Styling
PRIMARY_COLOR = "#FF6B6B"
BACKGROUND_COLOR = "#FFFFFF"
SECONDARY_BACKGROUND_COLOR = "#F0F2F6"
TEXT_COLOR = "#262730"

# Data processing
MAX_FILE_SIZE_MB = 200
SUPPORTED_FORMATS = ['csv', 'xlsx']
REQUIRED_COLUMNS = [
    'date', 'product_name', 'category', 'quantity', 
    'unit_price', 'total_amount', 'customer_id', 'customer_location'
]

# Sample data configuration
SAMPLE_DATA_MONTHS = 12
SAMPLE_DAILY_TRANSACTIONS = 15
SAMPLE_CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty']

# Export settings
PDF_PAGE_SIZE = "letter"
CSV_ENCODING = "utf-8"

# Contact information (update with your details)
CONTACT_EMAIL = "your-email@example.com"
SUPPORT_URL = "https://yourdomain.com/support"
DEMO_URL = "https://your-app-name.streamlit.app"

# License information
LICENSE_TYPE = "Commercial"
VERSION = "1.0.0"
AUTHOR = "Your Name"