import pandas as pd
from sqlalchemy import create_engine
import getpass

username = "postgres"
password = getpass.getpass("Enter your Postgres password: ")
host = "localhost"
port = "5432"
database = "supply_chain_db"

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")

df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding="latin1")

print("Rows, columns:", df.shape)
print(df.head())

df.to_sql("orders", engine, if_exists="replace", index=False)

print("Data loaded into 'orders' table successfully.")
