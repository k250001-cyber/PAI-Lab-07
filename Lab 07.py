import pandas as pd
import numpy as np

np.random.seed(42)
n_rows = 150
data = {
    'Customer_ID': [f'CUST_{1000 + i}' if i % 12 != 0 else np.nan for i in range(n_rows)],
    'Join_Date': pd.date_range(start='2023-01-01', periods=n_rows, freq='2D'),
    'Age': [np.random.randint(18, 65) if i % 7 != 0 else np.nan for i in range(n_rows)],
    'Gender': np.random.choice(['Male', 'Female', 'Other'], size=n_rows, p=[0.48, 0.48, 0.04]),
    'City': np.random.choice(['Karachi', 'Lahore', 'Islamabad', 'Peshawar'], size=n_rows),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], size=n_rows),
    'Order_Count': np.random.randint(1, 30, size=n_rows),
    'Total_Spent': [round(np.random.uniform(500, 50000), 2) if i % 9 != 0 else np.nan for i in range(n_rows)],
    'Is_VIP': np.random.choice([True, False], size=n_rows, p=[0.2, 0.8])
}
df = pd.DataFrame(data)

print(df.shape)
print(df.dtypes)
print(df.isna().sum())

df.dropna(subset=['Customer_ID'], inplace=True)

df['Age'] = df['Age'].fillna(df['Age'].median())
df['Total_Spent'] = df['Total_Spent'].fillna(df['Total_Spent'].mean())

df['Join_Date'] = pd.to_datetime(df['Join_Date'])
df['Join_Year'] = df['Join_Date'].dt.year
df['Join_Month'] = df['Join_Date'].dt.month_name()

df['Avg_Order_Value'] = df['Total_Spent'] / df['Order_Count']

df['High_Value_Customer'] = df['Avg_Order_Value'] > 2500

city_summary = df.groupby('City').agg(
    Total_Customers=('Customer_ID', 'count'),
    Avg_Total_Spent=('Total_Spent', 'mean'),
    Max_Order_Count=('Order_Count', 'max')
)
print(city_summary)

pivot = pd.pivot_table(df, index='Category', columns='Is_VIP', values='Total_Spent', aggfunc='sum')
print(pivot)

top5 = df[df['Category'].isin(['Electronics', 'Clothing'])].sort_values('Total_Spent', ascending=False).head(5)
print(top5)

vip_cities = df[(df['Is_VIP']) & (df['City'].isin(['Karachi', 'Lahore']))]
print(vip_cities.groupby('City')['Order_Count'].mean())

# Insight 1: Karachi has the highest average Total_Spent (27379.05) against 21828.03 for Peshawar, while Lahore has the most customers (41).
# Insight 2: Books has the highest total revenue (about 1003474) with Electronics close behind (about 997357); Home is lowest (about 614022).
# Insight 3: VIP customers do not spend more than non-VIP customers: average Total_Spent is 24797.65 for VIP and 24839.40 for non-VIP, and average Avg_Order_Value is 2184.37 for VIP against 2935.69 for non-VIP.