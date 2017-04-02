import json
import csv, sys

with open(sys.argv[1]) as file:
	data = json.load(file)

with open(sys.argv[2], "w") as file:
	csv_file = csv.writer(file)
	for item in data:
		try:
			csv_file.writerow([item['Title'].encode(encoding="utf-8"), item['ISBN'].encode(encoding="utf-8"), item['Author'].encode(encoding="utf-8")])
		except KeyError:
			continue
