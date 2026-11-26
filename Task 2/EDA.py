import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset (Input)
df = pd.read_excel("ecommerce-orders-clean dataset.xlsx", sheet_name="Sheet1")

# Ensure Date is in datetime format for any time-series analysis
df['Date'] = pd.to_datetime(df['Date'])

# Visual style for our charts
sns.set_theme(style="whitegrid")

# Focus on the numerical columns
numeric_cols = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']

print("--- Five-Number Summary (Descriptive Statistics) ---")
stats = df[numeric_cols].describe().T
print(stats)

# Let's look at the distribution of TotalPrice
plt.figure(figsize=(12, 5))

# Histogram
plt.subplot(1, 2, 1)
sns.histplot(df['TotalPrice'], bins=30, kde=True, color='teal')
plt.title('Distribution of Total Price')
plt.xlabel('Total Price ($)')

# Boxplot (PDF Page 12 - "The Fingerprint of Variability")
plt.subplot(1, 2, 2)
sns.boxplot(x=df['TotalPrice'], color='teal')
plt.title('Boxplot of Total Price (Outlier Detection)')
plt.xlabel('Total Price ($)')

plt.tight_layout()
plt.show()

# 1. Calculate Q1 (25th percentile) and Q3 (75th percentile)
Q1 = df['TotalPrice'].quantile(0.25)
Q3 = df['TotalPrice'].quantile(0.75)

# 2. Calculate IQR (The middle 50% of data)
IQR = Q3 - Q1

# 3. Define the "Expected Range" (Whiskers)
lower_bound = Q1 - (1.5 * IQR)
upper_bound = Q3 + (1.5 * IQR)

print(f"Q1: {Q1:.2f} | Q3: {Q3:.2f} | IQR: {IQR:.2f}")
print(f"Lower Bound: {lower_bound:.2f} | Upper Bound: {upper_bound:.2f}")

# 4. Find the Outliers
outliers = df[(df['TotalPrice'] < lower_bound) | (df['TotalPrice'] > upper_bound)]
print(f"\nNumber of outlier orders: {len(outliers)} out of {len(df)}")

# Calculate the correlation matrix
corr_matrix = df[numeric_cols].corr()

# Plot the Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
plt.title('Correlation Matrix of Numeric Variables')
plt.show()

plt.figure(figsize=(14, 5))

# 1. Total Revenue by Product
plt.subplot(1, 2, 1)
revenue_by_product = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)
sns.barplot(x=revenue_by_product.values, y=revenue_by_product.index, hue=revenue_by_product.index, palette='viridis', legend=False)
plt.title('Total Revenue by Product')
plt.xlabel('Total Revenue ($)')

# 2. Count of Orders by OrderStatus
plt.subplot(1, 2, 2)
sns.countplot(data=df, y='OrderStatus', hue='OrderStatus', palette='magma', order=df['OrderStatus'].value_counts().index, legend=False)
plt.title('Order Status Breakdown')
plt.xlabel('Number of Orders')

plt.tight_layout()
plt.show()

# Save the Distribution Chart
plt.savefig("distribution_chart.png", bbox_inches='tight', dpi=300)

# Save the Correlation Heatmap
plt.savefig("correlation_chart.png", bbox_inches='tight', dpi=300)

# Save the Categorical Trends Chart
plt.savefig("categorical_chart.png", bbox_inches='tight', dpi=300)


from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
import pandas as pd
import numpy as np
import os

# --- 1. Load Data & Calculate Stats ---
df = pd.read_excel("ecommerce-orders-clean dataset.xlsx", sheet_name="Sheet1")
numeric_cols = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']
stats = df[numeric_cols].describe().T[['mean', '50%', 'max']].round(2)

