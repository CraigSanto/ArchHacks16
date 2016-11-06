from bs4 import BeautifulSoup
import requests


#Gets popular baby first names from 2010's
html = requests.get('https://www.ssa.gov/oact/babynames/decades/names2010s.html')
target = open("first_names.txt", 'w')
#target.write(html.text)


soup = BeautifulSoup(html.text, "html.parser")

u = soup.find_all('tr', {'align':'right'})
for x in u:
     y = x.find_all('td', {'align':'center'})
     for i in y:
        target.write(i.text.strip() + '\n')
