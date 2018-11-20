#core imports
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
import sys, math, os, random
from math import pi, sin, cos
from panda3d.core import loadPrcFileData 

loadPrcFileData('', 'win-size 600 800')
#Citation: https://stackoverflow.com/questions/15000460/how-to-change-the-window-size-in-panda3d

#for task managers
from direct.task.Task import Task


class myDemo(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        #load all the things
        self.pos=[]
        self.dimension=[]
        self.loadBackground() # load lights and the fancy background

        self.loadModels()

        self.accept("arrow_up", self.walkPrincess)
        self.rotation=[0,0,0]
        self.accept("space", self.rotatePrincess)
        self.accept("r", self.rotatePiece)
        self.success=False
 
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")


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
        plight3.setColor(VBase4(1, 1, 1, 1))
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

        plight7=PointLight('plight')
        plight7.setColor(VBase4(1, 1, 1, 1))
        plight7NodePath=render.attachNewNode(plight6)
        plight7NodePath.setPos(-500,0, 0)
        plight7NodePath.setHpr(170,0,0)
        render.setLight(plight7NodePath)

        
    def loadModels(self):
        self.princess=loader.loadModel("models/princess.egg")
        self.princess.reparentTo(render)
        self.princess.setPos(2.8,3.5,0)
        self.princess.setHpr(45,0,0)
        self.pos.append(self.princess.getPos())

        self.frame=loader.loadModel("models/chapter1frame.egg")
        self.frame.reparentTo(render)
        self.frame.setPos(0,5,-1)
        self.frame.setHpr(0,0,0)

        self.piece1=loader.loadModel("models/chapter11.egg")
        self.piece1.reparentTo(self.frame)
        self.piece1.setPos(0,0,0)
        self.piece1.setHpr(0,0,0)
        min1,max1=self.piece1.getTightBounds()
        self.dimension.append(max1-min1)

        self.piece2=loader.loadModel("models/chapter12.egg")
        self.piece2.reparentTo(self.frame)
        self.piece2.setPos(0,0,0)
        min2,max2=self.piece2.getTightBounds()
        self.dimension.append(max2-min2)

        self.piece3=loader.loadModel("models/chapter13.egg")
        self.piece3.reparentTo(render)
        self.piece3.setPos(-1.63,7,4.3)
        self.piece3.setHpr(51,0,0)
        min3,max3=self.piece3.getTightBounds()
        self.dimension.append(max3-min3)

        self.piece4=loader.loadModel("models/chapter14.egg")
        self.piece4.reparentTo(self.frame)
        self.piece4.setPos(0,0,0)
        min4,max4=self.piece4.getTightBounds()
        self.dimension.append(max4-min4)

        self.piece5=loader.loadModel("models/chapter15.egg")
        self.piece5.reparentTo(self.frame)
        self.piece5.setPos(0,0,0)
        min5,max5=self.piece5.getTightBounds()
        self.dimension.append(max5-min5)
        

        

    def walkPrincess(self):
        x,y,z=self.pos[-1]
        print(self.rotation[0])
        if len(self.pos)==1:
            if self.rotation[0]%4==0:
                dx,dy,dz=self.dimension[0]
                newx,newy,newz=x-dx*(2/3),y+dy*(2/3),z
                self.princessMovement1=self.princess.posInterval(3,Point3(newx,newy,newz))
                self.princessMovement1.start()
                self.pos.append((newx,newy,newz))
                print(self.pos)
            elif self.rotation[0]%4==1:
                dx,dy,dz=self.dimension[1]
                newx,newy,newz=x-dx*(2/3),y+dy*(3/2),z+5
                self.princessinterval1=self.princess.posInterval(2,Point3(newx,newy,newz))
                self.princessinterval2=self.princess.scaleInterval(2,0.8)
                self.princessMovement2=Parallel(self.princessinterval1,self.princessinterval2)
                self.princessMovement2.start()
                self.pos.append((newx,newy,newz))
                print(self.pos)
                
        elif len(self.pos)==2:
            if self.success:
                    dx,dy,dz=self.dimension[2]
                    newx,newy,newz=x-dx*(2/3),y-dy*(2/3),z
                    self.princessMovement3=self.princess.posInterval(2,Point3(newx,newy,newz))
                    self.princessMovement3.start()
                    self.pos.append((newx,newy,newz))
        elif len(self.pos)==3:
            if self.rotation[0]%4==2:
                self.pos.pop()
                dx,dy,dz=self.pos[-1]
                self.princessMovement = self.princess.posInterval(3, Point3(x,y,z))
                self.princessMovement.start()

        

            

    def rotatePrincess(self):
        self.rotation[0]+=1
        if self.rotation[0]%4==0:
            self.princess.setHpr(45,0,0)
        elif self.rotation[0]%4==1:
            self.princess.setHpr(135,0,0)
        elif self.rotation[0]%4==2:
            self.princess.setHpr(225,0,0)
        else: self.princess.setHpr(-45,0,0)
        
    def rotatePiece(self):
        self.rotation[2]+=1
        if self.rotation[2]%2==1:
            piece3interval1=self.piece3.hprInterval(2,Point3(-45,-90,0))
            piece3interval2=self.piece3.posInterval(2,Point3(-0.46,7.95,5))
            piece3Movement1=Parallel(piece3interval1,piece3interval2)
            piece3Movement1.start()
            self.success=True
        elif self.rotation[2]%2==0:
            piece3interval3=self.piece3.hprInterval(2,Point3(51,0,0))
            piece3interval4=self.piece3.posInterval(2,Point3(-1.63,7,4.3))
            piece3Movement2=Parallel(piece3interval3,piece3interval4)
            piece3Movement2.start()
            self.success=False

    def spinCameraTask(self, task):
        base.cam.setPos(0,25,15)
        base.cam.lookAt(0,0,0)
        return Task.cont

game = myDemo()
r, g, b=0.04, 0.16, 0.2
base.setBackgroundColor(r,g,b)
base.run()