import random
import copy
import os
import numpy

from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, displayPapan, countThreat1, countThreat2, printThreat1, printThreat2

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