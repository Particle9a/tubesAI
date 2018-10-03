import random
import copy
import os
import numpy
from hillclimbing import findBetterState
from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, displayPapan, countThreat1, countThreat2

# SIMULATED ANNEALING ALGORITHM

# Main function of Simulated Annealing Algorithm
def simulatedAnnealing(takenPos,whiteList,blackList) :
	#Initialize minState
	minState = {}
	minState['Positions'] = copy.deepcopy(takenPos)
	minState['White'] = copy.deepcopy(whiteList)
	minState['Black'] = copy.deepcopy(blackList)
	minState['Cost'] = countThreat1(whiteList,takenPos) + countThreat1(blackList,takenPos) - countThreat2(whiteList,blackList,takenPos)
	#Initialize temperature
	temperature = 100
	while (temperature > 0):
		#Make a successor state
		tempState = findBetterState(minState['Positions'], minState['White'], minState['Black'])
		#Compare with current state
		if (tempState['Cost'] < minState['Cost']):
			minState = copy.deepcopy(tempState)
		else:
			probFactor = numpy.exp((minState['Cost']-tempState['Cost'])/temperature)
			change = numpy.random.choice([True,False], p = [probFactor,1-probFactor])
			if (change):
				minState = copy.deepcopy(tempState)
		#decrease temperature
		temperature = temperature - 1
	#temperature <= 0
	return minState
