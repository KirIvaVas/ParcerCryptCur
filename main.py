from bs4 import  BeautifulSoup
import requests
from re import compile, sub
import pandas as pd



url = "https://tradingeconomics.com/crypto"
currency = "BTC"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

responce = requests.get(url, headers=headers).text
soup = BeautifulSoup(responce, "html.parser")

btc_rates = soup.find_all("div", class_="panel panel-default")[1]
btc_table_header = btc_rates.find("thead").find_all(class_="te-sort")


columns_list = []
for count, h in zip(range(len(btc_table_header)), btc_table_header):
    if count == 0:
        regex = compile(f"{currency}")
        h = regex.findall(h.string)[0]
        columns_list.append(h)
    else:
        columns_list.append(h.string)


rows_pattern = compile(f"^datatable-row.*")
btc_table_body = btc_rates.find("tbody").find_all(class_=rows_pattern)


items_pattern = compile(f"^datatable-item")
values_list = []
for tag_row in btc_table_body:
    temp_values_list = []
    tag_row_items_list = tag_row.find_all(class_=items_pattern)
    for count, item in enumerate(tag_row_items_list):
        if count == 0:
            temp_values_list.append(item.a.b.string)
        elif count == 1:
            temp_values_list.append(sub(r"[^0-9]", '', item.string))
        elif count == (len(tag_row_items_list) - 1):
            temp_values_list.append(sub(r"[\s]", '', item.string))
        else:
            temp_values_list.append(item.get("data-value"))
    values_list.append(temp_values_list)


df = pd.DataFrame(values_list, columns=columns_list)
df_sorted = df.sort_values(by="Weekly")
df_sorted.to_csv("datatable.csv")


