from hillclimbing import hillClimbing
from simulatedannealing import simulatedAnne1, simulatedAnne2
from geneticalgorithm import geneticAlgorithm
from chess import Pion, displayPapan
import random

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
	result = hillClimbing(takenPos,objListW,objListB)

elif(method == "2"):
	if (objListB == []):
		result = simulatedAnne1(takenPos,objListW,0.95)
	else :
		result = simulatedAnne2(takenPos,objListW,objListB,0.95)

elif(method == "3"):
	result = geneticAlgorithm(takenPos,objListW,objListB)

displayPapan(result['Positions'],result['White'],result['Black'])
