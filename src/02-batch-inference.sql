USE CATALOG main;
USE SCHEMA sgfs;

-- Contract Intelligence 📑
-- Ferguson manages supplier agreements (pipes, fixtures, HVAC systems). Extract structured contract terms automatically.


SELECT ai_query(
    "databricks-gpt-oss-20b",
    "Extract contract key terms: Effective date, parties, renewal, payment terms, and purchase obligations.

    SUPPLY AGREEMENT
    Effective as of May 1, 2025, between Ferguson Enterprises, Inc. (Supplier) with offices in Newport News, VA,
    and ABC Mechanical Contractors, Chicago, IL (Purchaser). Initial Term: 24 months, auto-renews annually unless 90-day notice is given.
    Either party may terminate with 30-day written notice for cause. Purchaser minimum annual purchase: $3,000,000.
    Late payments beyond 15 days of invoice allow termination by Supplier.
    Pricing may increase annually capped at 5% or CPI-U adjustment."
,
    responseFormat => '{
      "type": "json_schema",
      "json_schema": {
        "name": "ferguson_contract_terms",
        "schema": {
          "type": "object",
          "properties": {
            "supplier": {"type": "string"},
            "purchaser": {"type": "string"},
            "effective_date": {"type": "string"},
            "initial_term_months": {"type": "integer"},
            "renewal_terms": {"type": "string"},
            "termination_notice_days": {"type": "integer"},
            "payment_terms": {"type": "string"},
            "min_annual_purchase": {"type": "number"},
            "pricing_cap": {"type": "string"}
          }
        }
      }
    }'
) as contract_structured;


-- CRM Log Extraction 👩‍🔧
-- Extract structured insights from Ferguson contractor or distributor call logs.


SELECT ai_extract(
    'Order Status: Delivered on Aug 12, 2025. Contractor Jane Smith contacted Ferguson DC #4512 in Richmond, VA.
    She purchased 15 units of Moen stainless faucets (3 batches of 5). She inquired about warranty coverage.',
    array('person','location','distribution_center_id','product_category','brand','quantity','issue_summary','order_status')
) as result;


-- Personalization & Communication ✉️
-- Generate contractor‑specific email campaigns automatically — personalize, then translate if needed.

WITH extracted_data AS (
  SELECT ai_extract(
    'Contractor John Miller purchased 12 Rheem HVAC units on Aug 10, 2025 from Ferguson Nashville DC.',
    array('person','product_category','brand','quantity','location','date_ordered')
  ) AS extracted_json
)
SELECT
  ai_gen(
    'Write a warm sales follow‑up email to ' || extracted_json.person || 
    ' thanking them for ordering ' || extracted_json.quantity || ' ' || extracted_json.brand || ' ' || extracted_json.product_category || ' units on ' || extracted_json.date_ordered || 
    '. They are based in ' || extracted_json.location || 
    '. Highlight Ferguson’s Fall 10% HVAC contractor discount and prompt them to contact their account rep.'
  ) as personalized_email_in_english,
  ai_translate(personalized_email_in_english, 'es') as personalized_email_in_spanish
FROM extracted_data;


-- Forecasting Revenue 📈
-- Rapidly forecast daily Ferguson sales without standing up a dedicated ML pipeline.

-- Generate mock Ferguson B2B sales data
CREATE OR REPLACE VIEW sales_data AS
SELECT
  DATE_ADD(DATE'2025-01-01', (n - 1)) AS sales_date,
  100000 + 2000 * SIN(n / 14.0) + (RAND() * 5000) AS revenue
FROM
  (SELECT EXPLODE(SEQUENCE(1, 120)) AS n) t;

select min(sales_date), max(sales_date),max(sales_date)-min(sales_date) days_of_data from sales_data;
-- Forecast forward 30 days
SELECT * FROM ai_forecast(
  TABLE(sales_data),
  horizon => '2025-06-01',
  time_col => 'sales_date',
  value_col => 'revenue'
);


-- Data Masking 🔒
-- Mask tax IDs and contact info in Ferguson ERP for compliance, only visible to authorized groups.

CREATE OR REPLACE VIEW partner_contacts AS
SELECT
  company_name,
  CASE 
    WHEN is_account_group_member('finance-core') THEN ein
    ELSE ai_mask(ein, array('TAX_ID'))
  END AS ein,
  industry,
  address,
  CASE 
    WHEN is_account_group_member('account users') THEN email -- i am a part of this group.
    ELSE ai_mask(email, array('EMAIL'))
  END AS email
FROM (
  VALUES
    ('Rheem Manufacturing', '12-3456789', 'HVAC', 'Atlanta, GA', 'contracts@rheem.com'),
    ('Moen Inc.', '98-7654321', 'Plumbing', 'Cleveland, OH', 'sales@moen.com')
) as t(company_name, ein, industry, address, email);

select * from partner_contacts;


-- Document Intelligence 📄
-- Parse Ferguson PDF terms (policies, contractor program guides, supplier catalogs).
-- https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_parse_document

WITH corpus AS (
  SELECT
    path,
    ai_parse_document(content) AS parsed
  FROM
    READ_FILES('/Volumes/main/sgfs/sg-vol/financial_results/Ferguson_FY25_Third_Quarter_Results_Presentation.pdf', format => 'binaryFile')
)
SELECT
  path,
  parsed:document AS document,
  parsed:document:pages AS pages,
  parsed:document:elements AS elements,
  parsed:metadata as metadata
FROM corpus;