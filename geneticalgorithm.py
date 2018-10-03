import random
import copy
import os
import numpy

from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, displayPapan, countThreat1, countThreat2

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
				if (sumEn!=0):
					prob = (maxThreat - x['Cost'])/sumEn
				else :
					prob = 1/len(population)
				probList.append(prob)

			#Choose tuple according to probability
			t1 = numpy.random.choice(population,p = probList)
			pops.remove(t1)
			
			#Making Probability List
			sumEn = sum((maxThreat - item['Cost']) for item in pops)
			probList = []
			for x in pops :
				if (sumEn!=0):
					prob = (maxThreat - x['Cost'])/sumEn
				else :
					prob = 1/len(pops)
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
			mutate = numpy.random.choice([True,False],p = [0.05,0.95]) #Randomizer to decide to mutate or not
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

def generatePopulation(takenPos,whiteList,blackList):
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
	return population

def geneticAlgorithm(takenPos,whiteList,blackList):
	#Make population
	population = generatePopulation(takenPos,whiteList,blackList)

	#Process
	for i in range(100):
		newPopulation = Mutation(Crossover(Selection(population)))

		population.sort(key = lambda i : i['Cost'])
		newPopulation.sort(key = lambda i : i['Cost'])
		population[31] = newPopulation[0].copy()	

	#Choose the best breed
	minVal  = population[0]
	for x in population :
		if (minVal['Cost'] > x['Cost']) and len(set(x['Positions'])) == len(x['Positions']): #If the cost of x is less than min value, assign x as new minValue
			minVal = x

	return minVal	