# Power BI Dashboard — Retail Sales Analytics

This folder documents how to build the Power BI dashboard from the star-schema
CSVs in `../data`. The CSVs are already Power BI–ready (one fact table + four
dimensions), so the model is a clean star schema.

> A binary `.pbix` can't be produced on Linux/CI, so this guide + the ready CSVs
> let you assemble the report in ~5 minutes in Power BI Desktop.

## 1. Import the data
1. Open **Power BI Desktop → Home → Get data → Text/CSV**.
2. Import all five files from `projects/retail-sales-analytics/data/`:
   `fact_sales.csv`, `dim_date.csv`, `dim_product.csv`, `dim_store.csv`, `dim_customer.csv`.
3. In **Transform data**, set types: `revenue/profit/cost/discount` → Decimal,
   `date` → Date, keys → Whole number. Close & Apply.

## 2. Model relationships (Model view)
Create these one-to-many relationships (dim → fact), single direction:

| From (dim)                 | To (fact)              |
|----------------------------|------------------------|
| `dim_date[date_key]`       | `fact_sales[date_key]` |
| `dim_product[product_id]`  | `fact_sales[product_id]` |
| `dim_store[store_id]`      | `fact_sales[store_id]` |
| `dim_customer[customer_id]`| `fact_sales[customer_id]` |

Mark `dim_date` as a **Date table** (Table tools → Mark as date table → `date`).

## 3. DAX measures
Create a `_Measures` table (Home → Enter data, blank) and add:

```DAX
Total Revenue = SUM ( fact_sales[revenue] )

Total Profit = SUM ( fact_sales[profit] )

Profit Margin % = DIVIDE ( [Total Profit], [Total Revenue] )

Order Count = DISTINCTCOUNT ( fact_sales[order_id] )

Avg Order Value = DIVIDE ( [Total Revenue], [Order Count] )

Revenue LY =
CALCULATE ( [Total Revenue], SAMEPERIODLASTYEAR ( dim_date[date] ) )

Revenue YoY % =
DIVIDE ( [Total Revenue] - [Revenue LY], [Revenue LY] )

Revenue MTD = TOTALMTD ( [Total Revenue], dim_date[date] )
```

## 4. Report layout (one page)
- **KPI cards** (top row): `Total Revenue`, `Total Profit`, `Profit Margin %`, `Avg Order Value`.
- **Line chart**: `Total Revenue` by `dim_date[date]` (month) with `Revenue LY` overlay.
- **Clustered bar**: `Total Revenue` by `dim_product[category]`.
- **Map / bar**: `Total Revenue` by `dim_store[region]`.
- **Matrix**: rows `dim_customer[segment]`, values `Total Revenue`, `Profit Margin %`.
- **Slicers**: `dim_date[year]`, `dim_store[region]`, `dim_product[category]`.

## 5. Suggested insights to call out
- Electronics drives the largest revenue share; Clothing/Beauty carry the highest margins.
- Clear Q4 (Nov–Dec) seasonal peak — visible in the YoY line chart.
- West region over-indexes on revenue vs East.
