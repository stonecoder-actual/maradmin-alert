from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3707403/fy24-approved-selections-to-gunnery-sergeant/"
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.text, "html.parser")
bodyText = (soup.select('div', class_='body-text'))
print(bodyText)