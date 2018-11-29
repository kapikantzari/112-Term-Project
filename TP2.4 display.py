#core imports
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from direct.interval.IntervalGlobal import *
import sys, math, os, random
from math import pi, sin, cos
from panda3d.core import loadPrcFileData 

import core

loadPrcFileData('', 'win-size 1200 800')
#Citation: https://stackoverflow.com/questions/15000460/how-to-change-the-window
#-size-in-panda3d

#for task managers
from direct.task import Task

class myDemo(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        #load all the things
        self.rotatingAngle1,self.rotatingAngle2=0,0
        self.rotatingAngle3,self.rotatingAngle4=0,0
        self.framex,self.framey,self.framez=0,0,0
        self.startingPoint=(0,0,0)
        self.endingPoint=(0,0,0)
        self.princessDir,self.princessDir2=0,0
        self.completed=False
        self.rotation,self.rotation2=0,0
        self.rotatingTri=0
        self.curr="start"
        self.success1,self.success2=False,False
        self.specialCase=0
        self.size=0
        self.level=2 #Change level to 2 to have 2 impossible triangle shapes

        self.blocks=[]
        self.path1,self.path2=[],[]
        self.triEnds=[]
        self.pathOrder=[]
        self.iconPos=[]
        self.ladders=set()
        
        self.loadModels()
        self.loadMaze()
        if self.level>1:
            self.loadExtraTri()
        self.loadLadder()
        self.loadStart()
        self.loadEnd()
        self.loadIcon()    
        self.loadBackground() # load lights and background

        self.accept("r", self.solve1)
        self.accept("z", self.solve2)
        self.accept("space", self.rotatePrincess)
        self.accept("arrow_up", self.nextEnd)
        
        # self.accept("arrow_down", self.toggleInterval, [self.rotationTri])
        
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        # Add the spinCameraTask procedure to the task manager.

        
        
    def loadBackground(self):
        #Citation: https://www.panda3d.org/manual/index.php/Lighting
        #add pointlight to each faces to illuminate the whole scene
        plight1=PointLight('plight')
        plight1.setColor(VBase4(0.5,0.5,0.5,0.5))
        plight1NodePath=render.attachNewNode(plight1)
        plight1NodePath.setPos(0,0,500)
        plight1NodePath.setHpr(170,0,0)
        render.setLight(plight1NodePath)

        plight2=PointLight('plight')
        plight2.setColor(VBase4(1, 1, 1, 1))
        plight2NodePath=render.attachNewNode(plight2)
        plight2NodePath.setPos(0,0,-500)
        plight2NodePath.setHpr(170,0,0)
        render.setLight(plight2NodePath)

        plight3=PointLight('plight')
        plight3.setColor(VBase4(0.5,0.5,0.5,0.5))
        plight3NodePath=render.attachNewNode(plight3)
        plight3NodePath.setPos(0, -500, 0)
        plight3NodePath.setHpr(170,0,0)
        render.setLight(plight3NodePath)

        plight4=PointLight('plight')
        plight4.setColor(VBase4(1, 1, 1, 1))
        plight4NodePath=render.attachNewNode(plight4)
        plight4NodePath.setPos(0, 500, 0)
        plight4NodePath.setHpr(170,0,0)
        render.setLight(plight4NodePath)

        plight5=PointLight('plight')
        plight5.setColor(VBase4(0.5,0.5,0.5,0.5))
        plight5NodePath=render.attachNewNode(plight5)
        plight5NodePath.setPos(500,0, 0)
        plight5NodePath.setHpr(170,0,0)
        render.setLight(plight5NodePath)

        plight6=PointLight('plight')
        plight6.setColor(VBase4(1, 1, 1, 1))
        plight6NodePath=render.attachNewNode(plight6)
        plight6NodePath.setPos(-500,0, 0)
        plight6NodePath.setHpr(170,0,0)
        render.setLight(plight6NodePath)

    def solve1(self):
        if self.check():
            solving1=Parallel()
            self.rotatingTri+=1
            angle=self.rotatingTri%4*90
            move1=self.tri1.hprInterval(2,Point3(self.rotatingAngle1-angle,self.rotatingAngle2,0))
            solving1.append(move1)
            if angle==90:
                self.success1=True
            else: self.success1=False
            if self.level==2:
                move2=self.extraTri.hprInterval(2,Point3(self.rotatingAngle3-angle,self.rotatingAngle4,0))
                solving1.append(move2)
                if angle==180:
                    self.success2=True
                else: self.success2=False
            solving1.start()  

    def solve2(self):
        if self.check():
            self.rotatingTri-=1
            move3=self.tri1.hprInterval(2,Point3(self.rotatingAngle1-90*self.rotatingTri,self.rotatingAngle2,0))
            move4=self.extraTri.hprInterval(2,Point3(self.rotatingAngle3-90*self.rotatingTri,self.rotatingAngle4,0))
            solving2=Parallel(move3,move4)
            solving2.start()
        
    def loadModels(self):
        ends=core.ends1
        (x,y,z,h,p,r,scale,self.size)=core.placeFrame(self.level)
        self.tri1=loader.loadModel("models2/tri1.egg")
        self.tri1.reparentTo(render)
        self.tri1.setScale(scale)
        self.tri1.setPos(x,y,z)
        self.tri1.setHpr(h,p,r)
        self.rotatingAngle1,self.rotatingAngle2=h,p
        self.pathOrder.append(self.tri1)
    
        self.frame=loader.loadModel("models2/tri1frame.egg")
        self.frame.reparentTo(render)
        self.frame.setScale(scale)
        self.frame.setPos(x,y,z)
        self.frame.setHpr(h,p,r)
        self.framex,self.framey,self.framez=x,y,z 

    def loadExtraTri(self):
        (x,y,z,h,p,r,i)=core.placeExtraTri(self.triEnds)
        self.extraTri=loader.loadModel("models2/extraTri.egg")
        self.extraTri.reparentTo(self.frame)
        self.extraTri.setPos(x,y,z)
        self.extraTri.setHpr(h,p,r)
        self.rotatingAngle3,self.rotatingAngle4=h,p
        if i==0:
            self.pathOrder.insert(0,self.extraTri)
        else:
            self.pathOrder.append(self.extraTri)
      
    def loadMaze(self):
        self.path1,self.path2=core.getPath(self.size,self.framex,self.framey,self.framez)
        self.pathOrder.insert(0,"path1")
        self.pathOrder.append("path2")
        x1,y1,z1=self.path1[-1]
        x2,y2,z2=self.path2[-1]
        x,y,z=self.frame.getPos()
        self.triEnds.append((x1,y1,z1))
        self.triEnds.append((x2,y2,z2))
        self.blocks=self.path1+self.path2
        self.ladders.update(core.checkLadder(self.path1))
        self.ladders.update(core.checkLadder(self.path2))
        for i in range(len(self.blocks)):
            x,y,z=self.blocks[i]
            h=-45
            self.block=loader.loadModel("models2/block.egg")
            self.block.reparentTo(self.frame)
            self.block.setPos(x,y,z)
            self.block.setHpr(h,0,0)

    def loadLadder(self):
        for i in self.triEnds:
            self.ladders.add(i)
        for j in self.ladders:
            (x,y,z)=j
            h=-45
            self.ladder=loader.loadModel("models2/ladder.egg")
            self.ladder.reparentTo(self.frame)
            self.ladder.setPos(x,y,z)
            self.ladder.setHpr(h,0,0)
        
    def loadStart(self):
        firstx,firsty,firstz=random.choice(self.triEnds)
        self.startingPoint=(firstx,firsty,firstz)
        i=self.triEnds.index(self.startingPoint)
        self.triEnds.pop(i)
        if i==0:
            self.pathOrder.insert(0,"start")
        else: self.pathOrder.append("start")
        sx,sy,sz=core.getStart(firstx,firsty,firstz)
        self.start=loader.loadModel("models2/start.egg")
        self.start.reparentTo(self.frame)
        self.start.setPos(sx,sy,sz)
        self.start.setHpr(0,0,0)

        self.princess=loader.loadModel("models2/princess.egg")
        self.princess.reparentTo(self.frame)
        self.princess.setHpr(self.princessDir,0,0)
        dz=0.185
        self.princess.setPos(sx,sy,sz-dz)

    def loadEnd(self):
        (lastx,lasty,lastz)=self.triEnds[-1]
        (x,y,z,h)=core.getEnd(lastx,lasty,lastz)
        self.endingPoint=(x,y,z)
        self.end=loader.loadModel("models2/end.egg")
        self.end.reparentTo(self.frame)
        self.end.setPos(x,y,z)
        self.end.setHpr(h,0,0)

    def loadIcon(self):
        self.icon1=loader.loadModel("models2/icon.egg")
        self.icon1.reparentTo(self.tri1)
        x1,y1,z1=core.ends1[1]
        dx1,dz1=4.84,0.5
        self.icon1.setPos(x1+dx1,y1,z1+dz1)
        self.iconPos.append((x1+dx1,y1,z1+dz1))
        
        self.icon2=loader.loadModel("models2/icon.egg")
        self.icon2.reparentTo(self.tri1)
        x2,y2,z2=core.ends1[0]
        dy2,dz2=5,0.5
        self.icon2.setPos(x2,y2+dy2,z2+dz2)
        self.iconPos.append((x2,y2+dy2,z2+dz2))

        if self.level==2:
            self.icon3=loader.loadModel("models2/icon.egg")
            self.icon3.reparentTo(self.extraTri)
            x3,y3,z3=core.ends1[1]
            dx3,dz3=4.84,0.5
            self.icon3.setPos(x3+dx3,y3,z3+dz3)

            self.icon4=loader.loadModel("models2/icon.egg")
            self.icon4.reparentTo(self.extraTri)
            x4,y4,z4=core.ends1[0]
            dy4,dz4=5,0.5
            self.icon4.setPos(x4,y4+dy4,z4+dz4)
        
    def spinCameraTask(self, task):     # set up the camera
        x,y,z=0,22,13.1
        base.cam.setPos(x,y,z)
        base.cam.lookAt(self.princess)
        if self.completed:
            base.cam.lookAt(self.princess)
        return Task.cont

##############################################################################

    def rotatePrincess(self):   # rotate the princess in four directions
        self.rotation+=1
        self.princessDir=self.rotation%4*90
        if self.level==2 and self.princess.getParent()==self.extraTri:
            self.rotation2+=1
            self.princessDir2=self.rotation2%4*90
            self.princess.setHpr(self.princessDir2,0,0)
        else: self.princess.setHpr(self.princessDir,0,0)

    def getRotation(self, point1, point2):
        if self.level==2:
            if self.curr==self.extraTri:
                (y1,x1,z1)=point1
                (y2,x2,z2)=point2
                if x1<x2 and abs(y2-y1)<1:
                    return 0
                elif y1>y2 and abs(x2-x1)<1:
                    return 90
                elif x1>x2 and abs(y2-y1)<1:
                    return 180
                elif y1<y2 and abs(x2-x1)<1:
                    return 0
        (x1,y1,z1)=point1
        (x2,y2,z2)=point2
        if x1>x2 and abs(y2-y1)<1:
            return 90
        elif y1>y2 and abs(x2-x1)<1:
            return 180
        elif x1<x2 and abs(y2-y1)<1:
            return 270
        elif y1<y2 and abs(x2-x1)<1:
            return 0
        

    def nextEnd(self):
        if self.pathOrder[-1]=="start":
            self.pathOrder.reverse()
        if self.curr==self.pathOrder[-1]:
            (x,y,z)=self.princess.getPos()
            if isinstance(self.curr,str):
                if self.curr=="path1":
                    (endx,endy,endz)=self.path1[-1]
                elif self.curr=="path2":
                    (endx,endy,endz)=self.path2[-1]
            else:
                (triEndsx,triEndsy,triEndsz)=self.triEnds[-1]
                (lastx,lasty,lastz)=self.pathOrder[-1].getPos()
                (endx,endy,endz)=(triEndsy-lasty,-(triEndsx-lastx),triEndsz-lastz)
            dz=0.5
            if abs(x-endx)<1 and abs(y-endy)<1 and abs(z-dz-endz)<1:
                self.completed=True
                self.complete()
            else: self.walkTri()
        else:

            if self.curr=="start":
                point1=self.princess.getPos()
                point2=self.startingPoint
                angle=self.getRotation(point1,point2)
                if self.princessDir==angle:
                    self.getStarted()
            elif self.curr=="path1":
                (x,y,z)=self.princess.getPos()
                dz=0.5
                if abs(x-self.path1[-1][0])<1 and abs(y-self.path1[-1][1])<1 and abs(z-self.path1[-1][2])<1:
                    self.switchToTri()
                else:
                    self.walkPath(1)  
            elif self.curr=="path2":
                (x,y,z)=self.princess.getPos()
                dz=0.5
                if abs(x-self.path2[-1][0])<1 and abs(y-self.path2[-1][1])<1 and abs(z-self.path2[-1][2])<1:
                    self.switchToTri()
                else:
                    self.walkPath(2)
            elif self.curr==self.tri1 or self.curr==self.extraTri:
                # self.princess.wrtReparentTo(self.curr)
                self.moveOn()

    def getStarted(self):
        then=self.pathOrder[1]
        if not isinstance(then,str):
            height=self.startingPoint[2]+0.5-self.princess.getPos()[2]
            self.climb(self.startingPoint,height)
            self.curr=then
        elif then=="path1":
            self.path1.reverse()
            (height,point)=self.getHeight(1)
            self.climb(point,height)
            self.curr="path1"
        elif then=="path2":
            self.path2.reverse()
            (height,point)=self.getHeight(2)
            self.climb(point,height)
            self.curr="path2"

    def moveOn(self):
        i=self.pathOrder.index(self.curr)
        then=self.pathOrder[i+1] 
        if not isinstance(self.curr,str):
            self.princess.wrtReparentTo(self.curr)
            self.walkTri()
        elif self.curr=="path1":
            i=self.pathOrder.index(self.curr)
            self.princess.wrtReparentTo(self.frame)
            (height,point)=self.getHeight(1)
            self.climb(point,height)
        elif self.curr=="path2":
            i=self.pathOrder.index(self.curr)
            self.princess.wrtReparentTo(self.frame)
            (height,point)=self.getHeight(2)
            self.climb(point,height)

    def walkPath(self, n):
        if n==1:
            path=self.path1
        elif n==2:
            path=self.path2
        dz=0.5
        (x,y,z)=self.princess.getPos()
        (x1,y1,z1)=(x,y,z-dz)
        currBlock=0
        (x2,y2,z2)=path[currBlock+1]
        (dx,dy,dz)=(abs(x2-x1),abs(y2-y1),abs(z2-z1))
        if (abs(dx-1)<1 and abs(dy-0)<1 and abs(dz-1)<1) or (abs(dx-0)<0 and abs(dy-1)<1 and abs(dz-1)<1):
            self.climb((x2,y2,z2),1)
        elif abs(path[2][0]-path[1][0])<1 and abs(path[2][1]-path[1][1])<1 and abs(path[2][2]-path[1][2])>1:
            (height,point)=self.getHeight(n,2)
            self.climb(point,height)
        else:
            for b in range(currBlock+2,len(path)-1):
                if (abs(path[b][0]-path[b-1][0]-dx)>1 or abs(path[b][1]-path[b-1][1]-dy)>1) and abs(path[b][2]-path[b-1][2]-dz)>1:
                    point=path[b-1]
                    self.walk(point)
        point=path[-1]
        self.walk(point)

    def walkTri(self):
        (x,y,z)=self.princess.getPos()
        (end1x,end1y,end1z)=core.ends1[0]
        (end2x,end2y,end2z)=core.ends1[1]
        dz=0.5
        if abs(end1z-(z-dz))>1 and abs(end2z-(z-dz))>1:
            if abs(end1z-z)<abs(end2z-z):
                height=end1z-z
                point=(end1x,end1y,end1z)
                self.climb(point,height)
            elif abs(end1z-z)>abs(end2z-z):
                height=end2z-z
                # point=(fx+end2x,fy+end2y,fz+end2z)
                point=(end2x,end2y,end2z)
                self.climb(point,height)
        if self.check():
            self.leaveIcon()
        else:
            for i in range(len(self.iconPos)):
                if abs(self.iconPos[i][2]-z)<1:
                    (x,y,z)=self.iconPos[i]
                    dz=0.5
                    point=(x,y,z-dz)
                    break
            self.walk(point)
        tmp=self.reachEndOfTri()
        if tmp!=None:
            self.princess.wrtReparentTo(self.frame)
            (x,y,z)=self.princess.getPos()
            (endx,endy,endz,n)=tmp
            dz=0.5
            point=(endx,endy,endz)
            if abs(z-dz-point[2])<1:
                movement4=self.princess.posInterval(0.5,Point3(point))
                self.walkPath(n)

    def reachEndOfTri(self):
        if self.curr==self.pathOrder[-1]:
            return None
        else:
            i=self.pathOrder.index(self.curr)
            then=self.pathOrder[i+1]
            (x,y,z)=self.princess.getPos()
            if then=="path1":
                (endx,endy,endz)=self.path1[0]
                if abs(x-endx)<2 and abs(y-endy)<2 and abs(z-endz)<2:
                    self.curr=then
                    return (endx,endy,endz,1)
            elif then=="path2":
                (endx,endy,endz)=self.path2[0]
                self.specialCase+=1
                if self.level==2 and self.pathOrder[1]==self.extraTri: 
                    if self.specialCase==1:
                        (dx,dy,dz)=self.extraTri.getPos()
                        (endx,endy,endz)=(endx+dx,endy+dy,endz+dz)
                    elif self.specialCase==2:
                        (endx,endy,endz)=(0,-7,0.5)
                if (abs(x-endx)<2 and abs(y-endy)<2 and abs(z-endz)<2):
                    self.curr=then
                    return (endx,endy,endz,2)
            elif isinstance(then,str):
                self.princess.wrtReparentTo(self.then)
            return None
            
            
    def climb(self, point, height):
        x,y,z=self.princess.getPos()
        climb=self.princess.posInterval(1,Point3(x,y,z+1))
        (px,py,pz)=point
        dz=0.5
        move=self.princess.posInterval(1,Point3(px,py,pz+dz))
        movement1=Sequence(climb,move)
        movement1.start()

    def walk(self, point):
        point1=self.princess.getPos()
        (x,y,z)=point
        point2=(x,y,z+0.5)
        angle=self.getRotation(point1,point2)
        print("calculated as", angle, "should be", self.princessDir)
        if self.level==2 and self.curr==self.extraTri and self.princessDir2==angle:
            movement2=self.princess.posInterval(2,Point3(point2))
            movement2.start()
        elif self.princessDir==angle:
            movement2=self.princess.posInterval(2,Point3(point2))
            movement2.start()

    def leaveIcon(self):
        triangle=self.princess.getParent()
        if triangle==self.tri1:
            if self.success1:
                self.fly()
            else:
                self.leave()
        elif self.level==2 and triangle==self.extraTri:
            if self.success2:
                self.fly()
            else:
                self.leave()

    def fly(self):
        for i in range(len(self.iconPos)):
            if abs(self.princess.getPos()[2]-self.iconPos[i][2])>1:
                (x,y,z)=self.iconPos[i]
        corner=(-3.84,0,4.5)
        fly1=self.princess.posInterval(1,Point3(corner))
        fly2=self.princess.posInterval(1,Point3(corner[0],corner[1]+2,corner[2]))
        fly3=self.princess.posInterval(1,Point3(x,y,z))
        turnaround1=self.princess.hprInterval(0.5,Point3(0,0,0))
        turnaround2=self.princess.hprInterval(0.5,Point3(270,0,0))
        if self.princess.getPos()[2]>z:
            flying=Sequence(fly1,turnaround1,fly2,fly3)
        elif self.princess.getPos()[2]<z:
            flying=Sequence(fly2,fly1,turnaround2,fly3)
        flying.start()

    def getHeight(self, n, i=0):
        height=1
        if n==1:
            path=self.path1[i:]
        elif n==2:
            path=self.path2[i:]
        x,y,z=path[0][0],path[0][1],path[0][2]
        for i in range(1,len(path)):
            if (path[i][0]!=x and path[i][2]!=z) or (path[i][1]!=y and path[i][2]!=z) or path[i][2]==z:
                return (height,path[i-1])
            height+=1
        return (height,path[-1])

    def switchToTri(self):
        i=self.pathOrder.index(self.curr)
        then=self.pathOrder[i+1]
        if isinstance(self.curr,str) and not isinstance(then,str):
            self.curr=then
            self.princess.wrtReparentTo(then)
            self.walkTri()

    def check(self):
        (x,y,z)=self.princess.getPos()
        for i in range(len(self.iconPos)):
            if abs(x-self.iconPos[i][0])<1 and abs(y-self.iconPos[i][1])<1 and abs(z-self.iconPos[i][2])<1:
                return True
        return False

    def leave(self):
        if self.princess.getParent()==self.tri1 or self.princess.getParent()==self.extraTri:
            end=core.ends1
            for i in range(len(end)):
                if abs(end[i][2]-self.princess.getPos()[2])<1:
                    point=end[i]
            self.walk(point)

    def complete(self):
        (x,y,z)=self.princess.getPos()
        (endx,endy,endz)=self.endingPoint
        angle=self.getRotation((x,y,z),self.endingPoint)
        self.princess.wrtReparentTo(self.end)
        (x,y,z)=self.princess.getPos()
        (Min,Max)=self.end.getTightBounds()
        (dx,dy,dz)=Max-Min
        scale=2/3
        turnaround=self.princess.hprInterval(0.5,Point3(-90,0,0))
        movement5=self.princess.posInterval(0.5,Point3(0,0,z))
        movement6=self.princess.posInterval(0.5,Point3(0,0,0.1))
        (Min2,Max2)=self.princess.getTightBounds()
        correction=Max2-Min2
        movement7=self.princess.posInterval(2,Point3(dy*scale,0,-dz+correction[2]*2+0.1))
        endMove=Sequence(movement5,movement6,turnaround,movement7)
        endMove.start()

game = myDemo()
base.run()