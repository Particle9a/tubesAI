import random
import copy
import os
import numpy

def isVHAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	if (x1 == x2):
		return(True)
	elif (y1 == y2):
		return(True)
	return(False)

def isDAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	d1 = abs(x1 - y1)
	d2 = abs(x2 - y2)
	if (d1 == d2):
		return True
	return False

def isHorseAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	c1 = abs(x1-x2)
	c2 = abs(y1-y2)
	if ((c1 == 1) and (c2 == 3)):
		return(True)
	elif ((c1 == 3) and (c2 == 3)):
		return(True)
	return(False)

class Pion :
	def __init__(self, t, x,y) :
		self.type = t
		self.position = (x,y)

	def isThreatenedBy(self,obj) :
		if (obj.type == 'QUEEN'):
			if (isVHAligned(self.position, obj.position)):
				return(True)
			elif (isDAligned(self.position, obj.position)):
				return(True)
		elif (obj.type == 'ROOK'):
			if (isVHAligned(self.position, obj.position)):
				return(True)
		elif (obj.type == 'BISHOP'):
			if (isDAligned(self.position, obj.position)):
				return(True)
		elif (obj.type == 'KNIGHT'):
			if (isHorseAligned(self.position,obj.position)):
				return(True)
		return(False)

takenPos = []
objListW = []
objListB = []

#Membuat List Objek
fil = open('input chess.txt')
for inp in fil :
	inp = inp.split()
	if (inp[0] == 'WHITE'):
		for y in range(0,int(inp[2])):
			posX = 0
			posY = 0
			while ((posX,posY) in takenPos):
				posX = random.randint(0,7)
				posY = random.randint(0,7)
			objListW.append(Pion(inp[1],posX,posY))
			takenPos.append((posX,posY))
	elif (inp[0] == 'BLACK'):
		for y in range(0,int(inp[2])):
			posX = 0
			posY = 0
			while ((posX,posY) in takenPos):
				posX = random.randint(0,7)
				posY = random.randint(0,7)
			objListB.append(Pion(inp[1],posX,posY))
			takenPos.append((posX,posY))

print(takenPos)

def displayPapan(takenPos, whiteList, blackList) :
	for i in range(0,8):
		string = ''
		for j in range(0,8):
			if ((i,j) not in takenPos):
				string += '-'
			else :
				found = False
				for c in whiteList :
					if ((i,j) == c.position):
						found = True
						string += c.type[0]
						break
				if not found :
					for c in blackList :
						if ((i,j) == c.position):
							found = True
							string += c.type.lower()[0]
							break
		print(string)

def countThreat1(whiteList):
	count = 0
	for x in whiteList :
		for y in whiteList :
			if (x != y) :
				if x.isThreatenedBy(y) :
					count += 1
	return count

def countThreat2(whiteList,blackList):
	count = 0
	for x in whiteList :
		for y in blackList :
			if x.isThreatenedBy(y) :
				count += 1
			if y.isThreatenedBy(x) :
				count += 1
	return count

def hillClimb1(takenPos, whiteList):
	minState = {}
	minState['Cost'] = countThreat1(whiteList)
	for x in range(0,len(whiteList)) :
		for a in range(0,8):
			for b in range(0,8):
				if ((a,b) not in takenPos):
					tempPos = copy.deepcopy(takenPos)
					tempWhite = copy.deepcopy(whiteList)
					tempWhite[x].position = (a,b)
					tempPos[x] = (a,b)
					tempV = countThreat1(tempWhite)
					if (tempV < minState['Cost']):
						minState['Cost'] = tempV
						minState['Positions'] = tempPos
						minState['White'] = tempWhite
	return(minState)
	
