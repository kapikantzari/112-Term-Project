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
from direct.task.Task import Task

class myDemo(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        #load all the things
        self.rotatingAngle1,self.rotatingAngle2=0,0
        self.framex,self.framey,self.framez=0,0,0
        self.size=0
        self.level=2
        self.blocks=[]
        self.path1,self.path2=[],[]
        self.triEnds=[]
        self.pathOrder=[]
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

        print(self.pathOrder)

        self.accept("r", self.rotate1)
        self.accept("z", self.rotate2)

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

    def rotate1(self):
        move=self.tri1.hprInterval(2,Point3(self.rotatingAngle1-90,self.rotatingAngle2,0))
        movement1=Sequence(move,Wait(2))
        movement1.start()
        x,y,z=self.princess2.getPos()
        print(x,y,z)

    def rotate2(self):
        move=self.tri1.hprInterval(2,Point3(self.rotatingAngle1,self.rotatingAngle2,0))
        move.start()
        
    def loadModels(self):
        ends=[(0,-7,0),(-4.84,0,4)]
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

        self.princess2=loader.loadModel("models/princess.egg")
        self.princess2.reparentTo(self.tri1)
        self.princess2.setHpr(0,0,0)
        self.princess2.setPos(0,-2,0.5)

    def loadExtraTri(self):
        (x,y,z,h,p,r,i)=core.placeExtraTri(self.triEnds)
        self.extraTri=loader.loadModel("models2/tri1.egg")
        self.extraTri.reparentTo(self.frame)
        self.extraTri.setPos(x,y,z)
        self.extraTri.setHpr(h,p,r)
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
        i=self.triEnds.index((firstx,firsty,firstz))
        self.triEnds.pop(i)
        if i==0:
            self.pathOrder.insert(0,"start")
        else: self.pathOrder.append("start")
        sx,sy,sz=core.getStart(firstx,firsty,firstz)
        self.start=loader.loadModel("models2/start.egg")
        self.start.reparentTo(self.frame)
        self.start.setPos(sx,sy,sz)
        self.start.setHpr(0,0,0)

        self.princess=loader.loadModel("models/princess.egg")
        self.princess.reparentTo(self.frame)
        self.princess.setHpr(0,0,0)
        dz=0.185
        self.princess.setPos(sx,sy,sz-dz)

    def loadEnd(self):
        (lastx,lasty,lastz)=self.triEnds[-1]
        (x,y,z,h)=core.getEnd(lastx,lasty,lastz)
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
        
        self.icon2=loader.loadModel("models2/icon.egg")
        self.icon2.reparentTo(self.tri1)
        x2,y2,z2=core.ends1[0]
        dy2,dz2=5,0.5
        self.icon2.setPos(x2,y2+dy2,z2+dz2)

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
        base.cam.lookAt(0,0,0)
        return Task.cont

game = myDemo()
base.run()