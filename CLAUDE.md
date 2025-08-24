# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Databricks data engineering project for Ferguson Enterprises that processes product data and performs AI-driven analytics. Uses Databricks Connect for serverless Spark execution and integrates with Databricks AI functions for contract intelligence, data extraction, and forecasting.

## Key Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Run data upload pipeline
cd src
python 01-upload.py
```

## Architecture

### Data Pipeline (`src/01-upload.py`)
Processes product catalog data from CSV to Delta tables:
1. Reads `data/products_synthetic.csv` using pandas
2. Normalizes column names (lowercase, underscores for spaces)
3. Creates `product_details` field combining name + descriptions
4. Generates UUID `product_id` for each product
5. Saves processed data to `data/products_synthetic_data.csv`
6. Uploads to Databricks Delta table with Change Data Feed enabled

### AI Analytics (`src/02-batch-inference.sql`)
SQL-based AI operations for Ferguson business use cases:
- **Contract Intelligence**: Extract structured terms from supplier agreements using `ai_query`
- **CRM Log Processing**: Parse contractor call logs with `ai_extract`
- **Personalization**: Generate contractor-specific emails with `ai_gen` and `ai_translate`
- **Forecasting**: Revenue predictions using `ai_forecast`
- **Data Masking**: Compliance masking with `ai_mask` based on user groups
- **Document Parsing**: PDF contract analysis with `ai_parse_document`

### Configuration

**Environment Variables** (`.env`):
- `DATABRICKS_CATALOG`: Target catalog for Delta tables
- `DATABRICKS_SCHEMA`: Target schema for Delta tables

**Databricks Bundle** (`databricks.yml`):
- Bundle name: `workshop_code`
- Default target: `dev` mode
- Workspace: Azure Databricks instance
- Profile: Uses "DEFAULT" for authentication

### Data Sources
- `data/products_synthetic.csv`: Product catalog with name, descriptions
- `data/Corporate_2023_Ferguson_supplier_tnc_2023.pdf`: Supplier terms for document parsing
- Generated output: `data/products_synthetic_data.csv` with enhanced product details

### Table Structure
Delta table: `{catalog}.{schema}.products_synthetic_data`
- All columns stored as string type for Spark compatibility
- Includes original product fields plus `product_details` and `product_id`
- Change Data Feed enabled for CDC operations