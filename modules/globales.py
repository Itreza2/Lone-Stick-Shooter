from csv import reader
from time import time

class Var:

    grille=[]; grilleP=[]

    lText=[]

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