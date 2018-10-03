import random
import copy
import os
import numpy
from hillclimbing import findBetterState
from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, displayPapan, countThreat1, countThreat2, printThreat1, printThreat2

def randomize(takenPos,whiteList,blackList):
	result = {}
	result['Positions'] = []
	result['White'] = copy.deepcopy(whiteList)
	result['Black'] = copy.deepcopy(blackList)
	for x in range(0,len(whiteList)):
		posX = random.randint(0,7)
		posY = random.randint(0,7)
		while ((posX,posY) in result['Positions']):
			posX = random.randint(0,7)
			posY = random.randint(0,7)
		result['Positions'].append((posX,posY))
		result['White'][x].position = (posX,posY)
	for x in range(0,len(blackList)):
		posX = random.randint(0,7)
		posY = random.randint(0,7)
		while ((posX,posY) in result['Positions']):
			posX = random.randint(0,7)
			posY = random.randint(0,7)
		result['Positions'].append((posX,posY))
		result['Black'][x].position = (posX,posY)
	result['Cost'] = countThreat1(result['White'],result['Positions']) + countThreat1(result['Black'],result['Positions']) - countThreat2(result['White'],result['Black'],result['Positions'])
	return result

# SIMULATED ANNEALING ALGORITHM
def simulatedAnnealing(takenPos,whiteList,blackList) :
	minState = {}
	minState['Positions'] = copy.deepcopy(takenPos)
	minState['White'] = copy.deepcopy(whiteList)
	minState['Black'] = copy.deepcopy(blackList)
	minState['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
	temperature = 1000
	while (temperature > 0):
		tempState = randomize(minState['Positions'], minState['White'], minState['Black'])
		if (tempState['Cost'] < minState['Cost']):
			minState = copy.deepcopy(tempState)
		else:
			probFactor = numpy.exp((minState['Cost']-tempState['Cost'])/temperature)
			change = numpy.random.choice([True,False], p = [probFactor,1-probFactor])
			if (change):
				minState = copy.deepcopy(tempState)
		temperature = temperature - 1
	return minState
