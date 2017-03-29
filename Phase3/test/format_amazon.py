import json
import csv, sys

with open(sys.argv[1]) as file:
	data = json.load(file, strict=False)

with open(sys.argv[2], "w") as file:
	csv_file = csv.writer(file)
	for item in data:
		try:
			#csv_file.writerow([item['Title'].encode(encoding="utf-8"), item['Ratings'].encode(encoding="utf-8"),
			#item['ProductDetails'][0]['Publisher'].encode(encoding="utf-8")])
			pub_idx = item['ProductDetails'].index("Publisher:")
			lang_idx = item['ProductDetails'].index("Language:")
			isbn_idx = item['ProductDetails'].index("ISBN-10:")
			isbn13_idx = item['ProductDetails'].index("ISBN-13:")
			pg_idx = item['ProductDetails'].index("Paperback:")
			print p_idx
			print item['ProductDetails'][p_idx]+item['ProductDetails'][p_idx+1]
		except KeyError:
			continue
