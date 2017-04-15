import json
import csv, sys

with open(sys.argv[1]) as file:
	data = json.load(file)

with open(sys.argv[2], "w") as file:
	csv_file = csv.writer(file)
	#csv_file.writerow([data[0].keys()[7], data[0].keys()[2], data[0].keys()[3], data[0].keys()[5], data[0].keys()[4],data[0].keys()[11]])
	csv_file.writerow(["Original_Title","Author","ISBN13","Publisher","Published_Date"])
	for item in data:
		try:
			published_date = ""
			if len(item['Published_Date']) == 3:
				#published_date = item['Published_Date'][0].encode(encoding="utf-8")+" "+item['Published_Date'][1].encode(encoding="utf-8")+", "+item['Published_Date'][2].encode(encoding="utf-8").strip('\n')
				published_date = str(item['Published_Date'][-1].encode(encoding="utf-8")).strip()
			elif len(item['Published_Date']) == 2:
				published_date = item['Published_Date'][0].encode(encoding="utf-8")+", "+item['Published_Date'][1].encode(encoding="utf-8").strip('\n')
			else:
				published_date = item['Published_Date'][0].encode(encoding="utf-8").strip('\n')
			csv_file.writerow([item['Original_Title'].encode(encoding="utf-8"), item['Author'].encode(encoding="utf-8"), str(item['ISBN13'].encode(encoding="utf-8")),
			item['Publication'].encode(encoding="utf-8"), published_date])
		except KeyError:
			continue
