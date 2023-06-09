from bs4 import  BeautifulSoup
import requests


url0 = """https://aliexpress.ru/wholesale?SearchText=bike+lights"""
url = """https://aliexpress.ru/wholesale"""


responce = requests.get(url, params={"SearchText": ["bike", "lights"]})

print(responce.url)
print(responce)
print(responce.text)
