#! /usr/bin/python
import sys
import re
import copy
from numpy import array
from sklearn import tree
from stop_words import get_stop_words
stop_words = get_stop_words('en')

data = []
target = []

def process(context, index, text, targetClass):
	feature = []
	# First word is 'The' or 'A' followed by word with first letter Capitalized
	if re.match(r"^The [A-Z]{1}",text) or re.match(r"^A [A-Z]{1}",text):
		feature.append(True)
	else:
		feature.append(False)

	# Character length of the text
	feature.append(len(text))

	# Word length of the phrase
	feature.append(len(text.split()))

	# All the words which are not stop words should be capitalized
	flag = True 
	for word in text.split():
		if unicode(word, "utf-8") not in stop_words:
			if word[0].islower():
				flag = False
	if flag:
		feature.append(True)
	else:
		feature.append(False)

	# Phrases which have period before and comma after them
	flag = True
	i = index
	while context[i-1] == " ":
		i = i - 1
	if context[i-1] == ".":
		i = index
		while context[i+len(text)+11] == " ":
			i = i + 1
		if context[i+len(text)+11] != ",":
			flag = False
	else:
		flag = False
	
	if flag:
		feature.append(True)
	else:
		feature.append(False)

	# Phrases followed by words ending with s
	m = re.search(r"\w+", context[index+len(text)+11:])
	if m.group(0)[-1] != 's':
		feature.append(False)
	else:
		feature.append(True)

	# If phrase has colon
	if text.find(':') == 1:
		feature.append(True)
	else:
		feature.append(False)

	# If all the letters in the phrase are caps
	if text.isupper():
		feature.append(True)
	else:
		feature.append(False)
	
	data.append(feature)
	target.append(targetClass)
		
	
			

def main(argv):
	textfile = sys.argv[1]
	
	with open(textfile) as f:
	    lines = f.readlines()

	count = 0
	for line in lines:
		print count
		count = count + 1
		m = re.finditer(r"(?<=\<\+\+\+\>)((?!<\/\+\+\+>).)*|(?<=\<\-\-\-[A-Z]\>)((?!<\/\-\-\-[A-Z]>).)*", line)
		if m:
			for x in m:
				if line[x.start()-4] == "+":
					process(line, x.start(), line[x.start():x.end()], True)
				else:
					process(line, x.start(), line[x.start():x.end()], False)

	
	trainDataset = array(data)
	trainTarget = array(target)

	# Use Decicion Trees
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(trainDataset, trainTarget)

	



					
			
			






"""
		text = line
		negtext = copy.deepcopy(text)
		while text:
			#m = re.search(r"(?<=\<\+\+\+\>)(.*)(?=\<\/\+\+\+\>)", text)
			m = re.search(r"(?<=\<\+\+\+\>)((?!<\/\+\+\+>).)*", text)
			if not m:
				break
			#print m.group(0)
			substr = "<+++>"+m.group(0)+"</+++>"
			index = text.find(substr)
			process(text, index, m.group(0), True)
			# Remove the processed text 
			text = text[index+len(substr):]

		m = re.finditer(r"(?<=\<\+\+\+\>)((?!<\/\+\+\+>).)*|(?<=\<\-\-\-[A-Z]\>)((?!<\/\-\-\-[A-Z]>).)*", negtext)
		if m:
			for x in m:
				print negtext[x.start()-5:x.end()]
				break

			

		while negtext:
			m = re.search(r"(\<\-\-\-[A-Z]->)(?<=\<\-\-\-[A-Z]\>)((?!<\/\-\-\-[A-Z]>).)*", negtext)
			if not m:
				break
		 		
			print m.group(0)
			substr = "<--->"+m.group(0)+"</--->"
			index = negtext.find(substr)
			process(negtext, index, m.group(0), False)
			# Remove the processed text 
			negtext = negtext[index+len(substr):]

	print data
	print target

"""
	
	

if __name__ == "__main__":
	main(sys.argv[1:])
