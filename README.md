# E-commerce Profitability and Retention Analytics

End-to-end portfolio project focused on a real business problem in e-commerce: sales are growing, but net profitability and customer retention are under pressure due to inefficient campaigns, excessive discounts, and high return rates.

## Business context

An e-commerce company sees steady top-line growth, but commercial leaders are concerned that revenue growth is not converting into healthy margin expansion. The business suspects that some customer segments, acquisition channels, and product categories generate sales volume while eroding profitability.

This project is designed to answer the type of questions a Senior Data Analyst would solve for a commercial, growth, or category management team.

## Business questions

1. Which customer segments generate the highest long-term value and which ones are at risk of churn?
2. Which channels and categories drive revenue but underperform on gross margin and return rate?
3. What levers could improve retention and profitability in a measurable way?

## Tech stack

- `SQL` for business queries and KPI aggregation
- `Python` for synthetic data generation, data cleaning, EDA, and RFM segmentation
- `Power BI` or `Tableau` for executive dashboards using the exported CSV outputs

## Project structure

```text
.
|-- data
|   |-- processed
|   `-- raw
|-- outputs
|   |-- charts
|   `-- tables
|-- sql
|   |-- business_queries.sql
|   `-- schema.sql
|-- src
|   |-- analyze_ecommerce.py
|   `-- generate_sample_data.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## How to run

1. Create a virtual environment.
2. Install dependencies.
3. Generate the synthetic dataset.
4. Run the analysis script.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_ecommerce.py
```

## Outputs

After execution, the project generates:

- cleaned transaction-level data in `data/processed`
- KPI summary tables in `outputs/tables`
- executive-ready charts in `outputs/charts`
- an RFM segmentation file for downstream dashboarding

## Key KPIs included

- net revenue
- gross profit
- gross margin percentage
- average order value
- repeat purchase rate
- return rate
- discount intensity
- marketing ROAS by channel

## Strategic value

The resulting analysis supports decisions such as:

- reallocating spend toward channels with stronger net margin
- reducing over-discounting in low-elasticity segments
- prioritizing retention campaigns for high-value at-risk customers
- intervening in product categories with abnormal return behavior

## Portfolio angle

This repository is intentionally designed to showcase:

- business framing, not just technical execution
- quantifiable recommendations connected to revenue and efficiency
- clean deliverables that can be reused in interviews, GitHub, and dashboards

