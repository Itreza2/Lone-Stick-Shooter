from csv import reader
from time import time
from PIL import Image, ImageTk

class Var:

    grille=[]; grilleP=[]

    lText=[]; Xp=[]; lDed=[]; lObj=[]; lCoffre=[]
    modList=[[], 0, time(), None]

    level=0; pression=0
    frame=time(); tac=time(); debordeur=0
    gStats=[time(), 0]

    bestiaire=[]; lecteur=reader(open('files/ennemies.csv','r'))
    for line in lecteur:bestiaire.append(line)
    for i in bestiaire:
        for j in range(len(i)):
            try:i[j]=int(i[j])
            except ValueError:pass

    arsenal=[]; lecteur=reader(open('files/weapons.csv','r'))
    for line in lecteur:arsenal.append(line)
    for i in arsenal:
        for j in range(len(i)):
            try:i[j]=float(i[j])
            except ValueError:pass

    monde=None; portal=[None, None]

    animE=[[1,4,None,None,'troupierIdle', 100, [], []],[1,6,None,None,'troupierWalk',100, [], []],[1,6,None,None,'troupierWalkR',100, [], []],
        [1,4,None,None,'gunnerIdle',100, [], []],[1,6,None,None,'gunnerWalk',100, [], []],[1,6,None,None,'gunnerWalkR',100, [], []],
        [1,4,None,None,'marksmanIdle',100, [], []],[1,6,None,None,'marksmanWalk',100, [], []],[1,6,None,None,'marksmanWalkR',100, [], []],
        [1,4,None,None,'gunnerIdle',200, [], []],[1,6,None,None,'gunnerWalk',200, [], []],[1,6,None,None,'gunnerWalkR',200, [], []],
        [1,4,None,None,'marksmanIdle',200, [], []],[1,6,None,None,'marksmanWalk',200, [], []],[1,6,None,None,'marksmanWalkR',200, [], []],
        [1,4,None,None,'dmgIdle', 100, [], []],[1,6,None,None,'dmgWalk',100, [], []],[1,6,None,None,'dmgWalkR',100, [], []],
        [1,4,None,None,'dmgIdle', 200, [], []],[1,6,None,None,'dmgWalk',200, [], []],[1,6,None,None,'dmgWalkR',200, [], []]]
    
    animO=[[1,4,None, [Image.open('sprites/portal/'+str(i)+'.png') for i in range(1,5)]]]