import random
import copy
import os
import numpy

from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, Pion, displayPapan, countThreat1, countThreat2, printThreat1, printThreat2

# HILL CLIMBING ALGORITHM
def findBetterState(takenPos, whiteList,blackList):
	# Initialize minState from 
	minState = {}
	minState['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
	minState['White'] = whiteList
	minState['Black'] = blackList

	# Iteration in white pion list to find a better assignment
	for x in range(0,len(whiteList)) :
		# Iterate a and b to find new position
		for a in range(0,8):
			for b in range(0,8):
				if ((a,b) not in takenPos):
					# Make new temporary variable of position and white pion list, with position that haven't been taken
					tempPos = copy.deepcopy(takenPos)
					tempWhite = copy.deepcopy(whiteList)
					tempWhite[x].position = (a,b)
					tempPos[x] = (a,b)
					
					# Count threats from the new position
					tempV = countThreat1(tempWhite,takenPos) + countThreat1(blackList,takenPos) - countThreat2(tempWhite,blackList,takenPos)
				
					# If the threat cost is less than the current minState, assign new minState with the temporary variables
					if (tempV < minState['Cost']):
						minState['Cost'] = tempV
						minState['Positions'] = tempPos
						minState['White'] = tempWhite

	# Iteration in black pion list to find a better assignment
	for x in range(0,len(blackList)) :
		# Iterate a and b to find new position
		for a in range(0,8):
			for b in range(0,8):
				if ((a,b) not in takenPos):
					# Make new temporary variable of position and black pion list, with position that haven't been taken
					tempPos = copy.deepcopy(takenPos)
					tempBlack = copy.deepcopy(blackList)
					tempBlack[x].position = (a,b)
					tempPos[x + len(whiteList)] = (a,b)
					
					# Count threats from the new position
					tempV = countThreat1(tempWhite,takenPos) + countThreat1(tempBlack,takenPos) - countThreat2(whiteList, tempBlack,takenPos)
					
					# If the threat cost is less than the current minState, assign new minState with the temporary variables
					if (tempV < minState['Cost']):
						minState['Cost'] = tempV
						minState['Positions'] = tempPos
						minState['Black'] = tempBlack
	return(minState)

def hillClimbing(takenPos,whiteList,blackList) :
	# Initialize minState
	minState = {}
	minState['Positions'] = copy.deepcopy(takenPos)
	minState['White'] = copy.deepcopy(whiteList)
	minState['Black'] = copy.deepcopy(blackList)
	minState['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
	
	# If there is better state, algorithm keep finding a better state
	betterExist = True
	while betterExist :
		tempState = findBetterState(minState['Positions'], minState['White'], minState['Black'])
		if (tempState['Cost'] < minState['Cost']):
			minState = tempState
		else : 
			betterExist = False
	return minState

# SIMULATED ANNEALING ALGORITHM
def simulatedAnne1(takenPos,whiteList,temperature):
	minState = {}
	minState['White'] = whiteList
	minState['Positions'] = takenPos
	minState['Cost'] = countThreat1(whiteList,takenPos)	
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
			if (countThreat1(tempWhite,takenPos) < countThreat1(whiteList,takenPos)):
				minState = simulatedAnne1(tempPos,tempWhite,temperature-0.005)
				return(minState)
			elif (countThreat1(tempWhite,takenPos) == countThreat1(whiteList,takenPos)):
				change = numpy.random.choice([True,False], p =[temperature,1-temperature])
				if change :
					minState = simulatedAnne1(tempPos,tempWhite,temperature-0.005)
					return(minState)
				else :
					continue
			else :
				probFactor = temperature*1/(countThreat1(tempWhite,takenPos)-countThreat1(whiteList,takenPos))
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
	minState['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
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
		tempV = countThreat1(tempWhite,takenPos) + countThreat1(tempBlack,takenPos) - countThreat2(tempWhite,tempBlack,takenPos)
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
#Return two breed from population to mate
def Selection(population):
	#Create list for pair to mate
	tupSelection = []
	for k in range(len(population)//2):
		tupExist = True
		while tupExist:
			pops = copy.copy(population) #Make population copy to remove first tuple so tuple didnt mate with 
			maxThreat = max(item['Cost'] for item in population) #Max conflict
			

			#Making Probability List
			sumEn = sum((maxThreat - item['Cost']) for item in population) #Sum of delta of conflict 
			probList = []
			for x in population :
				prob = (maxThreat - x['Cost'])/sumEn
				probList.append(prob)

			#Choose tuple according to probability
			t1 = numpy.random.choice(population,p = probList)
			pops.remove(t1)
			
			#Making Probability List
			sumEn = sum((maxThreat - item['Cost']) for item in pops)
			probList = []
			for x in pops :
				prob = (maxThreat - x['Cost'])/sumEn
				probList.append(prob)

			#Choose tuple
			t2 = numpy.random.choice(pops,p =probList)
			tup = (t1,t2)

			#Append tuple to list pair to mate if it hasn't exist
			if tup not in tupSelection:
				tupExist = False
				tupSelection.append(tup)
	return tupSelection

def Crossover(ind) :
	#Make list of new breed
	newInd = []
	for tup in ind:
		#Making intialization of new breed
		newInd1 = {}
		newInd1["White"] = []
		newInd1["Black"] = []
		newInd1["Positions"] = []

		newInd2 = {}
		newInd2["White"] = []
		newInd2["Black"] = []
		newInd2["Positions"] = []	

		#Crossovering White Piece Postition
		for i in range(0,len(tup[0]['White'])):
			rn = random.SystemRandom().randint(0,1) #Randomizing which one of the parent to copy the position
			if(rn == 0):
				if (tup[0]['White'][i] not in newInd1['Positions']): #Validation to prevent duplicate
					newInd1["White"].append(tup[0]['White'][i])
					newInd1["Positions"].append(tup[0]['Positions'][i])

					newInd2["White"].append(tup[1]['White'][i])
					newInd2["Positions"].append(tup[1]['Positions'][i])					
				else:
					newInd1["White"].append(tup[1]['White'][i])
					newInd1["Positions"].append(tup[1]['Positions'][i])

					newInd2["White"].append(tup[0]['White'][i])
					newInd2["Positions"].append(tup[0]['Positions'][i])
			else :
				if (tup[1]['White'][i] not in newInd1['Positions']):
					newInd1["White"].append(tup[1]['White'][i])
					newInd1["Positions"].append(tup[1]['Positions'][i])

					newInd2["White"].append(tup[0]['White'][i])
					newInd2["Positions"].append(tup[0]['Positions'][i])
				else:
					newInd1["White"].append(tup[0]['White'][i])
					newInd1["Positions"].append(tup[0]['Positions'][i])

					newInd2["White"].append(tup[1]['White'][i])
					newInd2["Positions"].append(tup[1]['Positions'][i])

		#Crossovering Black Piece Postition
		for i in range(0,len(tup[0]['Black'])):
			rn = random.SystemRandom().randint(0,1)
			if(rn == 0):
				if (tup[0]['Black'][i] not in newInd1['Positions']):
					newInd1["Black"].append(tup[0]['Black'][i])
					newInd1["Positions"].append(tup[0]['Positions'][i+len(newInd1['White'])])

					newInd2["Black"].append(tup[1]['Black'][i])
					newInd2["Positions"].append(tup[1]['Positions'][i+len(newInd2['White'])])
				else:
					newInd1["Black"].append(tup[1]['Black'][i])
					newInd1["Positions"].append(tup[1]['Positions'][i+len(newInd1['White'])])

					newInd2["Black"].append(tup[0]['Black'][i])
					newInd2["Positions"].append(tup[0]['Positions'][i+len(newInd2['White'])])
			else :
				if (tup[1]['Black'][i] not in newInd1['Positions']):
					newInd1["Black"].append(tup[1]['Black'][i])
					newInd1["Positions"].append(tup[1]['Positions'][i+len(newInd1['White'])])

					newInd2["Black"].append(tup[0]['Black'][i])
					newInd2["Positions"].append(tup[0]['Positions'][i+len(newInd2['White'])])
				else:
					newInd1["Black"].append(tup[0]['Black'][i])
					newInd1["Positions"].append(tup[0]['Positions'][i+len(newInd1['White'])])

					newInd2["Black"].append(tup[1]['Black'][i])
					newInd2["Positions"].append(tup[1]['Positions'][i+len(newInd2['White'])])

		#Calculating the new cost
		newInd1['Cost'] = countThreat1(newInd1['White'],newInd1['Positions']) + countThreat1(newInd1['Black'],newInd1['Positions']) - countThreat2(newInd1['White'],newInd1['Black'],newInd1['Positions'])
		newInd2['Cost'] = countThreat1(newInd2['White'],newInd2['Positions']) + countThreat1(newInd2['Black'],newInd2['Positions']) - countThreat2(newInd2['White'],newInd2['Black'],newInd2['Positions'])

		newInd.append(newInd1)
		newInd.append(newInd2)
	return(newInd)

def Mutation(ind) :
	#making list of mutated breed
	mutationList = []
	#print('mutating')

	for item in ind :
		#Create copy of breed to edit
		indTemp = copy.deepcopy(item)

		#Iterating over each piece position
		for i in range(len(item['Positions'])):
			mutate = numpy.random.choice([True,False],p = [0.1,0.9]) #Randomizer to decide to mutate or not
			if mutate or indTemp['Positions'].count(indTemp['Positions'][i]) > 1: #Mutate the piece position according to randomizer above OR if it has duplicate on the list

				#Creating mutated position
				tupExist = True
				while tupExist :
					t1 = random.SystemRandom().randint(0,7)
					t2 = random.SystemRandom().randint(0,7)
					tupExist = (t1,t2) in item['Positions'] or (t1,t2) in indTemp['Positions']
				
				#Assigning the mutated positon
				indTemp['Positions'][i] = (t1,t2)
				if (i < len(item['White'])):
					indTemp['White'][i].position = (t1,t2)
				else:
					indTemp['Black'][i-len(item['White'])].position= (t1,t2)

		#Re-calculate cost
		indTemp['Cost'] = countThreat1(indTemp['White'],indTemp['Positions']) + countThreat1(indTemp['Black'],indTemp['Positions']) - countThreat2(indTemp['White'], indTemp['Black'],indTemp['Positions'])
		mutationList.append(indTemp.copy())
	return mutationList

def GeneratePopulation(takenPos,whiteList,blackList):
	#Making Population Object
	obj = {}
	obj['Positions'] = takenPos
	obj['White'] = whiteList
	obj['Black'] = blackList
	obj['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
	population = [obj]

	#Making new state
	for i in range(31):
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

		#Completing new population and adding it to population list
		obj['Positions'] = tempPos
		obj['White'] = tempWhite
		obj['Black'] = tempBlack
		obj['Cost'] = countThreat1(tempWhite,takenPos) + countThreat1(tempBlack,takenPos) + countThreat2(tempWhite,tempBlack,takenPos)
		population.append(obj.copy())

	population.sort(key = lambda i : i['Cost'])
	return population

def GeneticAlgorithm(takenPos,whiteList,blackList):
	#Make population
	population = GeneratePopulation(takenPos,whiteList,blackList)

	#Process
	for i in range(111):
		population = Mutation(Crossover(Selection(population)))

	#Choose the best breed
	minVal  = population[0]
	for x in population :
		if (minVal['Cost'] > x['Cost']) and len(set(x['Positions'])) == len(x['Positions']): #If the cost of x is less than min value, assign x as new minValue
			minVal = x

	return minVal	


#MAIN PROGRAM
print('.__   __.      ____    ____ .___________. __    __   __  .__   __.   _______    ')
print('|  \ |  |      \   \  /   / |           ||  |  |  | |  | |  \ |  |  /  _____|   ')
print('|   \|  |  _____\   \/   /  `---|  |----`|  |__|  | |  | |   \|  | |  |  __     ')
print('|  . `  | |______\_    _/       |  |     |   __   | |  | |  . `  | |  | |_ |    ')
print('|  |\   |          |  |         |  |     |  |  |  | |  | |  |\   | |  |__| |    ')
print('|__| \__|          |__|         |__|     |__|  |__| |__| |__| \__|  \______|    ')
print('                                                                                ')
print('.______   .______        ______   .______    __       _______ .___  ___.        ')
print('|   _  \  |   _  \      /  __  \  |   _  \  |  |     |   ____||   \/   |        ')
print('|  |_)  | |  |_)  |    |  |  |  | |  |_)  | |  |     |  |__   |  \  /  |        ')
print('|   ___/  |      /     |  |  |  | |   _  <  |  |     |   __|  |  |\/|  |        ')
print('|  |      |  |\  \----.|  `--\'  | |  |_)  | |  `----.|  |____ |  |  |  |        ')
print('| _|      | _| `._____| \______/  |______/  |_______||_______||__|  |__|        ')
print('\nby:Liebe Dich')

# Initialization for, position taken by piece, list of white piece and list of black piece
takenPos = []
objListW = []
objListB = []

filename = input("\nEnter the input file name : ")
# Reading file, and assign the piece to list initialized before
fil = open(filename)
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

print('File loaded successfully!\n')
print('== Method List ==')
print('1.Hill Climbing')
print('2.Simulated Annealing')
print('3.Genetic Algorithm\n')

#Algorithm
method = input("Choose the local search method : ")
if (method == "1"):
	if (objListB == []):
		res = simulatedAnne1(takenPos,objListW,0.95)
		displayPapan(res['Positions'],res['White'],[])
	else :
		res = simulatedAnne2(takenPos,objListW,objListB,0.95)
		displayPapan(res['Positions'],res['White'],res['Black'])

elif(method == "2"):
	result = GeneticAlgorithm(takenPos,objListW,objListB)
	
elif(method() == "3"):
	result = hillClimbing(takenPos,objListW,objListB)

displayPapan(result['Positions'],result['White'],result['Black'])
