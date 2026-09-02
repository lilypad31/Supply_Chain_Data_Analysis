import pandas as pd
from sqlalchemy import create_engine
import getpass

password = getpass.getpass("Enter your Postgres password: ")
engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/supply_chain_db")

query = '''
SELECT
	"Late_delivery_risk",
	"Delivery Status",
	COUNT(*) AS order_count
FROM orders
GROUP BY "Late_delivery_risk", "Delivery Status"
ORDER BY "Late_delivery_risk", "Delivery Status";
'''

df = pd.read_sql(query, engine)
print(df.to_markdown(index=False))