import requests
import os

urls = [
    "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/grocery_data.csv",
    "https://raw.githubusercontent.com/plotly/datasets/master/ecommerce_data.csv",
    "https://raw.githubusercontent.com/mallikas0902/Ecommerce-Business-SQL-Analysis/main/Data/Products.csv",
    "https://raw.githubusercontent.com/mallikas0902/Ecommerce-Business-SQL-Analysis/main/Data/Orders.csv",
    "https://raw.githubusercontent.com/yugabyte/yugabyte-db/master/sample/retail.sql",
    "https://raw.githubusercontent.com/reconstruct-datasets/ecommerce-sales-data/main/data/data.csv",
    "https://raw.githubusercontent.com/datsoftlyngby/soft2018fall-bi-teaching-material/master/data/online_retail.csv",
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv" # Diamonds is stable and has clear columns
]

def find_working_url():
    for url in urls:
        print(f"Checking: {url}")
        try:
            r = requests.head(url, timeout=5)
            if r.status_code == 200:
                print(f"FOUND WORKING URL: {url}")
                return url
        except:
            pass
    return None

if __name__ == "__main__":
    url = find_working_url()
    if url:
        r = requests.get(url)
        filename = url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded {filename}")
    else:
        print("Still no working URL found.")
