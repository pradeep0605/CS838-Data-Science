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
3			Publisher
4			Published_Date
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

with open('merged_table.csv', "wb") as file, open('all_matched.csv', "wb") as file_all:
	csv_file = csv.writer(file)
	csv_file_all = csv.writer(file_all)
	
	csv_file.writerow(["ID","Title","Author","ISBN13","Publication","Published_Date","Ratings","Genres","Reviews","Average_Rating","Language"])

	matched_count = 0
	for row in matches:
		try:
			matched_count += 1
			#print str(matched_count) + " : " +  row[1] + " : " + str(gr_dict[row[1]]['Original_Title'].encode(encoding="utf-8")) + row[2] + " : " + str(ban_dict[row[2]][0])
			
			gr_item = gr_dict[row[1]]
			ban_item = ban_dict[row[2]]
			
			key = matched_count
			title = ""
			title_from_gr = None
			author = ""
			isbn13 = ""
			publication = ""
			
			#Rule 1 for title : Pick the one which is longest
			if len(str(gr_item['Original_Title'].encode(encoding="utf-8"))) >= len(str(ban_item[0])):
				title = str(gr_item['Original_Title'].encode(encoding="utf-8"))
				title_from_gr = True
			else :
				title = str(ban_item[0])
				title_from_gr = False
				
			#Rule 2 for author : Pick the one which is longest
			if len(str(gr_item['Author'].encode(encoding="utf-8"))) >= len(str(ban_item[1])):
				author = str(gr_item['Author'].encode(encoding="utf-8"))
			else :
				author = str(ban_item[1])
			
			#Rule 3 for ISBN-13: Take ISBN-13 from the matched keys obtained from Magellan from the source you picked title from
			#Rule 4 for Publisher: Take from the source you picked title from
			if title_from_gr :
				isbn13 = row[1]
				publication = str(gr_item['Publication'].encode(encoding="utf-8"))
			else :
				isbn13 = row[2]
				publication = str(ban_item[3])
			
			#Rule 5 for Published Date: Always take from BAN
			published_date = str(ban_item[4])
			
			#Rule 6 for Ratings, Genres, Reviews, Average Rating, Language: Always pick from Goodreads as none of them are present in BAN
			ratings = str(gr_item['Ratings'].encode(encoding="utf-8"))
			reviews = str(gr_item['Reviews'].encode(encoding="utf-8"))
			avg_rating = str(gr_item['Average_Rating'].encode(encoding="utf-8"))
			lang = str(gr_item['Edition_Language'].encode(encoding="utf-8"))
			
			#Genres
			genres = gr_item['Genres']
			genre = ""
			i = 0
			for g in genres:
				if i == (len(genres) - 1):
					genre += str(g.encode(encoding="utf-8"))
					
				else :
					genre += str(g.encode(encoding="utf-8"))
					genre += ", "
				i += 1
			
			# Write to the file which contains all matched tuples from source tables
			csv_file_all.writerow([matched_count, row[1], str(gr_item['Original_Title'].encode(encoding="utf-8")), str(gr_item['Author'].encode(encoding="utf-8")), str(gr_item['Publication'].encode(encoding="utf-8")), str(gr_item['Published_Date']), row[2], str(ban_item[0]), str(ban_item[1]), str(ban_item[3]), str(ban_item[4])])
			
			# Write to the final table E
			csv_file.writerow([matched_count, title, author, isbn13, publication, published_date, ratings, genre, reviews, avg_rating, lang])
		except KeyError:
			matched_count -= 1
			continue
