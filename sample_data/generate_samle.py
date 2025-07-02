"""Generate realistic sample data for the dashboard demo"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate realistic e-commerce sample data"""
    np.random.seed(42)
    
    # Date range - last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Product data
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty']
    products = {
        'Electronics': ['iPhone 15', 'MacBook Pro', 'AirPods', 'iPad', 'Apple Watch'],
        'Clothing': ['Premium T-Shirt', 'Designer Jeans', 'Running Shoes', 'Winter Jacket', 'Summer Dress'],
        'Home & Garden': ['Coffee Maker', 'Plant Pot Set', 'Bed Sheets', 'Table Lamp', 'Robot Vacuum'],
        'Sports': ['Running Shoes', 'Yoga Mat', 'Dumbbell Set', 'Basketball', 'Mountain Bike'],
        'Books': ['Bestseller Novel', 'Cookbook', 'Self-Help Guide', 'Biography', 'Programming Book'],
        'Beauty': ['Anti-Aging Cream', 'Lipstick Set', 'Shampoo', 'Sunscreen', 'Perfume']
    }
    
    # Price ranges by category
    price_ranges = {
        'Electronics': (99, 2499),
        'Clothing': (19, 299),
        'Home & Garden': (15, 599),
        'Sports': (25, 899),
        'Books': (9, 79),
        'Beauty': (12, 149)
    }
    
    # US states for customer locations
    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
    
    sales_data = []
    customer_id = 1000
    
    for date in date_range:
        # Seasonal patterns
        seasonal_mult = 1.0
        if date.month in [11, 12]:  # Holiday boost
            seasonal_mult = 1.8
        elif date.month in [1, 2]:  # Post-holiday drop
            seasonal_mult = 0.6
        elif date.month in [6, 7, 8]:  # Summer boost
            seasonal_mult = 1.3
        
        # Weekend boost
        weekend_mult = 1.4 if date.weekday() >= 5 else 1.0
        
        # Daily transactions
        base_transactions = 20
        daily_transactions = max(1, int(base_transactions * seasonal_mult * weekend_mult * np.random.normal(1, 0.2)))
        
        for _ in range(daily_transactions):
            category = np.random.choice(categories)
            product = np.random.choice(products[category])
            
            min_price, max_price = price_ranges[category]
            unit_price = round(np.random.uniform(min_price, max_price), 2)
            quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.65, 0.1, 0.1, 0.12, 0.02, 0.01])
            total_amount = round(unit_price * quantity, 2)
            
            # Customer logic - 40% new, 60% returning
            if np.random.random() < 0.4:
                customer_id += 1
                current_customer = customer_id
            else:
                current_customer = np.random.randint(1000, customer_id + 1)
            
            location = np.random.choice(states)
            
            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'product_name': product,
                'category': category,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': total_amount,
                'customer_id': current_customer,
                'customer_location': location
            })
    
    df = pd.DataFrame(sales_data)
    df.to_csv('sample_data/sample_sales.csv', index=False)
    print(f"Generated {len(df)} sample records")
    return df

if __name__ == "__main__":
    generate_sample_data()