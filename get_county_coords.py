from bs4 import BeautifulSoup
import requests
import json
import random
html = requests.get('http://www.ala.org/magirt/publicationsab/mo')

#url = 'https://bubinga.co/wp-content/uploads/jsoncounties.min_.js'
#response = requests.get(url)
#data = response.json()
#Gets all the
#i = open('county_lines.txt', 'w')
#c =data['features'][25]['counties']
#i = 0
#for e in c:
#    print(c[i]['name'] + " County)
#    i +=1
soup = BeautifulSoup(html.text, 'html.parser')
soup = soup.find_all('td')
#print(soup)
def convert_to_dec(text):
    #print(text)
    #TODO: make it more general ('ie: not break for degree over 100')

    degree = text.split(' ')[1]
    minutes = text.split(' ')[2][1:3]
    seconds = text.split('´')[1][:3]
    return float(random.uniform(-.3,.3) + (-1 if (text[0] == 'W' or text[0]=='S') else 1)*
    float(degree) + (float)(float(minutes)/60) + (float)(float(seconds)/3600) - .5)


def get_lat_lon():
    #f = open('counties.txt', 'w')


    i = 0

    name = ''
    lat = 0
    lon = 0

    min_lat = 36.494334
    max_lat = 40.56320
    threshold_lat1 = 39.012929
    threshold_lat2 = 39.489351
    threshhold_lat_bottom1 = 38.405990
    threshhold_lat_bottom2 = 37.954110
    min_long = -94.587793
    max_long = -89.160549
    max_long1 =  -90.369045
    max_long2 = -91.182034
    max_long_bottom = -90.161890

    data = {}
    for x in soup:
        if i%5 == 0:
            #print(x.text.strip())
            #f.write(x.text.strip() + '\n')
            name = x.text.strip()
        if i%5 == 1:
            #print("Longitude: " + convert_to_dec(x.text.strip()))
            lon = convert_to_dec(x.text.strip())
            #lon = max(lon, )
            #lon = min(lon,)
        if i%5 == 3:
            #print("Latitude: " +  convert_to_dec(x.text.strip()))
            lat = convert_to_dec(x.text.strip())
            if float(lon) < min_long:
                 lon = float(min_long * random.uniform(.95, 1))
            if float(lon) > max_long:
                 lon = float(max_long * random.uniform(1, 1.05))
            if float(lat) < min_lat:
                 lat = float(min_lat * random.uniform(1, 1.05))
            if float(lat) > max_lat:
                 lat = float(max_lat * random.uniform(.95, 1))
            if float(lat) > threshold_lat1 and float(lon) > max_long1:
                 lon = float(max_long1 * random.uniform(1, 1.05))
            if float(lat) > threshold_lat2 and float(lon) > max_long2:
                 lon = float(max_long2 * random.uniform(1, 1.05))
            if float(lat) > threshhold_lat_bottom2 and float(lat) < threshhold_lat_bottom1 and float(lon) > max_long_bottom:
                 lon = float(max_long_bottom * random.uniform(1, 1.05))
            data[name] = [lat, lon]
            name = ''
            lat = 0
            lon = 0
                #print("===========")

        i+=1
    return data


    #print('county:  ' +  y.text.strip())
#    for i in range(len(y)):
        #print(y[i].text.strip())
