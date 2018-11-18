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
        self.loadBackground() # load lights and the fancy background

        self.loadModels()

        self.accept("arrow_up", self.walkPrincess)
        self.rotation=[0,0]
        self.accept("space", self.rotatePrincess)
        self.accept("r", self.rotatePiece)
 
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

        self.piece1=loader.loadModel("models/chapter11.egg")
        self.piece1.reparentTo(render)
        self.piece1.setPos(0,5,-1)
        self.piece1.setHpr(0,0,0)

        self.piece5=loader.loadModel("models/chapter15.egg")
        self.piece5.reparentTo(self.piece1)
        self.piece5.setPos(0,0,0)
        self.piece5.setHpr(0,0,0)

        self.piece2=loader.loadModel("models/chapter12.egg")
        self.piece2.reparentTo(self.piece1)
        self.piece2.setPos(0,0,0)
        self.piece2.setHpr(0,0,0)

        self.piece4=loader.loadModel("models/chapter14.egg")
        self.piece4.reparentTo(self.piece2)
        self.piece4.setPos(0,0,0)
        self.piece4.setHpr(0,0,0)

    def walkPrincess(self):
        # self.princessMovement = self.princess.posInterval(3, Point3(-2.5, 10, 0))
        # self.princessMovement.loop()
        # self.princessMovement = self.princess.posInterval(3, Point3(-0.6, 0.5, 0))
        # self.princessMovement.loop()
        x,y,z=self.princess.getPos()
        if self.rotation[0]%4==0:
            minB,maxB=self.piece5.getTightBounds()
            dx,dy,dz=maxB-minB
            print(maxB)
            self.princessMovement = self.princess.posInterval(3, Point3(x-dx*(2/3),y+dy*(2/3),z))
            self.princessMovement.start()
        elif self.rotation[0]%4==2:
            self.princessMovement = self.princess.posInterval(3, Point3(2.8,3.5, 0))
            self.princessMovement.start()
        #elif self.rotation%4==1:
            

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
        piece4interval1 = self.piece4.hprInterval(2, Point3(-45, -90,0))
        piece4interval2=self.piece4.posInterval(2, Point3(-3,-1,9))
        piece4Movement=Parallel(piece4interval1, piece4interval2)
        piece4Movement.start()

    def spinCameraTask(self, task):
        base.cam.setPos(0,25,15)
        base.cam.lookAt(0,0,0)
        return Task.cont
    # def spinCameraTask(self, task):
    #     angleDegrees = task.time * 6.0
    #     angleRadians = angleDegrees * (pi / 180.0)
    #     self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
    #     self.camera.setHpr(angleDegrees, 3, 0)
    #     return Task.cont
     

game = myDemo()
base.disableMouse()
r, g, b=0.04, 0.16, 0.2
base.setBackgroundColor(r,g,b)
base.run()