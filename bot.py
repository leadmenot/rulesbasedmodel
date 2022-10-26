import time
start_time = time.time()

import requests, webbrowser
from bs4 import BeautifulSoup
import gspread
import numpy as np

def fetchSheet(sa):
    sheet = sa.open("LeadMeNot Reactive Rules") 
    worksheet = sheet.worksheet("name of sheet to be scanned")
    worksheet1 = sheet.worksheet("name  if sheet to be copied into")
    rawInfo = worksheet.get_all_values()
    return rawInfo[1:], worksheet, worksheet1

sa = gspread.service_account()
info = ""
list, worksheet, worksheet1 = fetchSheet(sa);
filteredList = []
print("Original List", list)
input = ""
for name in list:
    info=""
    input = name[0]
    googleSearch = requests.get("https://www.google.com/search?q="+input)

    soup = BeautifulSoup(googleSearch.text, "html.parser")
    searchResults = soup.find_all("span");

    for text in searchResults:
        info += text.get_text().lower();
    matches = ["porn", "fuck", "xxx", "sex"]

    if any(x in info for x in matches):
        filteredList.append(name);
        print(name)
print("\n\nFiltered List", filteredList)
filteredList = np.array(filteredList)
worksheet1.update('A2', filteredList.tolist())

print("Process finished --- %s seconds ---" % (time.time() - start_time))
