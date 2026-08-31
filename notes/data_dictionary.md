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
'''sql
-- List all columns and types
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;
'''

EOF