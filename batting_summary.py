import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

batting_summary = []
title_list = ["match","batsmanName","teamInings","out/not_out","runs","balls","Min","4s","6s","SR"]

url = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-cricket-world-cup-2023-24-15338"
request = requests.get(url)
soup = BeautifulSoup(request.text, "lxml")
# print(request)

score_card_links = []
table = soup.find("table")
rows = table.find_all("tr")

for row in rows:
    last_column = row.select_one("td:last-child span a")

    if last_column:
        href_value = last_column["href"]
        new_link = "https://www.espncricinfo.com/" + href_value
        score_card_links.append(new_link)

for i in score_card_links:
    url = i
    request = requests.get(url)
    soup_link = BeautifulSoup(request.text, "lxml")
    table = soup_link.find_all("table", class_="ci-scorecard-table")
    team_names = soup_link.find_all("span", class_="ds-text-title-xs ds-font-bold ds-capitalize")
    team1, team2 = team_names[0].text.strip(), team_names[1].text.strip()
    match_info = f'{team1} Vs {team2}'
    current_team = team1

    for i in table:
        rows = i.find_all("tr")
        for i in rows[1:]:
            data = i.find_all("td")
            row = [td.text.strip() for td in data]
            row.insert(1, current_team)

            if "Extras" in row[0]:
                current_team = team2
                break
            row.insert(0, match_info)

            if len(row) == len(title_list):
                batting_summary.append(row)

    batting_summary = [sublist for sublist in batting_summary if any(sublist)]

df = pd.DataFrame(batting_summary, columns=title_list)
print(df)

# df.to_csv("datasets/batting_summary.csv")


