#AUTHOR: Mitch Downey

from queue import SimpleQueue

#Check to see if key and target are within one letter of each other
def checkForValidity(key,target):
	charDifferent = False
	i = 0
	for index in range(min(len(target),len(key))):
		if key[index] != target[index]:
			if(charDifferent):
				return False;
			charDifferent = True;
	if (abs(len(target) - len(key)) > 1) or (charDifferent and abs(len(target) - len(key)) > 0):
		return False
	return True

wordList = []
partialTrees = {}
pairList = []
wordQueue = SimpleQueue()
visited = []

def readFiles(words,pairs):
	with open('dictionary.txt') as inFile:
		for line in inFile:
			lineLength = len(line)
			if(lineLength >= 4 and lineLength <= 6):
				translate = line[:lineLength-1]
				words.append(translate)
	with open('pairs.txt', 'r') as pairFile:
		for line in pairFile:
			pos = line.find(' ')
			if not line[len(line)-1].isalpha():
				end = len(line)-1
			else:
				end = len(line)
			a = line[:pos]
			b = line[pos + 1:end]
			if(len(a) == len(b)):
				pairs.append((a,b))
			else:
				print(a + " and " + b + " have different lengths")

#Create adjacency lists for each word in the wordList
def buildLists():
	for key in wordList:
		partialTrees[key] = []
		for ch in wordList:
			if key != ch:
				if checkForValidity(key,ch):
					partialTrees[key].append(ch)

#Go through the adjacency lists, looking for a path from key to target.
#The first connection to a word will be stored in the last element of that word's
#adjacency list
def parseLists(key, target):
	if key not in partialTrees:
		partialTrees[key] = []
		for ch in wordList:
			if key != ch:
				if checkForValidity(key, ch):
					partialTrees[key].append(ch)
	while not wordQueue.empty():
		wordQueue.get()
	wordQueue.put(key)
	visited.clear()
	while not wordQueue.empty():
		current = wordQueue.get()
		for ch in partialTrees[current]:
			if ch not in visited:
				partialTrees[ch].append(current)
				visited.append(ch)
				wordQueue.put(ch)
			if ch == target:
				return findPath(key,ch)
			
	return "No path found"

#Combine the path from key to target
def findPath(key,target):
	up = partialTrees[target].pop()
	finalPath = target
	while up != key:
		finalPath = up + " " + finalPath
		up = partialTrees[up].pop()
	return up + " " + finalPath

def main():
	readFiles(wordList,pairList)
	print("Files successfully read")
	print("Building partial adjacency trees. Please stand by, this will take approximately 2-4 minutes...")
	buildLists("",wordQueue)
	print("Adjacency lists successfully built. Now finding word ladders: ")
	for a,b in pairList:
		print("From " + a + " to " + b + ": ")
		print(parseLists(a,b) + '\n')

main()