import random
import copy
import os
import numpy

from chess import isHAligned, isVAligned, isDAligned, isBlockedV, isBlockedH, isBlockedD, isHorseAligned, displayPapan, countThreat1, countThreat2, printThreat1, printThreat2

# HILL CLIMBING ALGORITHM

# Find a better assignment to pions
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

# Return the minimum threat state
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