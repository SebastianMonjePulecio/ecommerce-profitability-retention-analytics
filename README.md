# E-commerce Profitability and Retention Analytics

This project was built as a portfolio case around a very common business problem in e-commerce: sales keep moving, but profitability does not improve at the same pace. The goal is not just to report revenue, but to understand what is happening underneath the surface and where the business is losing efficiency.

## Business context

The scenario is simple and realistic. An e-commerce company is growing, but commercial leaders are starting to worry about margin pressure, high return rates, and too much dependence on discounts. Some channels bring volume but not enough profit. Some categories sell well but come with expensive returns. At the same time, not every acquired customer becomes a repeat buyer.

This project is framed the way a Senior Data Analyst would approach it: starting from the business problem, translating it into measurable questions, and ending with recommendations the company could actually act on.

## Business questions

1. Which customer segments create the most value over time, and which ones are most likely to stop buying?
2. Which channels and product categories help revenue grow, but hurt profitability?
3. What actions could improve retention, reduce waste, and increase net revenue?

## Tech stack

- `SQL` for KPI calculation and business queries
- `Python` for data generation, cleaning, exploratory analysis, and RFM segmentation
- `Power BI` or `Tableau` for dashboarding and stakeholder storytelling

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

After running the scripts, the project generates:

- cleaned transaction-level data in `data/processed`
- KPI summary tables in `outputs/tables`
- business charts in `outputs/charts`
- an RFM segmentation file ready to be consumed in a dashboard

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

This analysis supports decisions such as:

- reallocating spend toward channels with stronger profit contribution
- reducing aggressive discounting where it is not really needed
- prioritizing retention actions for high-value customers at risk of churn
- reviewing product categories with unusually high return behavior

## Why this works well in a portfolio

This is the kind of project that helps in interviews because it shows more than tools. It shows business judgment, prioritization, and the ability to connect data to decisions that affect revenue, margin, and efficiency.
