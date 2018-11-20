#core imports
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from direct.interval.IntervalGlobal import *
import sys, math, os, random
from math import pi, sin, cos
from panda3d.core import loadPrcFileData 

loadPrcFileData('', 'win-size 600 800')
#Citation: https://stackoverflow.com/questions/15000460/how-to-change-the-window
#-size-in-panda3d

#for task managers
from direct.task.Task import Task

class myDemo(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        #load all the things
        self.pos=[]
        self.dimension=[]
        self.loadModels()
        self.loadBackground() # load lights and background

        self.accept("arrow_up", self.walkPrincess)
        self.rotation=[0,0,0]
        self.accept("space", self.rotatePrincess)
        self.accept("r", self.seeTheTruth) # once user completes the game
                                           # allowing rotation of the scene
        self.success=False  # if the user completes the game
        self.rotationComplete=False # if the user trigger the illusion piece

        #collision solid
        self.iconCol=CollisionNode('colIcon')
        self.iconCol.addSolid(CollisionSphere(0,0,0,1))
        self.fromIcon=self.icon1.attachNewNode(self.iconCol)

        # collision with icon
        pusher = CollisionHandlerPusher()
        pusher.addCollider(self.fromIcon,self.icon1)
 
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

        self.alight = render.attachNewNode(AmbientLight("Ambient"))
        self.alight.node().setColor(LVector4(0.05,0.05,0.05, 0.2))
        render.setLight(self.alight)
        
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

        self.piece6=loader.loadModel("models/chapter16.egg")
        self.piece6.reparentTo(self.frame)
        self.piece6.setPos(0,0,0)
        
        self.icon1=loader.loadModel("models/icon1.1.egg")
        self.icon1.reparentTo(render)
        dx,dy,dz=self.dimension[0]
        x,y,z=self.pos[0]
        newx,newy,newz=x-dx*(2/3),y+dy*(2/3)-0.3,z+0.5
        self.icon1.setPos(newx,newy,newz)

    def walkPrincess(self): # 'hard code' paths that the princess might walk
        x,y,z=self.pos[-1]
        if len(self.pos)==1:
            if self.rotation[0]%4==0:
                dx,dy,dz=self.dimension[0]
                newx,newy,newz=x-dx*(2/3),y+dy*(2/3),z
                princessMovement1=self.princess.posInterval(3,Point3(newx,newy,\
                    newz))
                princessMovement1.start()
                self.pos.append((newx,newy,newz))
                self.collisionCheck()
            elif self.rotation[0]%4==1:
                dx,dy,dz=self.dimension[1]
                newx,newy,newz=x-dx*(2/3),y+dy*(3/2),z+5.2
                princessinterval1=self.princess.posInterval(2,Point3(newx,newy,\
                    newz))
                princessinterval2=self.princess.scaleInterval(2,0.7)
                princessMovement2=Parallel(princessinterval1,princessinterval2)
                seq=Sequence()
                seq.append(princessMovement2)
                self.pos.append((newx,newy,newz))
                if self.rotationComplete:
                    x,y,z=self.pos[-1]
                    dx,dy,dz=self.dimension[2]
                    newx,newy,newz=x-dx*(5/3),y-dy*(5/3),z
                    princessMovement3=self.princess.posInterval(3,Point3(newx,\
                        newy,newz))
                    seq.append(princessMovement3)
                    self.pos.append((newx,newy,newz))
                seq.start()                
        elif len(self.pos)==2:
            if self.rotation[0]%4==2 and self.pos[-2]>self.pos[-1]:
                self.pos.pop()
                dx,dy,dz=self.pos[-1]
                princessMovement4=self.princess.posInterval(3, Point3(dx,dy,dz))
                princessMovement4.start()
            elif self.rotation[0]%4==3:
                self.pos.pop()
                dx,dy,dz=self.pos[-1]
                princessInterval3=self.princess.posInterval(3, Point3(dx,dy,dz))
                princessInterval4=self.princess.scaleInterval(3, 1)
                princessMovement5=Parallel(princessInterval3,princessInterval4)
                princessMovement5.start()
        elif len(self.pos)==3:
            if self.rotation[0]%4==2:
                dx,dy,dz=self.dimension[3]
                newx,newy,newz=x+dx*(4/5),y-dy*(4/5),z
                princessMovement6=self.princess.posInterval(3, Point3(newx,\
                    newy,z))
                princessMovement6.start()
                self.pos.append((newx,newy,newz))
            elif self.rotation[0]%4==3:
                seq=Sequence()
                self.pos.pop()
                dx,dy,dz=self.pos[-1]
                princessMovement7=self.princess.posInterval(3, Point3(dx,dy,dz))
                seq.append(princessMovement7)
                self.pos.pop()
                dx,dy,dz=self.pos[-1]
                princessInterval5=self.princess.posInterval(2, Point3(dx,dy,dz))
                princessInterval6=self.princess.scaleInterval(2, 1)
                princessMovement8=Parallel(princessInterval5,princessInterval6)
                seq.append(princessMovement8)
                seq.start()
        elif len(self.pos)==4:
            if self.rotation[0]%4==1:
                dx,dy,dz=self.dimension[4]
                newx,newy,newz=x-dx*(2/3),y-dy*(2/3),z+dz
                princessMovement9=self.princess.posInterval(3, Point3(newx,\
                    newy,newz))
                princessMovement9.start()
                self.success=True
            elif self.rotation[0]%4==0:
                self.pos.pop()
                dx,dy,dz=self.pos[-1]
                princessMovement10=self.princess.posInterval(3,Point3(dx,dy,dz))
                princessMovement10.start()

    def rotatePrincess(self):   # rotate the princess in four directions
        self.rotation[0]+=1
        if self.rotation[0]%4==0:
            self.princess.setHpr(45,0,0)
        elif self.rotation[0]%4==1:
            self.princess.setHpr(135,0,0)
        elif self.rotation[0]%4==2:
            self.princess.setHpr(225,0,0)
        else: self.princess.setHpr(-45,0,0)
        
    def seeTheTruth(self): # when the game is completed, the user can rotate the
        if self.success:   # setting to see the illusory trick
            self.rotation[2]+=1
            if self.rotation[2]%2==1:
                piece3MoveCheck=self.rotatePiece()
                piece3MoveCheck.start()
            elif self.rotation[2]%2==0:
                piece3interval3=self.piece3.hprInterval(2,Point3(51,0,0))
                piece3interval4=self.piece3.posInterval(2,Point3(-1.63,7,4.3))
                piece3MoveCheck2=Parallel(piece3interval3,piece3interval4)
                piece3MoveCheck2.start()

    def rotatePiece(self):      # rotate the magic piece
        piece3interval1=self.piece3.hprInterval(2,Point3(-45,-90,0))
        piece3interval2=self.piece3.posInterval(2,Point3(-0.46,7.95,5))
        piece3Movement1=Parallel(piece3interval1,piece3interval2)
        return piece3Movement1

    def collisionCheck(self):   # check if the princess collide with icon
        x,y,z=self.icon1.getPos()
        minb,maxb=self.icon1.getTightBounds()
        dx,dy,dz=maxb-minb
        transIcon=self.icon1.posInterval(1,Point3(x,y,z-dz))
        iconMove=Sequence(Wait(2.8),transIcon)
        iconMove.start()
        piece3Move=self.rotatePiece()
        piece3rotation=Sequence(Wait(3),piece3Move)
        piece3rotation.start()
        self.rotationComplete=True

    def spinCameraTask(self, task):     # set up the camera
        base.cam.setPos(0,22,13.1)
        base.cam.lookAt(0,0,0)
        if self.success:
            Wait(3)
            base.cam.lookAt(self.princess)
        return Task.cont

game = myDemo()
r, g, b=0.04, 0.16, 0.2
base.setBackgroundColor(r,g,b)
base.run()