import random
import math

#class randomMazeGenerator(object):
mazeProperty={1:0.8, 2:0.55}
hprx={-1:[-2,0], 0:[0,0], 1:[2,0]}
hprz={-3:[-6,4], -2:[-3,4], -1:[-3,0], 0:[0,0], 1:[3,0]}
ends1=[(0,-7,0),(-4.84,0,4)]
ends2=[(0,7,0),(-4.84,0,4)]

def placeFrame(level):
	scale=mazeProperty[level]
	size=6
	angle=-37
	triPos=[]
	x=random.randint(-1,1)
	z=random.randint(-3,1)
	rotation=90
	h,p,r=angle+hprx[x][0]+hprz[z][0]+rotation,hprx[x][1]+hprz[z][1],0
	return (x,0,z,h,p,r,scale,size)

def placeExtraTri(triEnds):
	(fx,fy,fz)=random.choice(triEnds)
	i=triEnds.index((fx,fy,fz))
	triEnds.pop(i)
	(dx,dy,dz)=random.choice(ends2)
	for j in ends2:
		if (dx,dy,dz)!=j:
			(endx,endy,endz)=j
	x1,y1,z1=ends2[0]
	x2,y2,z2=ends2[1]
	y1*=-1
	if distance(fx,fy,fz,x1,y1,z1)<distance(fx,fy,fz,x2,y2,z2) and (dx,dy,dz)==(0,7,0):
		triEnds.append((fx,fy,fz))
		return placeExtraTri(triEnds)
	else:
		x=fx-dy
		y=fy-dx
		z=fz-dz
	triEnds.append((x+endy,y+endx,z+endz))
	h=90
	p,r=0,0
	return (x,y,z,h,p,r,i)

def distance(x1,y1,z1,x2,y2,z2):
	return math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

def getPath(size, cx, cy, cz):
	pos1,pos2=[(0,-7,0)],[(-4.84,0,4)]
	length2=random.randint(size/3, size/2)
	length1=size-length2
	while len(pos1)<=length1:
		pos1=paveWay(pos1,cx,cy,cz,"x")
	while len(pos2)<=length2:
		pos2=paveWay(pos2,cx,cy,cz,"y")
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

def isValid(tmp, cx, cy, cz):

	x,y,z=tmp
	if (y==0 or y==1) and x>-4.84:
		return False
	elif x==0 and y>=-8 and z==-1:
		return False
	return True

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
		return (x1,y1,z1)
	elif (x2-x1==1 and y2-y1==0 and z2-z1==-1) or (x2-x1==0 and y2-y1==1 and z2-z1==-1):
		return (x1,y1,z1)
	return None

def getStart(fx,fy,fz):
	dx,dy=random.choice([(1,0),(0,1)])
	dz=0.1
	return (fx+dx,fy+dy,fz-dz)

def getEnd(fx,fy,fz):
	dx=random.choice([1,-1])
	dy,dz=-0.5,-0.5
	h=90
	return (fx+dx,fy+dy,fz+dz,h)

def getBound(pos):
	xmax,ymax,zmax=0,0,0
	xmin,ymin,zmin=0,0,0
	for i in range(len(pos)):
		x,y,z=pos[i]
		if x>xmax:
			xmax=x
		elif x<xmin:
			xmin=x
		if y>ymax:
			ymax=y
		elif y<ymin:
			ymin=y
		if z>zmax:
			zmax=z
		elif z<zmin:
			zmin=z
	return (xmax,ymax,zmax,xmin,ymin,zmin)
