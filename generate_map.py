import googlemaps
import gmplot
import geojson
import rethinkdb as r
import time
import sys
import numpy as np
import random
from datetime import datetime
from sklearn.cluster import KMeans

center = [38.360556, -92.592181]
gmap = gmplot.GoogleMapPlotter(center[0], center[1], 7)

num_clinics = 10


r.connect( "DESKTOP-K4G0PLO", 28015).repl()
#for i in range(0, 6):
while 1:
	tabletemp = r.db("ArchHacks").table("County_Lines").run()
	for item in tabletemp:
		county_ind = 0
		county_lat = []
		county_lng = []
		coords_temp = item["geometry"]["coordinates"][0]
		for coords in coords_temp:
			county_lat.append(coords[0])
			county_lng.append(coords[1])
			county_ind+=1
		gmap.polygon(county_lng, county_lat, "pink", county_lngedge_color="black", edge_width=1, face_color=None, face_alpha=0.1)

	people_table = r.db("ArchHacks").table("People").filter(r.row["status"] == False).run()
	count = r.db("ArchHacks").table("People").filter(r.row["status"] == False).count().run()
	print(count)

	ind_length = (count)/(num_clinics*4)

	people_lat = []
	people_lng = []
	for person in people_table:
		coords = person["coordinates"]
		coords[0] = float(coords[0])
		coords[1] = float(coords[1])
		people_lng.append(coords[0])
		people_lat.append(coords[1])
	gmap.heatmap(people_lng, people_lat, 10, 10)

	cluster_data = np.column_stack((np.array(people_lng), np.array(people_lat)))
	kcluster = KMeans(num_clinics).fit(cluster_data)
	for cluster in kcluster.cluster_centers_:
		gmap.circle(cluster[0], cluster[1], 5000, "red", ew=1)
	gmap.draw("testmap.html")
	gmap.heatmap_points = []



	for i in range(0, len(kcluster.cluster_centers_)):
		d = kcluster.transform(cluster_data)[:, i]
		print(ind_length)
		ind = np.argsort(d)[::][:ind_length]
		popdict = {"allergies" : 0, "vision" : 0, "childcare" : 0, "general" : 0, "mental" : 0, 
			"illness" : 0, "nutritional" : 0, "sexual health" : 0, "pregnant" : 0, 
			"physical" : 0}
		for j in range(0, ind_length):
			close_people = r.db("ArchHacks").table("People").filter((r.row["coordinates"] == cluster_data[ind][j]) & (r.row["status"] == False)).run()
			for person in close_people:
				temp = person["preferences"]
				for pref in temp:
					popdict[pref]+=1
				rand = random.randint(0, 100)
				cured = False
				add = 5 * random.randint(0, len(person["preferences"]))
				if rand > (30 + add):
					cured = True
				r.db("ArchHacks").table("People").filter(r.row["coordinates"] == person["coordinates"]).update({"status" : cured}).run()
		r.db("ArchHacks").table("Clinics").insert([{
				"requests" : popdict,
				"lat" : kcluster.cluster_centers_[i][0],
				"long" :  kcluster.cluster_centers_[i][1]
		}]).run()
		people_table = r.db("ArchHacks").table("People").filter(r.row["status"] == False).run()
		count = r.db("ArchHacks").table("People").filter(r.row["status"] == False).count().run()
		print(count)

		people_lat = []
		people_lng = []
		for person in people_table:
			coords = person["coordinates"]
			coords[0] = float(coords[0])
			coords[1] = float(coords[1])
			people_lng.append(coords[0])
			people_lat.append(coords[1])
		gmap.heatmap(people_lng, people_lat, 10, 10)
		gmap.draw("testmap.html")
		gmap.heatmap_points = []

	gmap.draw("testmap.html")
	gmap.shapes = []
	gmap.heatmap_points = []