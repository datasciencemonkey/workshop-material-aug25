# Ferguson Databricks Workshop - Data Engineering & AI/ML

A comprehensive Databricks project demonstrating data engineering, AI analytics, and MLflow integration for Ferguson Enterprises' product and sales data processing.

## Overview

This project showcases modern data engineering and AI/ML capabilities using Databricks, including:
- Automated data pipeline for product catalog processing
- Sales data generation and analysis
- AI-powered business intelligence using Databricks AI functions
- MLflow experiment tracking and model management
- Document parsing and contract intelligence

## Features

### Data Engineering
- **Product Data Processing**: Automated ETL pipeline for product catalog data
- **Sales Data Generation**: Synthetic sales data creation (Jan 2023 - July 2025)
- **Delta Lake Integration**: CDC-enabled Delta tables for real-time data processing
- **Serverless Spark**: Efficient distributed computing using Databricks Connect

### AI & Analytics
- **Contract Intelligence**: Automated extraction of structured terms from supplier agreements
- **CRM Analytics**: Parse and analyze contractor call logs
- **Personalization Engine**: Generate targeted communications with multi-language support
- **Revenue Forecasting**: AI-powered sales predictions
- **Compliance Masking**: Role-based data access with automatic PII masking
- **Document Intelligence**: PDF parsing for contracts and installation guides

### MLflow Integration
- **Experiment Tracking**: Comprehensive logging of model experiments
- **Model Tracing**: End-to-end traceability for AI model calls
- **Foundation Models**: Integration with Databricks Foundation Models
- **Custom Scorers**: Evaluation metrics for model performance

## Prerequisites

- Python 3.12+
- Databricks workspace with serverless compute enabled
- Databricks CLI configured with authentication
- Access to Databricks catalog and schema

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd workshop_code
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file with:
```env
DATABRICKS_CATALOG='main'
DATABRICKS_SCHEMA='your_schema'
DATABRICKS_TOKEN='your_token'
DATABRICKS_HOST='https://your-workspace.azuredatabricks.net'
MLFLOW_EXPERIMENT_ID='your_experiment_id'
```

## Usage

### 1. Data Pipeline Execution

Process product data and generate sales records:
```bash
cd src
python 01-upload.py
```

This will:
- Load and transform product catalog data
- Generate unique product IDs
- Create monthly sales data for 2023-2025
- Upload to Databricks Delta tables

### 2. AI Analytics (SQL)

Execute AI-powered queries in Databricks SQL interface:
```sql
-- Run queries from src/02-batch-inference.sql
USE CATALOG main;
USE SCHEMA your_schema;

-- Example: Extract contract terms
SELECT ai_query(...);
```

### 3. MLflow Tracing

Run MLflow experiments:
```bash
cd src/mlflow3_basics
python 01-trace-app.py  # Basic tracing
python 02-register-scorer-and-start.py  # Custom scorers
python 03-add-context.py  # Context enrichment
```

## Project Structure

```
workshop_code/
├── data/
│   ├── products_synthetic.csv         # Source product catalog
│   ├── products_synthetic_data.csv    # Processed product data
│   ├── products_sales_data.csv        # Generated sales data
│   ├── product_install_docs/          # Installation guides
│   └── *.pdf                          # Contract documents
├── src/
│   ├── 01-upload.py                   # Main data pipeline
│   ├── 02-batch-inference.sql         # AI analytics queries
│   └── mlflow3_basics/                # MLflow examples
│       ├── 01-trace-app.py
│       ├── 02-register-scorer-and-start.py
│       └── 03-add-context.py
├── databricks.yml                     # Databricks bundle config
├── requirements.txt                   # Python dependencies
├── CLAUDE.md                         # AI assistant guidance
└── README.md                         # This file
```

## Data Schema

### Products Table
- **Table**: `{catalog}.{schema}.products_synthetic_data`
- **Key Fields**: 
  - `product_id`: UUID identifier
  - `product_name`: Product name
  - `product_details`: Combined description
  - All fields stored as strings for Spark compatibility

### Sales Table
- **Table**: `{catalog}.{schema}.products_sales_data`
- **Key Fields**:
  - `product_id`: Links to product table
  - `year`, `month`, `date`: Time dimensions
  - `units_sold`: Monthly units (50-500 range)
  - `price_per_unit`: Price ($10-$200 range)
  - `sales_dollars`: Total revenue

## Key Technologies

- **Databricks Connect**: Serverless Spark execution
- **Delta Lake**: ACID transactions with CDC
- **MLflow**: Experiment tracking and model management
- **Databricks AI Functions**: Built-in AI capabilities
- **LangChain**: LLM application framework
- **OpenAI Integration**: Foundation model APIs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is part of the Ferguson Databricks Workshop and is intended for educational and demonstration purposes.

## Support

For questions or issues:
- Check the [CLAUDE.md](CLAUDE.md) file for technical details
- Review the inline documentation in source files
- Contact the workshop administrators

## Acknowledgments

- Ferguson Enterprises for the business use cases
- Databricks for the platform and AI capabilities
- The open-source community for the amazing tools and libraries