import json
import csv, sys

with open(sys.argv[1]) as file:
	data = json.load(file, strict=False)

#map to give months names from numbers
	date_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
	    7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

#to match the date format of goodreads, we need to append postfixes st,nd,rd,th after the date.
def daymap(day):
    try:
			if day == 1 or day == 21 or day == 31:
				return str(day) + "st"
			if day == 2 or day == 22:
				return str(day) + "nd"
			if day == 3 or day == 23:
				return str(day) + "rd"
			return str(day) + "th"
    except Exception as e:
		print "============================================== Exception:",e
		return "NULL"

with open(sys.argv[2], "w") as file:
	csv_file = csv.writer(file)
	book_dict = {}
	csv_file.writerow(["Original_Title","Author","ISBN13","Publisher","Published_Date"])
	csv_file.writerow(["pradeepanna","sharathanna","sowrabha","oaktreeapartments","2017"])
	
	for item in data:
		try:
			if item['ISBN-13'].encode(encoding="utf-8") in book_dict:
				book_dict[item['ISBN-13'].encode(encoding="utf-8")] += 1
				continue
			else:
				month, date, year = item['Publication date'].encode(encoding="utf-8").split('/')
				month = date_map[int(month)]
				date = daymap(int(date))
				#published_date = month + " " + date + ", " + year
				published_date = str(year).strip()
				book_dict[item['ISBN-13'].encode(encoding="utf-8")] = 1
				csv_file.writerow([item['Original_Title'].encode(encoding="utf-8"), item['Author'].encode(encoding="utf-8"),
				str(item['ISBN-13'].encode(encoding="utf-8")),
				item['Publisher'].encode(encoding="utf-8"), published_date])
		except Exception as e:
			print "!!!!!!!!!!!!!! Exception ", e
			continue

	repeat_count = 0
	for key in book_dict:
		#repeat_count = 0
		repeated = 0
		if (book_dict[key] > 1):
			repeat_count = repeat_count + 1
			print key + " : " + str(book_dict[key])
	
	print "Number tuples that were repeated :", repeat_count

