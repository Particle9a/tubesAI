import random
import copy
import os
import numpy

# Return true if two chess piece are aligne horizontally or vertically
def isVHAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	if (x1 == x2):
		return(True)
	elif (y1 == y2):
		return(True)
	return(False)

# Return true if two chess piece are aligned diagonally
def isDAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	d1 = abs(x1 - y1)
	d2 = abs(x2 - y2)
	if (d1 == d2):
		return True
	return False

# Return true if horse threats other piece
def isHorseAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	c1 = abs(x1-x2)
	c2 = abs(y1-y2)
	if ((c1 == 1) and (c2 == 3)):
		return(True)
	elif ((c1 == 3) and (c2 == 1)):
		return(True)
	return(False)

# Class for chess piece
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

# Initialization for, position taken by piece, list of white piece and list of black piece
takenPos = []
objListW = []
objListB = []

# Reading file, and assign the piece to list initialized before
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

# DISPLAY FUNCTION 
def displayPapan(takenPos, whiteList, blackList) :
	for i in range(0,8):
		string = ''
		for j in range(0,8):
			if ((i,j) not in takenPos): #Kayaknya ketuker
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
	print()
	print(takenPos)

# THREAT (ENERGY) Counter
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

# THREAT POSISITION
def printThreat1(whiteList):
	for x in whiteList :
		for y in whiteList :
			if (x != y) :
				if x.isThreatenedBy(y) :
					print(y.position,"attack", x.position)

def printThreat2(whiteList,blackList):
	for x in whiteList:
		for y in blackList:
			if x.isThreatenedBy(y):
				print(y.position, "attack", x.position)
			if y.isThreatenedBy(x):
				print(x.position, "attack", y.position)

# HILL CLIMBING ALGORITHM
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
	minState['Cost'] = countThreat1(whiteList) + countThreat1(blackList) - countThreat2(whiteList,blackList)
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
	print()
	print("Threats (same color) =", minState['Cost'])	
	print()
	printThreat1(minState['White'])	

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
		tempState = hillClimb2(minState['Positions'], minState['White'], minState['Black'])
		if (tempState['Cost'] < minState['Cost']):
			minState = tempState
			betterExist = True
		print("Solution :")
		displayPapan(minState['Positions'], minState['White'],minState['Black'])
		print(abs(minState['Cost']))
	# print("Threats (same color) =")
	# printThreat1(minState['White'])
	# print("=======================")
	# printThreat1(minState['Black'])
	# print()
	# print("Threat across color =")
	# printThreat2(minState['White'],minState['Black'])

# SIMULATED ANNEALING ALGORITHM
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
	
def simulatedAnne2(takenPos,whiteList,blackList,temperature):
	minState = {}
	minState['White'] = whiteList
	minState['Black'] = blackList
	minState['Positions'] = takenPos
	minState['Cost'] = countThreat1(whiteList) + countThreat1(blackList) - countThreat2(whiteList,blackList)
	for i in range (0,100):
		# print(i)
		# print(minState['Cost'])
		if (temperature == 0):
			return minState
		tempPos = []
		tempWhite = copy.deepcopy(whiteList)
		tempBlack = copy.deepcopy(blackList)
		for x in range(0,len(whiteList)):
			posX = random.randint(0,7)
			posY = random.randint(0,7)
			while ((posX,posY) in tempPos):
				posX = random.randint(0,7)
				posY = random.randint(0,7)
			tempPos.append((posX,posY))
			tempWhite[x].position = (posX,posY)
		for x in range(0,len(blackList)):
			posX = random.randint(0,7)
			posY = random.randint(0,7)
			while ((posX,posY) in tempPos):
				posX = random.randint(0,7)
				posY = random.randint(0,7)
			tempPos.append((posX,posY))
			tempBlack[x].position = (posX,posY)
		tempV = countThreat1(tempWhite) + countThreat1(tempBlack) - countThreat2(tempWhite,tempBlack)
		if (tempV < minState['Cost']):
			minState['White'] = tempWhite
			minState['Black'] = tempBlack
			minState['Positions'] = tempPos
			minState['Cost'] = tempV
		else:
			probFactor = numpy.exp((minState['Cost'] - tempV)/temperature)
			change = numpy.random.choice([True,False], p = [probFactor,1-probFactor])
			if (change):
				minState['White'] = tempWhite
				minState['Black'] = tempBlack
				minState['Positions'] = tempPos
				minState['Cost'] = tempV
		temperature = temperature - 0.001	
	return minState

