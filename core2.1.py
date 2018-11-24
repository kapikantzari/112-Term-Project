import random

def placeTri():
	angle=-37
	hprx={-1:[-2,0], 0:[0,0], 1:[2,0]}
	x=random.randint(-1,1)
	hprz={-4:[-6,8], -3:[-6,4], -2:[-3,4], -1:[-3,0], 0:[0,0], 1:[3,0], 2:[6,0]}
	z=random.randint(-4,2)
	rotation=90
	h,p,r=angle+hprx[x][0]+hprz[z][0]+rotation,hprx[x][1]+hprz[z][1],0
	return (x,0,z,h,p,r)

def getPath(size, cx, cy, cz):
	pos1,pos2=[(0,-7,0)],[(-4.84,0,4)]
	length2=random.randint(size/3, size/2)
	length1=size-length2
	while len(pos1)<=length1:
		pos1=paveWay(pos1, cx, cy, cz, "x")
	while len(pos2)<=length2:
		pos2=paveWay(pos2, cx, cy, cz, "y")
	return (pos1,pos2)

def paveWay(pos, cx, cy, cz, s):
	if s=="x":
		direction=[(1,0,0),(1,0,0),(1,0,0),(0,0,-1),(0,1,-1),(1,0,-1)]
	elif s=="y":
		direction=[(0,1,0),(0,1,0),(0,1,0),(0,0,-1),(0,1,-1),(1,0,-1)]
	dx,dy,dz=random.choice(direction)
	x,y,z=pos[-1]
	tmp=(x+dx,y+dy,z+dz)
	if isValid(tmp, cx, cy, cz):
		pos.append(tmp)
		return pos
	return pos

def checkLadder(pos):
	ladder=set()
	for i in range(len(pos)-2):
		tmp=ifLadder(pos, i)
		if tmp!=None:
			ladder.add(tmp)
	x2,y2,z2=pos[-1]
	x1,y1,z1=pos[-2]
	if (x2-x1==1 and y2-y1==0 and z2-z1==-1) or (x2-x1==0 and y2-y1==1 and z2-z1==-1) or (x2-x1==0 and y2-y1==0 and z2-z1==-1):
		ladder.add((x1,y1,z1))
	ladder.add((x2,y2,z2))
	return ladder

def ifLadder(pos, i):
	x1,y1,z1=pos[i]
	x2,y2,z2=pos[i+1]
	x3,y3,z3=pos[i+2]
	if x2-x1==0 and y2-y1==0 and z2-z1==-1:
		# if (x3-x2==1 and y3-y2==0 and z3-z2==0) or (x3-x2==0 and y3-y2==1 and z3-z2==0):
		return (x1,y1,z1)
	elif (x2-x1==1 and y2-y1==0 and z2-z1==-1) or (x2-x1==0 and y2-y1==1 and z2-z1==-1):
		return (x1,y1,z1)
	return None

def isValid(tmp, cx, cy, cz):
	x,y,z=tmp
	return -9<=x+cx<=4 and -7<=y+cy<=4 and -5<=z+cz<=10
