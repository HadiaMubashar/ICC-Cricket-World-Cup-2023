import requests
import pandas as pd
from bs4 import BeautifulSoup

title_list = []
url = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-cricket-world-cup-2023-24-15338"
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")
print(request)

table = soup.find("table")
header = table.find_all("span", class_ = "ds-cursor-pointer")

for i in header:
    title = i.text
    title_list.append(title)
print(title_list)

df = pd.DataFrame(columns = title_list)

rows = soup.find_all("tr")
for i in rows[1:]:
    data = i.find_all("td", class_ = "ds-min-w-max")
    row = [td.text for td in data]
    l = len(df)
    df.loc[l] = row

print(df)

# df.to_csv("datasets/match_results.csv")
