# Class for chess piece
class Pion :
	def __init__(self, t, x,y) :
		self.type = t
		self.position = (x,y)

	def isThreatenedBy(self,obj,listPos) :
		if (obj.type == 'QUEEN'):
			if (isVAligned(self.position, obj.position)):
				if(not isBlockedV(self.position,obj.position,listPos)):
					return(True)
			elif (isHAligned(self.position, obj.position)):
				if(not isBlockedH(self.position,obj.position,listPos)):
					return(True)
			elif (isDAligned(self.position, obj.position)):
				if(not isBlockedD(self.position,obj.position, listPos)):
					return(True)
		elif (obj.type == 'ROOK'):
			if (isVAligned(self.position, obj.position)):
				if(not isBlockedV(self.position,obj.position,listPos)):
					return(True)
			elif (isHAligned(self.position, obj.position)):
				if(not isBlockedH(self.position,obj.position,listPos)):
					return(True)
		elif (obj.type == 'BISHOP'):
			if (isDAligned(self.position, obj.position)):
				if(not isBlockedD(self.position,obj.position, listPos)):
					return(True)
		elif (obj.type == 'KNIGHT'):
			if (isHorseAligned(self.position,obj.position)):
				return(True)
		return(False)

# Return true if two chess piece are aligned horizontally or vertically
def isHAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	if (x1 == x2):
		return(True)
	return(False)

def isVAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	if (y1 == y2):
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
	elif ((x1 + y1) == (x2 + y2)):
		return True
	return False

def isBlockedV(pos1,pos2,listpos):
	x1,y1 = pos1
	x2,y2 = pos2
	xTemp = x1
	if x2 > x1 :
		xTemp += 1
	else :
		xTemp -= 1
	while(xTemp != x2):
		if ((xTemp,y1) in listpos):
			return True
		if x2 > x1 :
			xTemp += 1
		else :
			xTemp -= 1
		if xTemp < 0 :
			return False
		elif xTemp > 7 :
			return False 
	return False

def isBlockedH(pos1,pos2,listpos):
	x1,y1 = pos1
	x2,y2 = pos2
	yTemp = y1
	if y2 > y1 :
		yTemp += 1
	else :
		yTemp -= 1
	while(yTemp != y2):
		if ((x1,yTemp) in listpos):
			return True
		if y2 > y1 :
			yTemp += 1
		else :
			yTemp -= 1
		if yTemp < 0 :
			return False
		elif yTemp > 7 :
			return False 
	return False

def isBlockedD(pos1,pos2,listpos):
	x1,y1 = pos1
	x2,y2 = pos2
	xTemp = x1
	yTemp = y1
	
	if x2 > x1 :
		xTemp += 1
	else :
		xTemp -= 1
	if y2 > y1 :
		yTemp += 1
	else :
		yTemp -= 1
	while(xTemp != x2):
		if ((xTemp,yTemp) in listpos):
			return True
		if x2 > x1 :
			xTemp += 1
		else :
			xTemp -= 1
		if y2 > y1 :
			yTemp += 1
		else :
			yTemp -= 1
		if yTemp < 0 :
			return False
		elif yTemp > 7 :
			return False 
	return False

# Return true if horse threats other piece
def isHorseAligned(pos1,pos2):
	x1,y1 = pos1
	x2,y2 = pos2
	c1 = abs(x1-x2)
	c2 = abs(y1-y2)
	if ((c1 == 1) and (c2 == 2)):
		return(True)
	elif ((c1 == 2) and (c2 == 1)):
		return(True)
	return(False)

# DISPLAY FUNCTION 
def displayPapan(takenPos, whiteList, blackList) :
	for i in range(0,8):
		string = ''
		for j in range(0,8):
			if ((i,j) not in takenPos): # Koordinat dibalik
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
	
	
	samePieceConflict = str(countThreat1(whiteList,takenPos)+countThreat1(blackList,takenPos))
	diffPieceConflict = str(countThreat2(whiteList,blackList,takenPos))

	print(samePieceConflict + " " + diffPieceConflict)

# THREAT (ENERGY) Counter
def countThreat1(whiteList,listPos):
	count = 0
	for x in whiteList :
		for y in whiteList :
			if (x != y) :
				if x.isThreatenedBy(y,listPos) :
					count += 1
	return count

def countThreat2(whiteList,blackList,listPos):
	count = 0
	for x in whiteList :
		for y in blackList :
			if x.isThreatenedBy(y,listPos) :
				count += 1
			if y.isThreatenedBy(x,listPos) :
				count += 1
	return count

# THREAT POSISITION
def printThreat1(whiteList,listPos):
	for x in whiteList :
		for y in whiteList :
			if (x != y) :
				if x.isThreatenedBy(y,listPos) :
					print(y.position,"attack", x.position)

def printThreat2(whiteList,blackList,listPos):
	for x in whiteList:
		for y in blackList:
			if x.isThreatenedBy(y,listPos):
				print(y.position, "attack", x.position)
			if y.isThreatenedBy(x,listPos):
				print(x.position, "attack", y.position)