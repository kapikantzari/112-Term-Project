#core imports
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import sys, math, os, random
from math import pi, sin, cos

#for task managers
from direct.task.Task import Task


class myDemo(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        #load all the things
        self.loadBackground() # load lights and the fancy background

        self.loadModels()
 
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")


    def loadBackground(self):

        #add one light per face, so each face is nicely illuminated

        plight1 = PointLight('plight')
        plight1.setColor(VBase4(1, 1, 1, 1))
        plight1NodePath = render.attachNewNode(plight1)
        plight1NodePath.setPos(0, 0, 500)
        render.setLight(plight1NodePath)

        plight2 = PointLight('plight')
        plight2.setColor(VBase4(1, 1, 1, 1))
        plight2NodePath = render.attachNewNode(plight2)
        plight2NodePath.setPos(0, 0, -500)
        render.setLight(plight2NodePath)

        plight3 = PointLight('plight')
        plight3.setColor(VBase4(1, 1, 1, 1))
        plight3NodePath = render.attachNewNode(plight3)
        plight3NodePath.setPos(0, -500, 0)
        render.setLight(plight3NodePath)

        plight4 = PointLight('plight')
        plight4.setColor(VBase4(1, 1, 1, 1))
        plight4NodePath = render.attachNewNode(plight4)
        plight4NodePath.setPos(0, 500, 0)
        render.setLight(plight4NodePath)

        plight5 = PointLight('plight')
        plight5.setColor(VBase4(1, 1, 1, 1))
        plight5NodePath = render.attachNewNode(plight5)
        plight5NodePath.setPos(500,0, 0)
        render.setLight(plight5NodePath)

        plight6 = PointLight('plight')
        plight6.setColor(VBase4(1, 1, 1, 1))
        plight6NodePath = render.attachNewNode(plight6)
        plight6NodePath.setPos(-500,0, 0)
        render.setLight(plight6NodePath)

        
    def loadModels(self):
        self.princess=loader.loadModel("models/princess.egg")
        self.princess.reparentTo(render)
        z=7.3
        self.princess.setPos(0,0,z)
        self.triangle1=loader.loadModel("models/impossibleTriangle1.egg")
        self.triangle1.reparentTo(render)
        self.triangle1.setPos(0,5,0)
        self.triangle2=loader.loadModel("models/impossibleTriangle2.egg")
        self.triangle2.reparentTo(render)
        x1, x2=-0.1, 4.2
        self.triangle2.setPos(x1,x2,0)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 3, 0)
        return Task.cont
     

game = myDemo()
base.run()