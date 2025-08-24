#%%
from databricks.connect import DatabricksSession
import pandas as pd
from dotenv import load_dotenv
import os
import uuid
load_dotenv()

catalog = os.getenv("DATABRICKS_CATALOG")
schema = os.getenv("DATABRICKS_SCHEMA")

#%%
df = pd.read_csv("../data/products_synthetic.csv")
# convert all column names to acceptable format for spark and lowercase
df.columns = [col.replace(" ", "_").lower() for col in df.columns]
# convert all column types to appropriate spark types
df = df.astype({col: "string" for col in df.columns})
df.head()

#%%

# Add a fake product ID column that is a random UUID.
df['product_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
#  Now make a new column called Product Detail and combine product name, short description and longer description and introduce a new line between the product name and the short description and long description
df['product_details'] = df['product_name'] + "\n" + df['short_description'] + "\n" + df['longer_description']+ "\n" + df['product_id']
df.to_csv("../data/products_synthetic_data.csv", index=False)

#%%
# For each of the products create a year to snapshot of sales data by month for every month in the year 2023,2024 & 2025
import random

# Generate sales data for each product
sales_data = []

for product_id in df['product_id']:
    # Full years 2023 and 2024
    for year in [2023, 2024]:
        for month in range(1, 13):
            # Generate random sales units between 50 and 500
            units_sold = random.randint(50, 500)
            # Generate random price per unit between $10 and $200
            price_per_unit = round(random.uniform(10, 200), 2)
            # Calculate total sales in dollars
            sales_dollars = round(units_sold * price_per_unit, 2)
            
            sales_data.append({
                'product_id': product_id,
                'year': year,
                'month': month,
                'date': f"{year}-{month:02d}-01",
                'units_sold': units_sold,
                'price_per_unit': price_per_unit,
                'sales_dollars': sales_dollars
            })
    
    # 2025 - only up to July
    for month in range(1, 8):
        # Generate random sales units between 50 and 500
        units_sold = random.randint(50, 500)
        # Generate random price per unit between $10 and $200
        price_per_unit = round(random.uniform(10, 200), 2)
        # Calculate total sales in dollars
        sales_dollars = round(units_sold * price_per_unit, 2)
        
        sales_data.append({
            'product_id': product_id,
            'year': 2025,
            'month': month,
            'date': f"2025-{month:02d}-01",
            'units_sold': units_sold,
            'price_per_unit': price_per_unit,
            'sales_dollars': sales_dollars
        })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)
# Convert all columns to string for Spark compatibility
sales_df = sales_df.astype({col: "string" for col in sales_df.columns})
sales_df = sales_df.merge(df[['product_id', 'product_name']], on='product_id', how='left')
sales_df.to_csv("../data/products_sales_data.csv", index=False)
print(f"Generated {len(sales_df)} sales records for {len(df)} products")
print(sales_df.head())

#%%
# Write this dataframe into Databricks using the schema in the .env file and the catalog in the .env file.
spark = DatabricksSession.builder.profile("DEFAULT").remote(serverless=True).getOrCreate()
spdf = spark.createDataFrame(df)
spark.sql(f"drop table if exists {catalog}.{schema}.products_synthetic_data")
spdf.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.{schema}.products_synthetic_data")

#%%
spark.sql(
    f"ALTER TABLE {catalog}.{schema}.products_synthetic_data SET TBLPROPERTIES (delta.enableChangeDataFeed = true)"
)

#%%
# Upload sales data to Databricks
sales_spdf = spark.createDataFrame(sales_df)
spark.sql(f"drop table if exists {catalog}.{schema}.products_sales_data")
sales_spdf.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.{schema}.products_sales_data")
spark.sql(
    f"ALTER TABLE {catalog}.{schema}.products_sales_data SET TBLPROPERTIES (delta.enableChangeDataFeed = true)"
)
print(f"Uploaded {len(sales_df)} sales records to {catalog}.{schema}.products_sales_data")

