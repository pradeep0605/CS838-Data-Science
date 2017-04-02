import json
import csv, sys

with open(sys.argv[1]) as file:
	data = json.load(file, strict=False)

with open(sys.argv[2], "w") as file:
	csv_file = csv.writer(file)
	book_dict = {}
	for item in data:
		try:
			if item['ISBN-13'].encode(encoding="utf-8") in book_dict:
				book_dict[item['ISBN-13'].encode(encoding="utf-8")] += 1
				continue
			else:
				book_dict[item['ISBN-13'].encode(encoding="utf-8")] = 1
				csv_file.writerow([item['Original_Title'].encode(encoding="utf-8"), item['Author'].encode(encoding="utf-8"), item['ISBN-13'].encode(encoding="utf-8"), item['Publisher'].encode(encoding="utf-8"), item['Publication date'].encode(encoding="utf-8")])
		except Exception as e:
			print "!!!!!!!!!!!!!! Exception ", e
			continue
	csv_file.close()

	repeat_count = 0
	for key in book_dict:
		#repeat_count = 0
		repeated = 0
		if (book_dict[key] > 1):
			repeat_count = repeat_count + 1
			print key + " : " + str(book_dict[key])
	
	print "Number tuples that were repeated :", repeat_count

