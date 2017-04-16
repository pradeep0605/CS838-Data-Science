# TODO(all) : Write code to merge tables

import json
import csv, sys

f1 = open('Matches.csv')
matches = csv.reader(f1)

'''for row in matches:
  print row[1], row[2]'''


# Create a dictionary for goodreads data with ISBN13 as the key
# This dictionary will be used to access information about matched pairs on goodreads side
gr_dict = {}

with open('../Phase3/test/goodreads.json') as file:
	data = json.load(file)
	
for item in data:
	#print item
	try:
		gr_dict[item['ISBN13'].encode(encoding="utf-8")] = item
	except KeyError:
			continue
			

'''#Test the json is being read 
gr_count = 0
for key in gr_dict:
	gr_count += 1
	#print str(gr_count) + " : " + key + " : " + str(gr_dict[key]['Original_Title'].encode(encoding="utf-8"))
print gr_count
'''

# Create a dictionary for barnes and noble data with ISBN-13 as the key
# This dictionary will be used to access information about matched pairs on barnes and noble side
ban_dict = {}

f2 = open('../Phase3/data/barnes_and_noble.csv')
ban = csv.reader(f2)

'''
Barnes and Noble CSV schema
index		Column
0			Original_Title
1			Author
2			ISBN13
4			Publisher
5			Published_Date
'''

for row in ban:
	try:
		ban_dict[row[2]] = row
	except KeyError:
			continue

'''
#Test the barnes and noble data is being read and stored in dict
ban_count = 0
for key in ban_dict:
	try:
		ban_count += 1
		print str(ban_count) + " : " + key + " : " + str(ban_dict[key])
	except KeyError:
			continue
print ban_count
'''

with open('merged.csv', "w") as file:
	csv_file = csv.writer(file)

	matched_count = 0
	for row in matches:
		try:
			matched_count += 1
			#print str(matched_count) + " : " +  row[1] + " : " + str(gr_dict[row[1]]['Original_Title'].encode(encoding="utf-8")) + row[2] + " : " + str(ban_dict[row[2]][0])
			#TODO(all): Add rules to process before adding
			csv_file.writerow([matched_count, row[1], str(gr_dict[row[1]]['Original_Title'].encode(encoding="utf-8")), row[2], str(ban_dict[row[2]][0])])
			
		except KeyError:
				continue
