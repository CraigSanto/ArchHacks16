from bs4 import BeautifulSoup
import requests


#Gets popular last names in the 1990's
html = requests.get('http://surnames.behindthename.com/top/lists/united-states/1990')
target = open("last_names.txt", 'w')

soup = BeautifulSoup(html.text, "html.parser")

u = soup.find_all('tr', {'class': 'r0' or 'r1'})
for x in u:
    y = x.find_all('a')
    for i in y:
        target.write(i.text.strip() + '\n')
