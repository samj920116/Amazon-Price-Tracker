import pandas as pd
from pathlib import Path
import datetime as dt
import csv
class CSVManager:
    def __init__(self):
        self.min_price = 0

        self.file = Path("price_history.csv")
        self.csv_file_check()


    def csv_file_check(self):
        # Checking if csv file exist.
        default_columns = ["Product", "Price", "Date"]
        if not self.file.exists():
            empty_df = pd.DataFrame(columns=default_columns)
            empty_df.to_csv(self.file, index=False)

    def get_min_price(self) -> float:
        try:
            data = pd.read_csv(self.file)
        except FileNotFoundError:
            print("No price_history.csv found.")
        else:
            try:
                idx_min = data['Price'].idxmin()
            except ValueError:
                print("price_history.csv file empty.")
            else:
                self.min_price = float(data.iloc[idx_min].Price)
        return self.min_price

    def update_min_price(self,name:str,price:float):
        date = dt.datetime.now()
        date = date.strftime("%d/%m/%Y")
        try:
            with open(self.file, "a",encoding="utf-8",newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name,price,date])

        except FileNotFoundError:
            print("No price_history.csv found.")