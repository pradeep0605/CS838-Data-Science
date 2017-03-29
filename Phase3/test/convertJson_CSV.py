import json
import csv, sys

with open(sys.argv[1]) as file:
	data = json.load(file)

with open(sys.argv[2], "w") as file:
	csv_file = csv.writer(file)
	csv_file.writerow([data[0].keys()[7], data[0].keys()[2], data[0].keys()[3], data[0].keys()[5], data[0].keys()[4],data[0].keys()[11]])
	for item in data:
		try:
			csv_file.writerow([item['Title'].encode(encoding="utf-8"), item['Edition_Language'].encode(encoding="utf-8"), item['ISBN'].encode(encoding="utf-8"), item['ISBN13'].encode(encoding="utf-8"), item['Publication'].encode(encoding="utf-8"), item['Published_Date']])
		except KeyError:
			continue