#GENETIC ALGORITHM
def Selection(population):
	probList = []
	pops = copy.copy(population)
	maxThreat = 30
	sumEn = sum((maxThreat - item['Cost']) for item in population)
	for x in population :
		prob = (maxThreat - x['Cost'])/sumEn
		probList.append(prob)
	t1 = numpy.random.choice(population,p = probList)
	pops.remove(t1)
	sumEn = sum((maxThreat - item['Cost']) for item in pops)
	probList = []
	for x in pops :
		prob = (maxThreat - x['Cost'])/sumEn
		probList.append(prob)
	t2 = numpy.random.choice(pops,p =probList)
	return(t1,t2)

def Crossover(ind1,ind2) :
	newInd = {}
	newInd["White"] = []
	newInd["Positions"] = []
	for i in range(0,len(ind1['White'])):
		rn = random.SystemRandom().randint(0,1)
		if(rn == 0):
			newInd["White"].append(ind1['White'][i])
			newInd["Positions"].append(ind1['Positions'][i])
		else :
			newInd["White"].append(ind2['White'][i])
			newInd["Positions"].append(ind2['Positions'][i])
	newInd['Cost'] = countThreat1(newInd['White'])
	return(newInd)

def Mutation(ind) :
	mutate = numpy.random.choice([True,False],p = [0.3,0.7])
	if mutate :
		indTemp = copy.deepcopy(ind)
		rn = random.SystemRandom().randint(0,len(indTemp['White'])-1)
		tupExist = True
		while tupExist :
			t1 = random.SystemRandom().randint(0,7)
			t2 = random.SystemRandom().randint(0,7)
			tupExist = (t1,t2) in ind['Positions']
		indTemp['White'][rn].position = (t1,t2)
		indTemp['Positions'][rn] = (t1,t2)
		indTemp['Cost'] = countThreat1(indTemp['White'])
		return(indTemp)
	else :
		return ind

def GenAlgoLvl2(population):
	if(len(population) > 977):
		minVal  = population[0]
		for x in population :
			if (minVal['Cost'] > x['Cost']) :
				minVal = x
		return(minVal)
	else :
		return(GenAlgoLvl2(population + [Mutation(Crossover(*Selection(population)))]))

def GeneticAlgo1(takenPos,whiteList):
	obj = {}
	obj['Positions'] = takenPos
	obj['White'] = whiteList
	obj['Cost'] = countThreat1(whiteList)
	population = [obj]
	for i in range(0,3):
		tempWhite = copy.deepcopy(whiteList)
		tempPos = copy.deepcopy(takenPos)
		for j in range(0,len(whiteList)):
			loc = (random.SystemRandom().randint(0,7),random.SystemRandom().randint(0,7))
			tempWhite[j].position = loc
			tempPos[j] = loc
		obj['Positions'] = tempPos
		obj['White'] = tempWhite
		obj['Cost'] = countThreat1(tempWhite)
		population.append(obj.copy())
	population.sort(key = lambda i : i['Cost'])
	return(GenAlgoLvl2(population))

