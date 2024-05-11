import requests
import csv

url = "https://coronavirus-smartable.p.rapidapi.com/stats/v1/global/"
headers = {
    "X-RapidAPI-Key": "27ec836ab2msh3bc908074200bafp1320d5jsnbf6a9ab8de6a",
    "X-RapidAPI-Host": "coronavirus-smartable.p.rapidapi.com"
}
response = requests.get(url, headers=headers)
print(response)
response.raise_for_status() 
data = response.json()
rows = data["stats"]["breakdowns"]

with open('raw_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = rows[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Data successfully written to raw_data.csv file.")