Q1 = df['TotalPrice'].quantile(0.25)
Q3 = df['TotalPrice'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + (1.5 * IQR)
outliers = len(df[df['TotalPrice'] > upper_bound])

# --- 2. Ensure Images Exist (Safety Check) ---
images = ["distribution_chart.png", "correlation_chart.png", "categorical_chart.png"]
for img in images:
    if not os.path.exists(img):
        print(f"❌ ERROR: {img} not found! Please run the matplotlib savefig() code first.")
        exit()

# --- 3. Setup PDF Document ---
PDF_PATH = "Project2_EDA_Report_Fixed.pdf"
doc = SimpleDocTemplate(
    PDF_PATH, pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm,
    title="DecodeLabs Project 2 - EDA Report"
)

styles = getSampleStyleSheet()
title_style = styles["Title"]
heading_style = styles["Heading2"]
body_style = styles["BodyText"]

# Custom styles
insight_style = ParagraphStyle(name="Insight", parent=body_style, textColor=colors.darkred, fontName="Helvetica-Bold")
caption_style = ParagraphStyle(name="Caption", parent=body_style, fontSize=9, textColor=colors.grey, alignment=1) # Centered

story = []

# --- 4. Title & Problem Statement ---
story.append(Paragraph("Project 2: Exploratory Data Analysis", title_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>1. Problem Statement & Methodology</b>", heading_style))
story.append(Paragraph("The goal of this analysis is to interrogate the e-commerce dataset to uncover hidden patterns, trends, and outliers. We applied descriptive statistics, evaluated data distributions, and mapped correlations to translate raw numbers into business insights.", body_style))
story.append(Spacer(1, 0.5*cm))

# --- 5. Descriptive Statistics Table ---
story.append(Paragraph("<b>2. The Logic Skeleton (Five-Number Summary)</b>", heading_style))
story.append(Paragraph("By comparing the Mean to the Median (50%), we can determine the skewness of our data.", body_style))
story.append(Spacer(1, 0.2*cm))

stats_data = [["Metric", "Mean (Average)", "Median (50%)", "Max"]]
for index, row in stats.iterrows():
    stats_data.append([index, f"{row['mean']:,.2f}", f"{row['50%']:,.2f}", f"{row['max']:,.2f}"])

tbl = Table(stats_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1f4e79")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("ALIGN", (1,0), (1,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.white]),
]))
story.append(tbl)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Insight:</b> The <i>TotalPrice</i> Mean ($1,053.97) is significantly higher than the Median ($823.62). This confirms the data is heavily <b>Right-Skewed</b> due to high-value outliers.", insight_style))

# Start a new page for the first chart to give it room
story.append(PageBreak())

# --- 6. Distributions & Outliers ---
story.append(Paragraph("<b>3. Distributions & Outlier Detection</b>", heading_style))
story.append(Paragraph("The histogram confirms the right-skewed shape. Using the IQR method, we identified the 'Suspects' (Outliers).", body_style))
story.append(Spacer(1, 0.3*cm))

# Add Image 1 (Width 17cm, Height 7.5cm)
img1 = Image("distribution_chart.png", width=17*cm, height=7.5*cm)
story.append(img1)
story.append(Paragraph("Figure 1: Histogram and Boxplot of Total Price", caption_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(f"<b>Forensic Note:</b> Q1 = ${Q1:.2f}, Q3 = ${Q3:.2f}. Upper Bound = ${upper_bound:.2f}. We found <b>{outliers} outlier orders</b> exceeding ${upper_bound:.2f}. These are likely VIP or wholesale purchases, not errors.", insight_style))

story.append(PageBreak())

# --- 7. Correlation Analysis ---
story.append(Paragraph("<b>4. Mapping Relationships (Correlation)</b>", heading_style))
story.append(Paragraph("We used the Pearson Correlation Coefficient to measure the strength of linear relationships. Notice the strong positive correlation (dark red) between UnitPrice and TotalPrice.", body_style))
story.append(Spacer(1, 0.3*cm))

# Add Image 2 (Width 14cm, Height 11cm to keep it square-ish)
img2 = Image("correlation_chart.png", width=14*cm, height=11*cm)
story.append(img2)
story.append(Paragraph("Figure 2: Correlation Heatmap", caption_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Insight:</b> <i>UnitPrice</i> and <i>TotalPrice</i> have a strong positive correlation (0.72). <i>Quantity</i> and <i>ItemsInCart</i> are also heavily correlated (0.65).", insight_style))

story.append(PageBreak())

# --- 8. Categorical Trends ---
story.append(Paragraph("<b>5. Categorical Trends & Business Impact</b>", heading_style))
story.append(Paragraph("Analyzing revenue by product and the status of orders to identify operational risks.", body_style))
story.append(Spacer(1, 0.3*cm))

# Add Image 3 (Width 17cm, Height 7.5cm)
img3 = Image("categorical_chart.png", width=17*cm, height=7.5*cm)
story.append(img3)
story.append(Paragraph("Figure 3: Revenue by Product and Order Status", caption_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Insight:</b> 'Chair' and 'Printer' are our top revenue drivers. However, 'Cancelled' and 'Returned' orders are extremely high (nearly 50% combined). This is a major revenue leak that needs immediate investigation.", insight_style))
story.append(Spacer(1, 0.5*cm))

# --- 9. The Verdict ---
story.append(Paragraph("<b>6. The Verdict (Recommendations)</b>", heading_style))
recommendations = [
    "1. <b>VIP Tracking:</b> Since we have a right-skewed distribution with outliers, create a VIP program to retain the customers making bulk purchases.",
    "2. <b>Operational Audit:</b> With such a high volume of Cancelled/Returned items, investigate the supply chain (e.g., are Chairs arriving damaged?).",
    "3. <b>Pricing Strategy:</b> Because UnitPrice drives TotalPrice more than Quantity does, focus marketing on higher-tier products rather than pushing for bulk volume."
]
for rec in recommendations:
    story.append(Paragraph(rec, body_style))
    story.append(Spacer(1, 0.2*cm))

# --- Build PDF ---
doc.build(story)
print(f"✅ EDA PDF report successfully saved to: {PDF_PATH}")

