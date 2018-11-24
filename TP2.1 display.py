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

loadPrcFileData('', 'win-size 600 800')
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
        self.block=[]
        self.ladder1=set()
        self.ladder2=set()
        self.loadModels()
        self.loadBackground() # load lights and background
        self.loadMaze()

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
        move.start()

    def rotate2(self):
        move=self.tri1.hprInterval(2,Point3(self.rotatingAngle1,0,0))
        move.start()
        
    def loadModels(self):
        # self.block=loader.loadModel("models2/block.egg")
        # self.block.reparentTo(render)
        # self.block.setPos(0,0,0)

        # self.block2=loader.loadModel("models2/block.egg")
        # self.block2.reparentTo(render)
        # self.block2.setPos(4,0,0)

        # self.block3=loader.loadModel("models2/block.egg")
        # self.block3.reparentTo(render)
        # self.block3.setPos(5,0,0)

        # self.block4=loader.loadModel("models2/block.egg")
        # self.block4.reparentTo(render)
        # self.block4.setPos(0,0,-5)

        

        (x,y,z,h,p,r)=core.placeTri()
        self.tri1=loader.loadModel("models2/tri1.egg")
        self.tri1.reparentTo(render)
        self.tri1.setScale(0.8)
        self.tri1.setPos(x,y,z)
        self.tri1.setHpr(h,0,r)
        self.rotatingAngle1,self.rotatingAngle2=h,p
        
        self.frame=loader.loadModel("models2/tri1frame.egg")
        self.frame.reparentTo(render)
        self.frame.setScale(0.8)
        self.frame.setPos(x,y,z)
        self.frame.setHpr(h,0,r)
        self.framex,self.framey,self.framez=x,y,z

        self.block5=loader.loadModel("models2/ladder.egg")
        self.block5.reparentTo(self.frame)
        self.block5.setPos(0,-9,3)
        self.block5.setHpr(45,0,0)

        # self.block6=loader.loadModel("models2/block.egg")
        # self.block6.reparentTo(self.frame)
        # self.block6.setPos(-4.84,0,4)
        # self.block6.setHpr(-45,0,0)

        # self.block7=loader.loadModel("models2/block.egg")
        # self.block7.reparentTo(self.frame)
        # self.block7.setPos(0,0,-5)
        # self.block7.setHpr(-45,0,0)

        self.princess=loader.loadModel("models/princess.egg")
        self.princess.reparentTo(self.tri1)
        self.princess.setHpr(90,0,0)
        self.princess.setPos(0,0,4.5)

    def loadMaze(self):
        path1,path2=core.getPath(12, self.framex, self.framey, self.framez)
        print(path1,path2)
        self.ladder1=core.checkLadder(path1)
        self.ladder2=core.checkLadder(path2)
        for i in range(len(path1)):
            x,y,z=path1[i]
            h=-45
            if (x,y,z) in self.ladder1:
                self.ladder=loader.loadModel("models2/ladder.egg")
                self.ladder.reparentTo(self.frame)
                self.ladder.setPos(x,y,z)
                self.ladder.setHpr(h,0,0)
            else:
                self.block=loader.loadModel("models2/block.egg")
                self.block.reparentTo(self.frame)
                self.block.setPos(x,y,z)
                self.block.setHpr(h,0,0)
        for j in range(len(path2)):
            x,y,z=path2[j]
            h=-45
            if (x,y,z) in self.ladder2:
                self.ladder=loader.loadModel("models2/ladder.egg")
                self.ladder.reparentTo(self.frame)
                self.ladder.setPos(x,y,z)
                self.ladder.setHpr(h,0,0)
            else:
                self.block=loader.loadModel("models2/block.egg")
                self.block.reparentTo(self.frame)
                self.block.setPos(x,y,z)
                self.block.setHpr(h,0,0)
    def spinCameraTask(self, task):     # set up the camera
        x,y,z=0,22,13.1
        base.cam.setPos(x,y,z)
        base.cam.lookAt(0,0,0)
        return Task.cont

game = myDemo()
base.run()