#Return two breed from population to mate
def Selection2(population):
	probList = []
	pops = copy.copy(population)
	maxThreat = max(item['Cost'] for item in population)
	#print(maxThreat)
	sumEn = sum((maxThreat - item['Cost']) for item in population)

	for x in population :
		prob = (maxThreat - x['Cost'])/sumEn
		probList.append(prob)
	t1 = numpy.random.choice(population,p = probList)
	
	pops.remove(t1)
	sumEn = sum((maxThreat - item['Cost']) for item in pops)
	probList = []
	for x in pops :
		prob = (maxThreat - x['Cost'])/sumEn
		probList.append(prob)
	t2 = numpy.random.choice(pops,p =probList)
	#print('selecting')
	
	#print('Selection')
	#print(t1['Positions'])
	#print(t2['Positions'])
	return(t1,t2)

def Crossover2(ind1,ind2) :
	#Making intialization of new breed
	newInd = {}
	newInd["White"] = []
	newInd["Black"] = []
	newInd["Positions"] = []

	for i in range(0,len(ind1['White'])):
		rn = random.SystemRandom().randint(0,1)
		if(rn == 0):
			if (ind1['White'][i] not in newInd['Positions']):
				newInd["White"].append(ind1['White'][i])
				newInd["Positions"].append(ind1['Positions'][i])
			else:
				newInd["White"].append(ind2['White'][i])
				newInd["Positions"].append(ind2['Positions'][i])
		else :
			if (ind2['White'][i] not in newInd['Positions']):
				newInd["White"].append(ind2['White'][i])
				newInd["Positions"].append(ind2['Positions'][i])
			else:
				newInd["White"].append(ind1['White'][i])
				newInd["Positions"].append(ind1['Positions'][i])


	for i in range(0,len(ind1['Black'])):
		rn = random.SystemRandom().randint(0,1)
		if(rn == 0):
			if (ind1['Black'][i] not in newInd['Positions']):
				newInd["Black"].append(ind1['Black'][i])
				newInd["Positions"].append(ind1['Positions'][i+len(newInd['White'])])
			else:
				newInd["Black"].append(ind2['Black'][i])
				newInd["Positions"].append(ind2['Positions'][i+len(newInd['White'])])
		else :
			if (ind2['Black'][i] not in newInd['Positions']):
				newInd["Black"].append(ind2['Black'][i])
				newInd["Positions"].append(ind2['Positions'][i+len(newInd['White'])])
			else:
				newInd["Black"].append(ind1['Black'][i])
				newInd["Positions"].append(ind1['Positions'][i+len(newInd['White'])])

	newInd['Cost'] = countThreat1(newInd['White']) + countThreat1(newInd['Black']) - countThreat2(newInd['White'],newInd['Black'])
	#print('cross-overing')
	#print ('Indice 1')
	#print (ind1['Positions'])
	#print ('Indice 2')
	#print (ind2['Positions'])
	#print ('New Indice')
	#print (len(newInd['Positions']))
	#print (newInd['Positions'])
	return(newInd)

def Mutation2(ind) :
	mutate = numpy.random.choice([True,False],p = [0.3,0.7])
	#print('mutating')
	if mutate :
		indTemp = copy.deepcopy(ind)
		rnWhite = random.SystemRandom().randint(0,len(indTemp['White'])-1)
		rnBlack = random.SystemRandom().randint(0,len(indTemp['Black'])-1)

		tupExist = True
		while tupExist :
			t1 = random.SystemRandom().randint(0,7)
			t2 = random.SystemRandom().randint(0,7)
			tupExist = (t1,t2) in ind['Positions'] or (t1,t2) in indTemp['Positions']
		indTemp['White'][rnWhite].position = (t1,t2)
		indTemp['Positions'][rnWhite] = (t1,t2)

		tupExist = True
		while tupExist :
			t1 = random.SystemRandom().randint(0,7)
			t2 = random.SystemRandom().randint(0,7)
			tupExist = (t1,t2) in ind['Positions'] or (t1,t2) in indTemp['Positions']
		indTemp['Black'][rnBlack].position = (t1,t2)
		indTemp['Positions'][rnBlack+len(indTemp['White'])] = (t1,t2)

		indTemp['Cost'] = countThreat1(indTemp['White']) + countThreat1(indTemp['Black']) - countThreat2(indTemp['White'], indTemp['Black'])
		#print('mutating 1')
		#print (len(indTemp['Positions']))
		return(indTemp)
	else :
		#print('mutating2')
		#print (len(ind['Positions']))
		return ind

