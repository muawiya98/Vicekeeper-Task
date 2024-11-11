import pandas as pd
import numpy as np
import os

# Load the data
root_path = 'C:\\Users\\user\\Desktop\\Task'
file_path = os.path.join(root_path, 'Test data.xlsx')
data = pd.read_excel(file_path)

# Display the first few rows to understand the data structure
print("Dataset Head:")
print(data.head())

# Check for missing values and handle them (Data Cleaning Step)
missing_data_summary = data.isnull().sum()
print("Missing Data Summary:")
print(missing_data_summary)

# For simplicity, let's drop rows with missing values if they are few, or use imputation if needed
data = data.dropna()

# Check for and remove duplicates if any
data = data.drop_duplicates()

# Data Summarization

# Calculate total sales, total profit, and average sales by region
region_sales_summary = data.groupby('Region').agg(
    total_sales=('Sales Amount', 'sum'),
    total_profit=('Profit', 'sum'),
    avg_sales=('Sales Amount', 'mean')
)
print("Region Sales Summary:")
print(region_sales_summary)

# Calculate total sales and profit by product category
product_category_summary = data.groupby('Product Category').agg(
    total_sales=('Sales Amount', 'sum'),
    total_profit=('Profit', 'sum')
)
print("Product Category Summary:")
print(product_category_summary)

# Calculate the profit margin for each order
data['Profit Margin'] = data['Profit'] / data['Sales Amount']

# Calculate the overall average profit margin
overall_avg_profit_margin = data['Profit Margin'].mean()
print("Overall Average Profit Margin:")
print(overall_avg_profit_margin)

# Trend Analysis

# Analyze sales trends by customer segment
segment_sales_summary = data.groupby('Customer Segment').agg(
    total_sales=('Sales Amount', 'sum'),
    total_profit=('Profit', 'sum')
)
print("Customer Segment Sales Summary:")
print(segment_sales_summary)

# Analyze sales trend by order date
# First, extract month or day to see if there are monthly trends
data['Order Month'] = data['Order Date'].dt.month
monthly_sales_trend = data.groupby('Order Month').agg(total_sales=('Sales Amount', 'sum'))
print("Monthly Sales Trend:")
print(monthly_sales_trend)

# Regional performance comparison
region_performance = region_sales_summary.sort_values(by='total_sales', ascending=False)
print("Region Performance Summary:")
print(region_performance)

# Insights and Recommendations

# Top-performing region in terms of total sales and profit
top_region = region_sales_summary.sort_values(by='total_sales', ascending=False).head(1)
print("Top-Performing Region (Sales):")
print(top_region)

# Product category with highest sales and profit margin
product_category_summary['profit_margin'] = product_category_summary['total_profit'] / product_category_summary['total_sales']
top_product_category = product_category_summary.sort_values(by='profit_margin', ascending=False).head(1)
print("Top Product Category by Profit Margin:")
print(top_product_category)

# Most profitable customer segment
top_customer_segment = segment_sales_summary.sort_values(by='total_profit', ascending=False).head(1)
print("Most Profitable Customer Segment:")
print(top_customer_segment)

# Identify underperforming regions or product categories for improvement
underperforming_regions = region_sales_summary[region_sales_summary['total_sales'] < region_sales_summary['total_sales'].mean()]
underperforming_categories = product_category_summary[product_category_summary['total_sales'] < product_category_summary['total_sales'].mean()]

print("Underperforming Regions:")
print(underperforming_regions)
print("Underperforming Product Categories:")
print(underperforming_categories)

# Recommendations based on insights
print("\nRecommendations:")
if top_region.empty:
    print("- No regions identified for strong performance.")
else:
    print(f"- Focus more marketing efforts in the {top_region.index[0]} region to capitalize on its high sales.")

if not underperforming_regions.empty:
    print(f"- Consider running targeted campaigns or promotions in underperforming regions: {', '.join(underperforming_regions.index)}")

if not underperforming_categories.empty:
    print(f"- Evaluate potential improvements or promotions for underperforming product categories: {', '.join(underperforming_categories.index)}")

if not top_customer_segment.empty:
    print(f"- Invest in loyalty programs or exclusive offers for the {top_customer_segment.index[0]} customer segment, as it is the most profitable.")

# Save the summarized data for reporting
region_sales_summary.to_csv(os.path.join(root_path, 'Region_Sales_Summary.csv'))
product_category_summary.to_csv(os.path.join(root_path, 'Product_Category_Summary.csv'))
segment_sales_summary.to_csv(os.path.join(root_path, 'Customer_Segment_Summary.csv'))
monthly_sales_trend.to_csv(os.path.join(root_path, 'Monthly_Sales_Trend.csv'))
