import pandas as pd
from sqlalchemy import create_engine
import getpass

password = getpass.getpass("Enter your Postgres password: ")
engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/supply_chain_db")

query = '''
SELECT 
	"Shipping Mode",
	AVG("Days for shipment (scheduled)") AS avg_scheduled_days,
	AVG("Days for shipping (real)") AS avg_real_days,
	ROUND(AVG("Days for shipping (real)") - AVG("Days for shipment (scheduled)"), 2) AS avg_days_over
FROM orders
GROUP BY "Shipping Mode"
ORDER BY avg_days_over DESC;
'''

df = pd.read_sql(query, engine)
print(df.to_markdown(index=False))