def GenAlgoLvl22(population):

	if(len(population) > 900): #Enough population has been made, return the minimum value
		minVal  = population[0]
		for x in population :
			if (minVal['Cost'] > x['Cost']) and len(set(x['Positions'])) == len(x['Positions']):
				minVal = x
				'''
		print(minVal['Positions'])
		print('White')
		for w in minVal['White']:
			print(w.position)
		print('Black')
		for b in minVal['Black']:
			print(b.position)
			'''
		return(minVal)	
	else : 
		#print('computing')
		return(GenAlgoLvl22(population + [Mutation2(Crossover2(*Selection2(population)))]))

def GeneticAlgo2(takenPos,whiteList,blackList):
	#Making Population Object
	obj = {}
	obj['Positions'] = takenPos
	obj['White'] = whiteList
	obj['Black'] = blackList
	obj['Cost'] = countThreat1(whiteList) + countThreat1(blackList) - countThreat2(whiteList,blackList)
	population = [obj]

	#Making new population
	for i in range(0,10):
		tempWhite = copy.deepcopy(whiteList)
		tempBlack = copy.deepcopy(blackList)
		tempPos = copy.deepcopy(takenPos)

		#Making new White List
		for j in range(0,len(whiteList)):
			loc = (random.SystemRandom().randint(0,7),random.SystemRandom().randint(0,7))
			while loc in tempPos:
				loc = (random.SystemRandom().randint(0,7),random.SystemRandom().randint(0,7))
			tempWhite[j].position = loc
			tempPos[j] = loc

		#Making new Black List
		for j in range(0,len(blackList)):
			loc = (random.SystemRandom().randint(0,7),random.SystemRandom().randint(0,7))
			while loc in tempPos:
				loc = (random.SystemRandom().randint(0,7),random.SystemRandom().randint(0,7))
			tempBlack[j].position = loc
			tempPos[j+len(whiteList)] = loc
		'''
		print(tempPos)
		for w in tempWhite:
			print(w.type)
			print(w.position)
		for b in tempBlack:
			print(b.type)
			print(b.position)
		''' 	
		#Completing new population and adding it to population list
		obj['Positions'] = tempPos
		obj['White'] = tempWhite
		obj['Black'] = tempBlack
		obj['Cost'] = countThreat1(tempWhite) + countThreat1(tempBlack) + countThreat2(tempWhite,tempBlack)
		population.append(obj.copy())

	population.sort(key = lambda i : i['Cost'])
#print(population)
	return(GenAlgoLvl22(population))

method = input("Enter the method you want : ")
#MAIN PROGRAM
if (method.lower() == "sa"):
	if (objListB == []):
		res = simulatedAnne1(takenPos,objListW,0.95)
		displayPapan(res['Positions'],res['White'],[])
		print(res['Cost'])
	else :
		res = simulatedAnne2(takenPos,objListW,objListB,0.95)
		displayPapan(res['Positions'],res['White'],res['Black'])
		print(res['Cost'])
elif(method.lower() == "ga"):
	if (objListB == []):
		res = GeneticAlgo1(takenPos,objListW)
		displayPapan(res['Positions'],res['White'],[])
		print(res['Cost'])
	else :
		res = GeneticAlgo2(takenPos,objListW,objListB)
		displayPapan(res['Positions'],res['White'],res['Black'])
		print(res['Cost'])
elif(method.lower() == "hc"):
	if (objListB == []) :
		hillClimbS1(takenPos,objListW)
	elif (objListW == []) :
		hillClimbS1(takenPos,objListB)
	else :
		hillClimbS2(takenPos,objListW,objListB)	
else : # by default use hill climbing (bonus)
	hillClimbS2(takenPos,objListW,objListB)