def hillClimb2(takenPos, whiteList,blackList):
	minState = {}
	minState['Cost'] = countThreat1(whiteList)
	minState['White'] = whiteList
	minState['Black'] = blackList
	for x in range(0,len(whiteList)) :
		for a in range(0,8):
			for b in range(0,8):
				if ((a,b) not in takenPos):
					tempPos = copy.deepcopy(takenPos)
					tempWhite = copy.deepcopy(whiteList)
					tempWhite[x].position = (a,b)
					tempPos[x] = (a,b)
					tempV = countThreat1(tempWhite) + countThreat1(blackList) - countThreat2(tempWhite,blackList)
					if (tempV < minState['Cost']):
						minState['Cost'] = tempV
						minState['Positions'] = tempPos
						minState['White'] = tempWhite
	for x in range(0,len(blackList)) :
		for a in range(0,8):
			for b in range(0,8):
				if ((a,b) not in takenPos):
					tempPos = copy.deepcopy(takenPos)
					tempBlack = copy.deepcopy(blackList)
					tempBlack[x].position = (a,b)
					tempPos[x + len(whiteList)] = (a,b)
					tempV = countThreat1(tempWhite) + countThreat1(tempBlack) - countThreat2(whiteList, tempBlack)
					if (tempV < minState['Cost']):
						minState['Cost'] = tempV
						minState['Positions'] = tempPos
						minState['Black'] = tempBlack
	return(minState)

def hillClimbS1(takenPos,whiteList) :
	minState = {}
	minState['Positions'] = copy.deepcopy(takenPos)
	minState['White'] = copy.deepcopy(whiteList)
	minState['Cost'] = countThreat1(whiteList)
	betterExist = True
	while betterExist :
		betterExist = False
		os.system('cls')
		tempState = hillClimb1(minState['Positions'],minState['White'])
		if (tempState['Cost'] < minState['Cost']):
			minState = tempState
			betterExist = True
		print("Solution :")
		displayPapan(minState['Positions'], minState['White'],[])
		print(minState['Cost'])			

def hillClimbS2(takenPos,whiteList,blackList) :
	minState = {}
	minState['Positions'] = copy.deepcopy(takenPos)
	minState['White'] = copy.deepcopy(whiteList)
	minState['Black'] = copy.deepcopy(blackList)
	minState['Cost'] = countThreat1(whiteList) + countThreat1(blackList) - countThreat2(whiteList,blackList)
	betterExist = True
	while betterExist :
		betterExist = False
		os.system('cls')
		tempState = hillClimb2(minState['Positions'],minState['White'], minState['Black'])
		if (tempState['Cost'] < minState['Cost']):
			minState = tempState
			betterExist = True
		print("Solution :")
		displayPapan(minState['Positions'], minState['White'],minState['Black'])
		print(minState['Cost'])

def simulatedAnne1(takenPos,whiteList,temperature):
	minState = {}
	minState['White'] = whiteList
	minState['Positions'] = takenPos
	minState['Cost'] = 0	
	if (temperature < 0.001):
		return minState
	else :
		nextStt = False
		countStep = 0
		while not(nextStt):
			countStep += 1
			pieceNum = random.SystemRandom().randint(0,len(whiteList)-1)
			a = random.SystemRandom().randint(0,7)
			b = random.SystemRandom().randint(0,7)
			tempPos = copy.deepcopy(takenPos)
			tempWhite = copy.deepcopy(whiteList)
			tempWhite[pieceNum].position = (a,b)
			tempPos[pieceNum] = (a,b)
			if (countThreat1(tempWhite) < countThreat1(whiteList)):
				minState = simulatedAnne1(tempPos,tempWhite,temperature-0.005)
				return(minState)
			elif (countThreat1(tempWhite) == countThreat1(whiteList)):
				change = numpy.random.choice([True,False], p =[temperature,1-temperature])
				if change :
					minState = simulatedAnne1(tempPos,tempWhite,temperature-0.005)
					return(minState)
				else :
					continue
			else :
				probFactor = temperature*1/(countThreat1(tempWhite)-countThreat1(whiteList))
				change = numpy.random.choice([True,False], p = [probFactor,1-probFactor])
				if change :
					minState = simulatedAnne1(tempPos,tempWhite,temperature-0.005)
					return(minState)
				else :
					continue
			if(countStep >= 100):
				nextStt = True
		return(minState)

if objListB == [] :
	os.system('cls')
	hillClimbS1(takenPos,objListW)
	res = simulatedAnne1(takenPos,objListW,0.95)
	print(res['Cost'])
	displayPapan(res['Positions'],res['White'],[])

elif objListW == [] :
	hillClimbS1(takenPos,objListB)
else :
	hillClimbS2(takenPos,objListW,objListB)


print
print 
print(countThreat1(objListW))
displayPapan(takenPos, objListW, objListB)