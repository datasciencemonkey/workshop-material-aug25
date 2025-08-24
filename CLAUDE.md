# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Databricks data engineering and AI/ML project for Ferguson Enterprises that processes product data, performs AI-driven analytics, and implements MLflow tracing. The project uses Databricks Connect for serverless Spark execution, integrates with Databricks AI functions for business intelligence, and leverages MLflow for experiment tracking and model management.

## Key Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Run data upload pipeline
cd src
python 01-upload.py

# Run MLflow tracing examples
cd src/mlflow3_basics
python 01-trace-app.py
python 02-register-scorer-and-start.py
python 03-add-context.py
```

## Architecture

### Data Pipeline (`src/01-upload.py`)
Processes product catalog and generates sales data:
1. Reads `data/products_synthetic.csv` using pandas
2. Normalizes column names (lowercase, underscores for spaces)
3. Creates `product_details` field combining name + descriptions + product_id
4. Generates UUID `product_id` for each product
5. Creates monthly sales data for Jan 2023 - July 2025 with:
   - Random units sold (50-500 per month)
   - Random price per unit ($10-$200)
   - Calculated sales dollars
6. Saves processed data to CSV files
7. Uploads both product and sales data to Databricks Delta tables with CDC enabled

### AI Analytics (`src/02-batch-inference.sql`)
SQL-based AI operations for Ferguson business use cases:
- **Contract Intelligence**: Extract structured terms from supplier agreements using `ai_query`
- **CRM Log Processing**: Parse contractor call logs with `ai_extract`
- **Personalization**: Generate contractor-specific emails with `ai_gen` and `ai_translate`
- **Forecasting**: Revenue predictions using `ai_forecast`
- **Data Masking**: Compliance masking with `ai_mask` based on user groups
- **Document Parsing**: PDF contract analysis with `ai_parse_document`

### MLflow Integration (`src/mlflow3_basics/`)
Implements MLflow tracing and experiment tracking:
- **01-trace-app.py**: Basic OpenAI/Databricks Foundation Model tracing with auto-logging
- **02-register-scorer-and-start.py**: Custom scorer registration and evaluation
- **03-add-context.py**: Adding context to traces for better observability
- Uses Databricks Foundation Models (databricks-gpt-oss-120b)
- Tracks experiments using MLflow experiment ID from environment

### Configuration

**Environment Variables** (`.env`):
- `DATABRICKS_CATALOG`: Target catalog for Delta tables (main)
- `DATABRICKS_SCHEMA`: Target schema for Delta tables (sgfs)
- `DATABRICKS_TOKEN`: Databricks API token for authentication
- `DATABRICKS_HOST`: Databricks workspace URL
- `MLFLOW_EXPERIMENT_ID`: MLflow experiment ID for tracking

**Databricks Bundle** (`databricks.yml`):
- Bundle name: `workshop_code`
- Default target: `dev` mode
- Workspace: Azure Databricks instance
- Profile: Uses "DEFAULT" for authentication

### Data Sources

**Product Data:**
- `data/products_synthetic.csv`: Product catalog with name, descriptions
- `data/products_synthetic_data.csv`: Enhanced product data with details and IDs
- `data/products_sales_data.csv`: Monthly sales data (2023-2025)

**Documentation:**
- `data/Corporate_2023_Ferguson_supplier_tnc_2023.pdf`: Supplier terms
- `data/product_install_docs/`: Product installation guides (various PDFs)
- `data/custom_embedding_models.png`: Model architecture diagram

### Table Structure

**Product Table**: `{catalog}.{schema}.products_synthetic_data`
- All columns stored as string type for Spark compatibility
- Includes original product fields plus `product_details` and `product_id`
- Change Data Feed enabled for CDC operations

**Sales Table**: `{catalog}.{schema}.products_sales_data`
- Monthly sales records from Jan 2023 to July 2025
- Columns: product_id, year, month, date, units_sold, price_per_unit, sales_dollars, product_name
- All columns as string type with CDC enabled

## Dependencies

Key libraries include:
- `databricks-connect==17.1.1`: Serverless Spark execution
- `databricks-agents==1.4.0`: AI agent framework
- `databricks-sdk==0.64.0`: Databricks API client
- `mlflow==3.3.1`: Experiment tracking and model management
- `langchain==0.3.27`: LLM application framework
- `openai==1.101.0`: OpenAI API client for Foundation Models
- `pandas==2.3.2`: Data manipulation
- Additional ML/AI libraries for vector search, embeddings, and tracing