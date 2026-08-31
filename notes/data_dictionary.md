# Data Dictionary & Notes

## Key columns
- **Delivery Status** (text): "Advance shipping", "Late delivery", "Shipping canceled", "Shipping on time"
- **Shipping Mode** (text): "First Class", "Same Day", "Second Class", "Standard Class"
- **Late_Delivery_risk** (bigint): pre-existing flag column; need to check if this duplicates my own late-delivery calculation or means something else
- **order date (DateOrders_** / **shipping date (DateOrders)**: stored as TEXT, not real dates - will need to CAST or TO_DATE() before doing any date math

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

## Findings so far

### Late delivery rate by Shipping Mode
cat >> notes/data_dictionary.md << 'EOF'

## Findings so far

### Late delivery rate by Shipping Mode
"Shipping Mode"	"total_orders"	"late_orders"	"late_pct"
"First Class"	27814	26513	95.32
"Second Class"	35216	26987	76.63
"Same Day"	9737	4454	45.74
"Standard Class"	107752	41023	38.07

**Surprising result:** First Class has the worst late rate, Standard Class has the best
While initially appears counterintuitive, this is not likely due to literal speed, but rather First Class likely promises a tight delivery window, making it easy to miss; Standard Class probably promises a loose window, making it easy to hit.

**Next step to confirm:** compare "Days for shipping (real)" vs "Days for shipment (scheduled)" by Shipping Mode  to confirm tight-promise theory regarding First Class shipping.