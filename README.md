# 15112-Term-Project
For CS 15-112 Term Project at Carnegie Mellon University

# Project Name: Edge
  (Inspired by Monument Valley)
  (Inspired by Galileo and scientists working on the Edge of the world)
  (Youtube: https://www.youtube.com/watch?v=lmMKk0I1g78&t=4s)


# Description :
Use Panda3D and Blender to construct mazes with two-dimensional visual 
illusions (Penrose triangle) in the style of the original game Monument 
Valley and develop an algorithm in Python for generating random solvable 
mazes.


# Main Files :
splash.py
         displays fancy splash screen, main menu that describes the 
         playing rules and introduces the inspiration for making the game.

display.py
          displays different game scenes depending on the difficulty
          level chosen by the player. Hello, Princess Ada!
          
core.py
       contains an algorithm in python that serves as a random generator
       for solvable mazes. 
       
models2/
        updated models of Princess Ada, building blocks, Penrose triangle,
        pattern of the most beautiful geometric structure Lie Group E8, and
        everything you see in the game are stored here. They're all built
        with Blender.
        
        
# Running the game
Download Edge_final.zip and Edge_models, unzip and put models2 folder into 
unzipped Edge_final. Open display.py, run, and Enjoy the game!
(Note: Panda3D is a module developed by CMU, and it might not work consistently
with the latest MacOS system. If you fail to open it in such editors as Sublime,
try to run it in terminal with command: $ python display.py)
