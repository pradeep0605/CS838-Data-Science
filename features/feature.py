#! /usr/bin/python
import sys
import re
import copy
from numpy import array
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model
from stop_words import get_stop_words
stop_words = get_stop_words('en')



def process(context, index, index_end, text):
	text = text.strip()

	feature = []
	# First word is 'The' or 'A' followed by word with first letter Capitalized
	if re.match(r"^The [A-Z]{1}",text) or re.match(r"^A [A-Z]{1}",text):
		feature.append(True)
	else:
		feature.append(False)
	# Character length of the text
	feature.append(len(text))
	
	# word length greater than 2
	if len(text.split()) >= 2:
		feature.append(True)
	else:
		feature.append(False)
	
	#Word length of the phrase
	feature.append(len(text.split()))

	# All the words which are not stop words should be capitalized
	flag = True 
	for word in text.split():
		if unicode(word, "utf-8") not in stop_words:
			if word[0].islower():
				flag = False

	
	feature.append(flag)
	
	# check if there is a period within the phrase
	if text.find(".") != -1:
		feature.append(True)
	else:
		feature.append(False)

	"""
	# Phrases which have period before and comma after them
	flag = False 
	i = index
	while context[i-1] == " ":
		i = i - 1
	if context[i-1] == ".":
		i = index_end
		while context[i] == " ":
			i = i + 1
		if context[i] == ",":
			flag = True 

	feature.append(flag)
	"""

	"""
	# Phrases followed by words ending with s
	m = re.search(r"\w+", context[index_end+1:])
	if m.group(0)[-1] != 's':
		feature.append(False)
	else:
		feature.append(True)
	"""	

	"""
	# If there is 'In' before the phrase, it is positive
	i = index
	while context[i-1] == " ":
		i = i - 1
	m = re.match("[Ii]n",context[i-2:i])
	if m:
		feature.append(True)
	else:
		feature.append(False)
	"""
	
	# If phrase has colon
	if text.find(':') != -1:
		feature.append(True)
	else:
		feature.append(False)

	"""
	# If all the letters in the phrase are caps
	if text.isupper():
		feature.append(True)
	else:
		feature.append(False)
	"""

	# If the phrase is inside brackets (), then it is negative
	flag = False 
	i = index
	while context[i-1] == " ":
		i = i - 1
	if context[i-1] == "(":
		i = index_end
		while context[i] == " ":
			i = i + 1
		if context[i] == ")":
			flag = True 
	feature.append(flag)
	

	# If a phrase is in between two full stops, then it is negative
	flag = False 
	i = index
	while context[i-1] == " ":
		i = i - 1
	if context[i-1] == ".":
		i = index_end
		while context[i] == " ":
			i = i + 1
		if context[i] == ".":
			flag = True 
	feature.append(flag)


	# If a phrase is in between two commas, then it is negative
	flag = False 
	i = index
	while context[i-1] == " ":
		i = i - 1
	if context[i-1] == ",":
		i = index_end
		while context[i] == " ":
			i = i + 1
		if context[i] == ",":
			flag = True 
	feature.append(flag)

	# If there is 'By' before the phrase, it is a negative example 
	"""
	i = index
	while context[i-1] == " ":
		i = i - 1
	m = re.match("[Bb][Yy]",context[i-2:i])
	if m:
		feature.append(True)
	else:
		feature.append(False)
	"""

	return feature
	

def main(argv):
	trainfile = sys.argv[1]
	testfile = sys.argv[2]
	

	#get the train dataset
	with open(trainfile) as f:
	    lines = f.readlines()

	data = []
	target = []

	for line in lines:
		m = re.finditer(r"(?<=\<\+\+\+\>)((?!<\/\+\+\+>).)*|(?<=\<\-\-\-[A-Z]\>)((?!<\/\-\-\-[A-Z]>).)*", line)
		if m:
			for x in m:
				if line[x.start()-4] == "+":
					data.append(process(line, x.start()-5, x.end()+6, line[x.start():x.end()]))
					target.append(True)
				elif line[x.start() - 4] == '-':
					data.append(process(line, x.start()-6, x.end()+7, line[x.start():x.end()]))
					target.append(False)
				else:
				    print "SOMETHING WRONG!"

	
	trainDataset = array(data)
	trainTarget = array(target)

	cvs_scores = {}

	#Use various classifiers and get the precision and recall 
	classifier = {'DecisionTree' : DecisionTreeClassifier(random_state=0), 'SVM         ' : svm.SVC(probability=True, random_state=0), 'RandomForest' :
	RandomForestClassifier(), 'kNN         ' :KNeighborsClassifier(5)}
	for clf in classifier:
		precisionScores = cross_val_score(classifier[clf], trainDataset, trainTarget, cv=5, scoring='precision')
		recallScores = cross_val_score(classifier[clf], trainDataset, trainTarget, cv=5, scoring='recall')
		cvs_scores[clf] = { precisionScores.mean(), recallScores.mean()}

	#get f1
	for val in cvs_scores:
		print val, " \t:\t", cvs_scores[val] 


	#get the test dataset
	with open(testfile) as f:
	    lines = f.readlines()

	data = []
	target = []
	phrases = []
	for line in lines:
		m = re.finditer(r"(?<=\<\+\+\+\>)((?!<\/\+\+\+>).)*|(?<=\<\-\-\-[A-Z]\>)((?!<\/\-\-\-[A-Z]>).)*", line)
		if m:
			for x in m:
				if line[x.start()-4] == "+":
					phrases.append(line[x.start() - 5:x.end() + 6])
					data.append(process(line, x.start()-5, x.end()+6, line[x.start():x.end()]))
					target.append(True)
				elif line[x.start() - 4] == '-':
					#print line[x.start()-20:x.end()+20]
					phrases.append(line[x.start() - 6:x.end() + 7])
					data.append(process(line, x.start()-6, x.end()+7, line[x.start():x.end()]))
					target.append(False)
				else:
				    print "SOMETHING WRONG!"

	
	testDataset = array(data)
	testTarget = array(target)

	for clssfr in classifier:
		#clf = tree.DecisionTreeClassifier()
		print "====================================", clssfr,"===================================="
		clf = classifier[clssfr]
		clf = clf.fit(trainDataset, trainTarget)
		results = clf.predict(testDataset)
		total_positive = float(0)
		total_negative = float(0)
		predicted_positive = float(0)
		predicted_negative = float(0)
		actual_positive = float(0)
		false_positive = float(0)
		for phrase, line, actual, predicted in zip(phrases, testDataset,testTarget,results):
			if predicted == True:
				predicted_positive = predicted_positive + 1
			else:
				predicted_negative = predicted_negative + 1

			if actual == True:
				total_positive = total_positive + 1
				if predicted == actual:
					actual_positive = actual_positive + 1
			else:
				total_negative = total_negative + 1
				if predicted != actual:
					false_positive = false_positive + 1
			#if actual != predicted:
			#	print line, actual,predicted, phrase
		print "total_positive =", total_positive
		print "total_negative = ", total_negative 
		print "predicted_positive = ", predicted_positive
		print "predicted_negative =", predicted_negative
		print "actual_positive = ", actual_positive
		print "false_positive = ", false_positive
		print "Precision = ", (actual_positive / (actual_positive + false_positive)), "  Recall = ", (actual_positive / total_positive)

if __name__ == "__main__":
	main(sys.argv[1:])
