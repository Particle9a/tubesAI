import random
import copy
import os
import numpy
from hillclimbing import findBetterState
from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, displayPapan, countThreat1, countThreat2, printThreat1, printThreat2

# SIMULATED ANNEALING ALGORITHM
def simulatedAnnealing(takenPos,whiteList,blackList) :
	minState = {}
	minState['Positions'] = copy.deepcopy(takenPos)
	minState['White'] = copy.deepcopy(whiteList)
	minState['Black'] = copy.deepcopy(blackList)
	minState['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
	temperature = 100
	while (temperature > 0):
		tempState = findBetterState(minState['Positions'], minState['White'], minState['Black'])
		if (tempState['Cost'] < minState['Cost']):
			minState = copy.deepcopy(tempState)
		else:
			probFactor = numpy.exp((minState['Cost']-tempState['Cost'])/temperature)
			change = numpy.random.choice([True,False], p = [probFactor,1-probFactor])
			if (change):
				minState = copy.deepcopy(tempState)
		temperature = temperature - 2
	return minState
