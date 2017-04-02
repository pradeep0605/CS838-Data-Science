import sys

import json

del_count=0

def filter_books(bookname_data, json_tuple):
    global del_count 
    
    jbook_name = ("".join(json_tuple['Original_Title'].encode(encoding="utf-8").split()))
    jauthor_name =  ("".join(json_tuple['Author'].encode(encoding="utf-8").split()))

    for i in range(0, len(bookname_data)):
        item = bookname_data[i]
        string = ("".join(item.split()))
        k = string.rfind("@")
        bookname, authorname = string[:k], string[k+1:]
        #bookname, authorname = ("".join(item.split())).split("@")
        #print "\tcomparing :", bookname, "==", jbook_name, "|", authorname, "==", jauthor_name
        if ((jbook_name.find(bookname) != -1 or bookname.find(jbook_name) != -1) and
           (authorname == jauthor_name or authorname.find(jauthor_name) != -1 or jauthor_name.find(authorname) != -1)):
            #print "Deleting ", bookname_data[i]
            del bookname_data[i]
            del_count = del_count + 1
            break
            

if __name__=="__main__":
    global del_count
    if len(sys.argv) < 3:
        print "Please enter two argements, First argument in the booknames.txt file and other is the json file. Output will output.txt"
    del_count = 0
    argv = sys.argv
    print argv[0], argv[1], argv[2]
    bookname_data = []
    booknamefile =  open(sys.argv[1], "r")
    line = booknamefile.readline()
    
    while line != "":
        bookname_data.append(line)
        line = booknamefile.readline()
    
    json_file = (open(sys.argv[2], "r"))
    line = json_file.readline().strip()
    while line != "":
        if line == "[" or line == "]":
            line = json_file.readline().strip()
            continue 
        if line[len(line) - 1] == ',':
            line = line[:len(line) - 1]

        try:
            tuple = json.loads(line)
            #print tuple
            filter_books(bookname_data, tuple)
        #"""
        except Exception as e:
            print e
            print "Cannot process line :" , line
        #"""
        line = json_file.readline().strip()
    
    write_file = open("filtered_booknames.txt", "w")
    for item in bookname_data:
        write_file.writelines(item)
    write_file.close()
    
    print "Total filtered books: ", del_count