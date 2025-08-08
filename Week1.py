import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

#  Step 1: Setup

sns.set(style='whitegrid')
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load dataset
df = pd.read_csv(
    r"C:\Users\saadk\Desktop\Projects\Sample - Superstore.csv",
    parse_dates=['Order Date', 'Ship Date'],
    encoding='ISO-8859-1'
)

# Clean dataset
df.dropna(inplace=True)
df['Month'] = df['Order Date'].dt.to_period('M')


# Step 2: Analysis

category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
monthly_sales = df.groupby('Month')['Sales'].sum()
subcat_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()


# Step 3: Generate & Save Plots

def save_plot(name):
    return os.path.join(output_dir, name)

# Sales by Category
category_sales.plot(kind='bar', color='skyblue', title='Sales by Category')
plt.ylabel('Sales')
plt.tight_layout()
plt.savefig(save_plot('sales_by_category.png'))
plt.close()

# Profit by Region
region_profit.plot(kind='bar', color='salmon', title='Profit by Region')
plt.ylabel('Profit')
plt.tight_layout()
plt.savefig(save_plot('profit_by_region.png'))
plt.close()

# Monthly Sales
monthly_sales.plot(kind='line', marker='o', color='green', title='Monthly Sales Trend')
plt.ylabel('Sales')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(save_plot('monthly_sales_trend.png'))
plt.close()

# Heatmap: Region vs Category
plt.figure(figsize=(8, 6))
heatmap_data = df.pivot_table(index='Region', columns='Category', values='Sales', aggfunc='sum')
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlGnBu')
plt.title('Sales Heatmap: Region vs Category')
plt.tight_layout()
plt.savefig(save_plot('heatmap_region_category.png'))
plt.close()

# Profit by Sub-Category
subcat_profit.plot(kind='barh', color='mediumpurple', title='Profit by Sub-Category')
plt.xlabel('Profit')
plt.tight_layout()
plt.savefig(save_plot('profit_by_subcategory.png'))
plt.close()


# Step 4: Create PDF Report

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 8, "- Technology category has the highest total sales.", ln=True)


# Section: Key Insights
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Superstore Sales Analysis Report", ln=True)

# Section: Key Insights
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, "Key Insights:", ln=True)
pdf.set_font("Arial", '', 11)
insights = [
    "- Technology category has the highest total sales.",
    "- The West region earns the most profit.",
    "- Sales peak during November and December.",
    "- Bookcases and Tables are the least profitable sub-categories.",
    "- Heatmap shows high sales concentration in Technology in the West region."
]
for insight in insights:
    pdf.cell(0, 8, insight, ln=True)


# Section: Charts
pdf.set_font("Arial", 'B', 12)
pdf.ln(5)
pdf.cell(0, 10, "Visual Analysis:", ln=True)

def add_image(pdf, path, title):
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, title, ln=True)
    pdf.image(path, w=170)
    pdf.ln(5)

add_image(pdf, save_plot('sales_by_category.png'), "Sales by Category")
add_image(pdf, save_plot('profit_by_region.png'), "Profit by Region")
add_image(pdf, save_plot('monthly_sales_trend.png'), "Monthly Sales Trend")
add_image(pdf, save_plot('heatmap_region_category.png'), "Region vs Category Heatmap")
add_image(pdf, save_plot('profit_by_subcategory.png'), "Profit by Sub-Category")

# Save the PDF
pdf_path = os.path.join(output_dir, "superstore_sales_report.pdf")
pdf.output(pdf_path)

print(f" PDF report generated: {pdf_path}")
