from databricks.connect import DatabricksSession
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Databricks catalog and schema from environment
catalog = "main"
schema = "sgfs"
table_name = "starbucks_reviews"

# Initialize Databricks session
print("Connecting to Databricks...")
spark = DatabricksSession.builder.profile("DEFAULT").remote(serverless=True).getOrCreate()

# Read the table from Databricks
print(f"Reading table {catalog}.{schema}.{table_name}...")
df_spark = spark.sql(f"SELECT * FROM {catalog}.{schema}.{table_name}")

# Convert to Pandas DataFrame
print("Converting to Pandas DataFrame...")
df_pandas = df_spark.toPandas()

# Define output path
output_dir = "../../data"
output_file = os.path.join(output_dir, "starbucks_reviews.csv")

# Ensure the data directory exists
os.makedirs(output_dir, exist_ok=True)

# Save to CSV
print(f"Saving to {output_file}...")
df_pandas.to_csv(output_file, index=False)

print(f"Successfully downloaded {len(df_pandas)} rows from {catalog}.{schema}.{table_name}")
print(f"Data saved to: {output_file}")

# Show sample of the data
print("\nFirst 5 rows of the data:")
print(df_pandas.head())

# Show basic statistics
print(f"\nData shape: {df_pandas.shape}")
print(f"Columns: {list(df_pandas.columns)}")

