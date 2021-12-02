'''
Web Scrapping MLB Tables

author: Daryl Adopo
'''


# Required Packages
 from bs4 import BeautifulSoup
 import requests
 import csv


url="https://www.spotrac.com/mlb/payroll/2021/positional"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
# print(soup.prettify()) # print the parsed data of html


# ### Find Table of interest on the webpage


mlb_table = soup.find("table", attrs={"class": "datatable rtable captracker"})

mlb_table_header = mlb_table.thead.find_all("tr") # Headers
mlb_table_data = mlb_table.tbody.find_all("tr")  # Rows


# ### Extract Information from the Table

# Get all the headings
headings = []
for th in mlb_table_header[0].find_all("th"):
    # remove any newlines and extra spaces from left and right
    headings.append(th.text.replace('\n', ' ').strip())

print(headings)


data = []
for tr in mlb_table_data: # find all tr's from table's tbody
    if tr.attrs:
        if tr.attrs["class"][0] == "average":
            continue
    row = {}
    # Each row is stored in the form of
    # row = {'Rank': '', 'Team': '',etc...}

    # find all td's in tr and zip it with headings
    for td, th in zip(tr.find_all("td"), headings):
        row[th] = td.text.replace('\n', '').strip()
    data.append(row)

print(data)


# ### Exporting Data to Excel


with open("mlb_positional.csv", 'w', newline = '') as out_file:
    writer = csv.DictWriter(out_file, headings)
    writer.writeheader()
    writer.writerows(data)
