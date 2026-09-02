# Data Dictionary & Notes

## Key columns
- **Delivery Status** (text): "Advance shipping", "Late delivery", "Shipping canceled", "Shipping on time"
- **Shipping Mode** (text): "First Class", "Same Day", "Second Class", "Standard Class"
- **Late_Delivery_risk** (bigint): pre-existing flag column; need to check if this duplicates my own late-delivery calculation or means something else
- **order date (DateOrders_** / **shipping date (DateOrders)**: stored as text, not real dates - will need to CAST or TO_DATE() before doing any date math

## Open questions
- For "Shipping on time", does that include or exclude "Advance shipping"?
- Need to check row counts per Delivery Status value to understand how common cancellations are

## Useful queries
```sql
-- List all columns and types
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;
```

## Reusable script: run a SQL query and print as Markdown table
Paste this into a .py file (or Terminal via python3) to quickly turn any query
result into a copy-pasteable Markdown table for these notes.

```python
import pandas as pd
from sqlalchemy import create_engine
import getpass

password = getpass.getpass("Enter your Postgres password: ")
engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/supply_chain_db")

query = '''
-- paste your SQL query here
'''

df = pd.read_sql(query, engine)
print(df.to_markdown(index=False))
```

## Findings so far

### Late delivery rate by Shipping Mode
|"Shipping Mode"	| "total_orders" |"late_orders"|"late_pct"|
|---|---|---|---|
| "First Class" | 27814 | 26513	| 95.32 |
| "Second Class" | 35216 | 26987 | 76.63 |
|"Same Day" | 9737 | 4454 | 45.74 |
|"Standard Class" | 107752 | 41023| 38.07 | 

**Surprising result:** First Class has the worst late rate, Standard Class has the best.
While initially appears counterintuitive, this is not likely due to literal speed, but rather First Class likely promises a tight delivery window, making it easy to miss; Standard Class probably promises a loose window, making it easy to hit.

**Next step to confirm:** compare "Days for shipping (real)" vs "Days for shipment (scheduled)" by Shipping Mode  to confirm tight-promise theory regarding First Class shipping.

### Real vs scheduled delivery days by Shipping Mode
| Shipping Mode   |   avg_scheduled_days |   avg_real_days |   avg_days_over |
|:----------------|---------------------:|----------------:|----------------:|
| Second Class    |                    2 |        3.99083  |            1.99 |
| First Class     |                    1 |        2        |            1    |
| Same Day        |                    0 |        0.478279 |            0.48 |
| Standard Class  |                    4 |        3.99591  |            0    |

**Key insight:** Actual delivery times are fairly similar across all shipping modes (roughly 2-4 days regardless of tier). Fulfillment doesn't get meaningfully faster just because a customer paid for a faster tier. Promised/scheduled shipping days do not reflect actual shipping times; this confirms the previous finding that late shipping reflects broken promises vs fulfillment capability, not actual speed differences between different tiers.

### Late_delivery_risk vs Delivery Status cross-check
|   Late_delivery_risk | Delivery Status   |   order_count |
|---------------------:|:------------------|--------------:|
|                    0 | Advance shipping  |         41592 |
|                    0 | Shipping canceled |          7754 |
|                    0 | Shipping on time  |         32196 |
|                    1 | Late delivery     |         98977 |

**Conclusion:** 'Late_delivery_risk' is not a separate signal; it's just a pre-computed 0/1 that communicates whether or not "Delivery Status = Late delivery" (N being 0, Y being 1). Not useful as an independent feature, but confirms that AVG("Late_delivery_risk") rather than a full CASE WHEN calculation is a reliable shortcut.

**README Headline number:** 98,977 of 180,519 total orders are late - about 54.8% overall.

**Resolved open question:** For "Shipping on time", does that include or exclude "Advance shipping"?
No, the Delivery Status cross-check shows 4 distinct, mutually exclusive values (Advance shipping, Shipping canceled, Shipping on time, Late delivery), each with its own separate count. They are separate categories, not overlapping.
Notably, Advance shipping has a higher order count than Shipping on time.