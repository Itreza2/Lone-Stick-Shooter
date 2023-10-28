from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk
from math import cos, sin, atan, pi, sqrt
from random import randint, randrange, random
from time import time
from csv import reader, writer
from os import path, environ, makedirs

from modules.classes import Joueur, Combat, Ennemi, Projectile, Orbe
from modules.globales import Var
from modules.affichage import affichage, affichageMenus

tk=Tk()
tk.attributes('-fullscreen', True)
tk.config(cursor='none')
tk.iconbitmap('sprites/UI/icone.ico')

#-------------------------------------------------------------------------------------------------------------------|>

tic=time(); fpsLimiter=time(); animP=[[1,5],[1,6]]; state=False
lInput=[False, False, False, False, False, False]; anim=1; Joueur.wStats=[0, 'FAMAS', 1]
Projectile.index=[]; salles=[]; curseur=[0,0]
Combat.index=[]; Ennemi.index=[]; nL=True; angle=pi/100; fps=0
bonus=[1,1,0]; Orbe.index=[]; Var.Xp=[0,1,1]
filter=ImageTk.PhotoImage(Image.open('sprites/UI/filter.png').resize((int(tk.winfo_screenwidth()/2), int(tk.winfo_screenheight()))))

weapon=None; map=None

for i in range(len(Var.animE)):#Découpe des Sprite Sheets
    for j in range(Var.animE[i][1]):
        Var.animE[i][6].append(ImageTk.PhotoImage(
        Image.open('sprites/ennemies/'+Var.animE[i][4]+'.png').crop((0+24*(j),0,24+24*(j),24)).resize((Var.animE[i][5], Var.animE[i][5]))))
        Var.animE[i][7].append(ImageTk.PhotoImage(
        Image.open('sprites/ennemies/'+Var.animE[i][4]+'.png').crop((0+24*(j),0,24+24*(j),24)).resize((Var.animE[i][5], Var.animE[i][5])).transpose(Image.FLIP_LEFT_RIGHT)))

menuState=['Main',0,True,time()]; config=False
bg=[PhotoImage(file='sprites/UI/bg.png'),None,None,0,0,time(),0]

modsC=[]; lecteur=reader(open('files/mods.csv', 'r'))
for line in lecteur:modsC.append(line)
for i in range(len(modsC)):
    for j in range(len(modsC[i])):modsC[i][j]=float(modsC[i][j])
wSprites={} 
Joueur.wStats=Var.arsenal[0]

WeaponsP=[[Image.open('sprites/armes/'+Var.arsenal[i][1]+'/'+Var.arsenal[i][1]+str(j)+'.png')
           for j in range(1,4)] for i in range(len(Var.arsenal))]

Joueur.powers=[[False, False, ImageTk.PhotoImage(Image.open('sprites/perso/shield.png').resize((100, 100)))],
        [False, False, ImageTk.PhotoImage(Image.open('sprites/perso/fire.png').resize((100, 100)))],
        [True, False, ImageTk.PhotoImage(Image.open('sprites/perso/wings.png').resize((100, 100)))]]

ded1=ImageTk.PhotoImage(Image.open('sprites/ennemies/troupierDed.png').resize((100,100)))
ded2=ImageTk.PhotoImage(Image.open('sprites/ennemies/troupierDed.png').resize((200,200)))

mur=[PhotoImage(file='sprites/level/tiles/1.png'),PhotoImage(file='sprites/level/tiles/2.png'),PhotoImage(file='sprites/level/tiles/3.png')]
murH=[PhotoImage(file='sprites/level/tiles/mur1H.png'),PhotoImage(file='sprites/level/tiles/mur2H.png'),PhotoImage(file='sprites/level/tiles/mur3H.png')]
door=PhotoImage(file='sprites/level/tiles/door.png'); doorH=PhotoImage(file='sprites/level/tiles/doorH.png')
box=[ImageTk.PhotoImage(Image.open('sprites/level/tiles/box.png').resize((40,60))), ImageTk.PhotoImage(Image.open('sprites/level/tiles/boxH.png').resize((40,40)))]
for i in range(3):
    Var.monolith[1].append(ImageTk.PhotoImage(Image.open('sprites/props/monolith'+str(i)+'.png').resize((40,80))))
modsText=[PhotoImage(file='sprites/UI/texts/'+str(i)+'.png') for i in range(6)]
Joueur.mods=[1,1,1,1,1,1,0,0]#Dmg, mul.tir, pré, vit, crit, mult.crit, GLOCK

#-------------------------------------------------------------------------------------------------------------------|>

def init():
    global bonus
    can.delete('all')

    Joueur.wStats=Var.arsenal[0]; Joueur.stats=[0, 100, 100, 250, 100, 100, randint(0,2)]; bonus=[1,1,0]; Var.Xp=[0,1,1]; Var.monolith[0]=[]; Var.monolith[2]=False
    Var.level=0; Ennemi.index=[]; Projectile.index=[]; Combat.index=[]; Var.gStats=[time(), 0]; Var.pression=0; Joueur.mods=[1,1,1,1,1,1,0,0]
    chargement()

def main():
    global tic, fpsLimiter, animP, weapon, anim, state, bonus, angle, fps

    #Calcul angle visée libre (hors combat)
    if lInput[0] and lInput[2]:angle=pi+3*pi/4
    elif lInput[0] and lInput[3]:angle=pi/4
    elif lInput[1] and lInput[2]:angle=pi+pi/4
    elif lInput[1] and lInput[3]:angle=3*pi/4
    elif lInput[0]:angle=pi/100
    elif lInput[1]:angle=pi
    elif lInput[2]:
        if angle<pi/2 or angle>3*pi/2:angle=3*pi/2+pi/100
        else:angle=3*pi/2-pi/100
    elif lInput[3]:
        if angle<pi/2 or angle>3*pi/2:angle=pi/2-pi/100
        else:angle=pi/2+pi/100

    for i in range(len(Combat.index)):#Calcul visée auto
        if Combat.index[i].actif and Combat.index[i].Pop>0:
            target=[0,0]
            for j in range(len(Ennemi.index)):
                if Ennemi.index[j].combat==i and sqrt(((Ennemi.index[j].posX-Joueur.pos[0])**2)+((Ennemi.index[j].posY-Joueur.pos[1])**2))<sqrt(((target[0]-Joueur.pos[0])**2)+((target[1]-Joueur.pos[1])**2)):
                    try:#Y'a t'il un obstacle ? (ouai c'est moche... mais ca fonctionne !)
                        condition=True
                        if (Ennemi.index[j].posX>Joueur.pos[0]):angleP=atan((Ennemi.index[j].posY-Joueur.pos[1])/(Ennemi.index[j].posX-Joueur.pos[0]))
                        else:angleP=pi+atan((Ennemi.index[j].posY-Joueur.pos[1])/(Ennemi.index[j].posX-Joueur.pos[0]))
                        for p in range(10,int(sqrt(((Ennemi.index[j].posX-Joueur.pos[0])**2)+((Ennemi.index[j].posY-Joueur.pos[1])**2)))-10,10):
                            if Var.grille[int((Joueur.pos[1]+p*sin(angleP))/40)][int((Joueur.pos[0]+p*cos(angleP))/40)]=='0':condition=False
                        if condition:target=[Ennemi.index[j].posX,Ennemi.index[j].posY]
                    except ZeroDivisionError:pass
            if target==[0,0]:#Si aucun Ennemi.index n'est "accessible", prendre le plus proche quand même (rustine provisoire)
                for j in range(len(Ennemi.index)):
                    if Ennemi.index[j].combat==i and sqrt(((Ennemi.index[j].posX-Joueur.pos[0])**2)+((Ennemi.index[j].posY-Joueur.pos[1])**2))<sqrt(((target[0]-Joueur.pos[0])**2)+((target[1]-Joueur.pos[1])**2)):
                        target=[Ennemi.index[j].posX,Ennemi.index[j].posY]
            if (target[0]-Joueur.pos[0])!=0 and target!=[0,0]:
                if (target[0]>Joueur.pos[0]):angle=atan((target[1]-Joueur.pos[1])/(target[0]-Joueur.pos[0]))
                else:angle=pi+atan((target[1]-Joueur.pos[1])/(target[0]-Joueur.pos[0]))

    if time()-tic>1/10:#Animation
        for i in range(len(animP)):
            animP[i][0]+=anim
            if animP[i][0]>animP[i][1]:animP[i][0]=1
            elif animP[i][0]<1:animP[i][0]=animP[i][1]
        for i in range(len(Var.animO)):
            Var.animO[i][0]+=1
            if Var.animO[i][0]>Var.animO[i][1]:Var.animO[i][0]=1
        for i in range(len(Var.animE)):
            Var.animE[i][0]+=1
            if Var.animE[i][0]>Var.animE[i][1]:Var.animE[i][0]=1
        for i in range(len(Ennemi.index)):
            if Combat.index[Ennemi.index[i].combat].actif:
                if Ennemi.index[i].arme[2]>1:Ennemi.index[i].arme[2]-=1
        if Joueur.wStats[2]>1:Joueur.wStats[2]-=1
        tic=time()

    Joueur.perso[1]='Idle'; Joueur.perso[2]=0
    if lInput[0] or lInput[1] or lInput[2] or lInput[3]:Joueur.perso[1]='walk'; Joueur.perso[2]=1

    anim=1; posP=Joueur.pos[:]
    if Joueur.stats[1]>0 and state:
        if lInput[0]:
            if angle>pi/2 and angle <3*pi/2:anim=-1
            posP[0]+=(time()-Var.frame)*(Joueur.stats[3]+bonus[2])*Joueur.mods[3]
        if lInput[1]:
            if angle<pi/2 or angle>3*pi/2:anim=-1
            posP[0]-=(time()-Var.frame)*(Joueur.stats[3]+bonus[2])*Joueur.mods[3]
        if lInput[2]:posP[1]-=(time()-Var.frame)*(Joueur.stats[3]+bonus[2])*Joueur.mods[3]
        if lInput[3]:posP[1]+=(time()-Var.frame)*(Joueur.stats[3]+bonus[2])*Joueur.mods[3]

    if (Joueur.powers[0][1]==False and Var.grille[int((posP[1]+8)/40)][int((posP[0]-16)/40)]!='0' and Var.grille[int((posP[1]+8)/40)][int((posP[0]+16)/40)]!='0'
        and Var.grille[int((posP[1]+28)/40)][int((posP[0]-16)/40)]!='0' and Var.grille[int((posP[1]+28)/40)][int((posP[0]+16)/40)]!='0'): Joueur.pos=posP[:]

    Var.debordeur-=1; rustine=time()
    if lInput[4] and Joueur.stats[1]>0 and Joueur.powers[0][1]==False and not Var.monolith[2]:#Tir de l'Arme (JOUEUR)
        if (time()-Joueur.stats[0])>Joueur.wStats[6]:
            for i in range(int(Joueur.wStats[4]*bonus[1]*(Joueur.mods[1] if Joueur.wStats[11]==0 else 1))):
                disp=angle+(-((Joueur.wStats[5]*Joueur.mods[2])/2/180*pi)+random()*((Joueur.wStats[5]*Joueur.mods[2])/180*pi))
                Joueur.stats[0]=time(); Joueur.wStats[2]=3
                Projectile.index.append(Projectile(
                        Joueur.pos[0]+(Joueur.wStats[3])*cos(disp), Joueur.pos[1]+8+(Joueur.wStats[3])*sin(disp), Joueur.pos[0]+(Joueur.wStats[3])*cos(disp), 
                        Joueur.pos[1]+8+(Joueur.wStats[3])*sin(disp),disp, Joueur.wStats[7]*1.5, True, (2+(Joueur.wStats[8]*(1+((1.5-1)*Joueur.mods[5])/Joueur.wStats[9]))/10)*bonus[0],
                        Joueur.wStats[11], Joueur.wStats[12], Joueur.wStats[13]
                ))
            while time()-rustine<1/60:0==0

    for i in range(len(Combat.index)):#Déclenchement/Arrêt Combat
        Combat.index[i].startnstop()

    Adolf=[]; OlowCost=0
    for i in range(len(Orbe.index)):#Actualisation vitesse et position des orbes d'Xp
        Adolf=Orbe.index[i].move(i, Adolf)
    for i in Adolf:Orbe.index.pop(i-OlowCost); OlowCost+=1


    for i in Projectile.index:#Actualisation position Projectiles
        i.actualisation()

    Holocaust=[]; Hitlof=0; Shaw=[]; Musso=0
    for i in range(len(Projectile.index)):#Collisions Projectiles
        retour=Projectile.index[i].collision(i, Holocaust, Shaw)
        if retour[0]:Holocaust.append(i)
        Shaw+=retour[1]
    for i in range(len(Holocaust)):
        I=Holocaust[i]-Hitlof; obj=Projectile.index[I]
        nbrFragments=int(obj.nbrS*(Joueur.mods[1] if obj.friendly else 1)+(Var.pression if (obj.nbrS>0 and not obj.friendly) else 0))
        for j in range(nbrFragments):#Spawn balles à fragmentation
            predPos=(time()-obj.spawnT)*obj.vit
            while (Var.grille[int((obj.spawnY+predPos*sin(obj.angle)+20)/40)][int((obj.spawnX+predPos*cos(obj.angle))/40)]=='0'):predPos-=5
            Projectile.index.append(Projectile(
                obj.spawnX+predPos*cos(obj.angle), obj.spawnY+predPos*sin(obj.angle), 
                obj.spawnX+predPos*cos(obj.angle), obj.spawnY+predPos*sin(obj.angle),  
                obj.angle+((2*pi)/nbrFragments)*j, obj.vitS,
                obj.friendly,  (2+obj.dmgS/6 if obj.friendly else obj.dmgS/2), 0, 0, 0, obj.color, obj.outline, obj.dmgS))
        Projectile.index.pop(I); Hitlof+=1
    obj=None
    for k in range(len(Shaw)):
        for j in range(randint(5,10)*(12 if Var.level%3==0 else 1)):
            Orbe.index.append(Orbe(Ennemi.index[Shaw[k]-Musso].posX+randint(-25*(2 if Var.level%3==0 else 1),25*(2 if Var.level%3==0 else 1)), 
                        Ennemi.index[Shaw[k]-Musso].posY+randint(-25*(2 if Var.level%3==0 else 1),25*(2 if Var.level%3==0 else 1)),0,0))
        Var.lDed.append([Ennemi.index[Shaw[k]-Musso].posX, Ennemi.index[Shaw[k]-Musso].posY])
        Combat.index[Ennemi.index[Shaw[k]-Musso].combat].Pop-=1; Ennemi.index.pop(Shaw[k]-Musso); Var.gStats[1]+=1; Musso+=1

    for i in range(len(Ennemi.index)):#"IA" des Ennemis
        Ennemi.index[i].comportement()

    if lInput[-1] and Joueur.stats[4]>0:Joueur.stats[4]-=40*(time()-Var.frame)
    elif lInput[-1]==False and Joueur.stats[4]<Joueur.stats[5]:Joueur.stats[4]+=10*(time()-Var.frame)
    if Joueur.stats[4]<0:lInput[-1]=False; Joueur.stats[4]=0; Joueur.powers[Joueur.stats[6]][1]=False
    if Joueur.stats[4]>Joueur.stats[5]:Joueur.stats[4]=Joueur.stats[5]
    if lInput[-1]:
        if Joueur.stats[6]==1 and Joueur.stats[4]>0:bonus[0]=2; bonus[1]=2
        else:bonus[0]=1; bonus[1]=1
        if Joueur.stats[6]==2 and Joueur.stats[4]>0:bonus[2]=200
        else:bonus[2]=75
    else:bonus[0]=1; bonus[1]=1; bonus[2]=0

    Var.frame=time()
    if time()-Var.tac>2:Var.tac=time()

    if time()-fpsLimiter>1/60:#Affichage
        fps=1/(time()-fpsLimiter)
        fpsLimiter=time()
        if angle!=0:
            if angle<pi/2 or angle>3*pi/2:
                Joueur.perso[0]=ImageTk.PhotoImage(Image.open('sprites/perso/'+Joueur.perso[1]+str(animP[Joueur.perso[2]][0])+'.png').resize((100, 100), Image.ANTIALIAS))
                weapon=ImageTk.PhotoImage(WeaponsP[int(Joueur.wStats[0])][int(Joueur.wStats[2])-1].rotate(angle*180/pi).resize((100, 100), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
            else:
                Joueur.perso[0]=ImageTk.PhotoImage(Image.open('sprites/perso/'+Joueur.perso[1]+str(animP[Joueur.perso[2]][0])+'.png').resize((100, 100), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                weapon=ImageTk.PhotoImage(WeaponsP[int(Joueur.wStats[0])][int(Joueur.wStats[2])-1].rotate(180-angle*180/pi).resize((100, 100), Image.ANTIALIAS))
        Var.animO[0][2]=ImageTk.PhotoImage(Var.animO[0][3][Var.animO[0][0]-1].resize((100, 180)))
        for i in range(len(Var.animE)):
            Var.animE[i][2]=Var.animE[i][6][Var.animE[i][0]-1]
            Var.animE[i][3]=Var.animE[i][7][Var.animE[i][0]-1]
        for i in range(len(Ennemi.index)):#Sprites Armes Ennemies
            size=(200 if Var.level%3==0 else 100)
            if ((Ennemi.index[i].posX)**2-Joueur.pos[0]**2)!=0 and Combat.index[Ennemi.index[i].combat].actif:
                if Joueur.pos[0]>Ennemi.index[i].posX:
                    angle=atan(((Ennemi.index[i].posY)-Joueur.pos[1])/((Ennemi.index[i].posX)-Joueur.pos[0])); Ennemi.index[i].angle=angle
                    Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(angle*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                else:
                    angle=pi+atan(((Ennemi.index[i].posY)-Joueur.pos[1])/((Ennemi.index[i].posX)-Joueur.pos[0])); Ennemi.index[i].angle=angle
                    Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(180-angle*180/pi).resize((size, size), Image.ANTIALIAS))
            elif (Combat.index[Ennemi.index[i].combat].actif==False and Ennemi.index[i].posX>Joueur.pos[0]-tk.winfo_screenwidth()/2-40 and Ennemi.index[i].posX<Joueur.pos[0]+tk.winfo_screenwidth()/2+40
            and Ennemi.index[i].posY>Joueur.pos[1]-tk.winfo_screenheight()/2-40 and Ennemi.index[i].posY<Joueur.pos[1]+tk.winfo_screenheight()/2+40):
                if Joueur.pos[0]>Ennemi.index[i].posX:Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(0*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                else:Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(180-0*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))
        affichage(tk, can, lInput, curseur, state, weapon, modsText, fps, ded1, ded2, murH, mur, doorH, door, nL, map, filter, box)

        for i in Ennemi.index:i.dmgAnimEnd()

    if menuState[2]!=True:
        if state:tk.after(1, main)
        elif nL and Var.Xp[1]>Var.Xp[2]:#Menu selection mod.
            if time()-Var.modList[2]>0.33:
                if lInput[0]:Var.modList[1]+=1; Var.modList[2]=time()
                if Var.modList[1]>2:Var.modList[1]=0
                if lInput[1]:Var.modList[1]-=1; Var.modList[2]=time()
                if Var.modList[1]<0:Var.modList[1]=2
            tk.after(1, main)
        elif nL:chargement()
    else:tk.after(1, menus)

def menus():
    global menuState, bg

    if bg[1]==None or (time()-bg[5])>2:
        bg[1]=randint(int(tk.winfo_screenwidth()/2),7000-int(tk.winfo_screenwidth()/2))
        bg[2]=randint(int(tk.winfo_screenheight()/2),7000-int(tk.winfo_screenheight()/2))
        bg[5]=time()

    posP=[bg[1],bg[2]]; condition=True
    posP[0]+=bg[3]*(time()-bg[5]); posP[1]+=bg[4]*(time()-bg[5])
    if (posP[0]<7000-tk.winfo_screenwidth()/2 and posP[0]>tk.winfo_screenwidth()/2 and
        posP[1]<7000-tk.winfo_screenheight()/2 and posP[1]>tk.winfo_screenheight()/2):
        bg[1]=posP[0]; bg[2]=posP[1]; condition=False
    bg[5]=time()

    if (time()-bg[6])>10 or condition:
        bg[3]=0; bg[4]=0
        while bg[3]==0 and bg[4]==0:bg[3]=25*randint(-1,1); bg[4]=25*randint(-1,1)
        bg[6]=time()

    var=(2 if menuState[0]=='Main' else 6)
    if lInput[2] and not config and (time()-menuState[3])>0.2:menuState[3]=time(); menuState[1]-=1
    if lInput[3] and not config and (time()-menuState[3])>0.2:menuState[3]=time(); menuState[1]+=1
    if menuState[1]>var:menuState[1]=0
    if menuState[1]<0:menuState[1]=var

    if menuState[2]==True:
        if (time()-fpsLimiter)>1/60:affichageMenus(tk, can, menuState, config, bg)
        tk.after(1, menus)

def generationNiveau():
    global salles, map, state, nL

    generation=True; Var.lObj=[]; Var.lCoffre=[]; Ennemi.index=[]; Combat.index=[]; Var.lDed=[]; Orbe.index=[]; Var.level+=1
    Var.monolith[0]=[]

    if Joueur.mods[6]==1:Joueur.mods[6]=0; Joueur.wStats=Var.arsenal[5]
    if Joueur.mods[7]==1:Joueur.mods[7]=0; Joueur.stats[1]=100

    Var.modList[0]=[-1,-1,-1]
    for i in range(3):#Selection de la liste de modificateurs à proposer si lvl. up
        condition=True
        while condition:
            n=randint(0,5)
            if n not in Var.modList[0]:condition=False
        Var.modList[0][i]=n

    if Var.level%3==1 and Var.level!=1:Var.pression+=1
    while generation:#Layer du niveau
        generation=False; salles=[[[0,0] for i in range(5)] for j in range(5)]

        if Var.level%3!=0:#Niveau classique
            pos=[randint(0,4), randint(0,4)]; salles[pos[1]][pos[0]]=[1,1]
            for i in range(4):
                condition=True; var=0
                while condition:
                    posP=[pos[0], pos[1]]; var+=1
                    if randint(0,1)==0:posP[0]+=randrange(-1,2,2)#mouai, faudra m'expliquer comment marche randrange XD
                    else:posP[1]+=randrange(-1,2,2)
                    if posP[0]>=0 and posP[0]<5 and posP[1]>=0 and posP[1]<5:
                        if salles[posP[1]][posP[0]][0]==0 or (salles[posP[1]][posP[0]][0]==1 and salles[posP[1]][posP[0]][1]>2):
                            condition=False
                    if var>10:condition=False; generation=True
                pos[0]=posP[0]; pos[1]=posP[1]
                if i==0:first=posP[:]
                if i==3:salles[posP[1]][posP[0]]=[1,2]
                else:
                    salles[posP[1]][posP[0]][0]=randint(2,3)
                    if randint(0,1)==0:posP[0]+=randint(-1,1)
                    else:posP[1]+=randint(-1,1)
                    if posP[0]>=0 and posP[0]<5 and posP[1]>=0 and posP[1]<5:
                        if salles[posP[1]][posP[0]][0]==0:salles[posP[1]][posP[0]]=[1,3]
        else:#Boss
            rand=(randrange(-1,2,2), randint(0,1)); first=None
            salles[2+rand[0] if rand[1]==0 else 2][2+rand[0] if rand[1]==1 else 2]=[1,1]; salles[2][2]=[3,0]; 
            salles[2-rand[0] if rand[1]==0 else 2][2-rand[0] if rand[1]==1 else 2]=[1,2]

    Var.grille=[['0' for i in range(35*5)] for j in range(35*5)]; Var.grilleP=[['0' for i in range(35*5)] for j in range(35*5)]
    for i in range(5):#Création de la matrice
        for j in range(5):
            if salles[j][i][0]!=0:
                if salles[j][i][0]==1:
                    if salles[j][i][1]==1:Joueur.pos=[i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2]
                    elif salles[j][i][1]==2:Var.portal=[i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2]
                    elif salles[j][i][1]==3:
                        Var.lCoffre.append([True, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, 
                        ImageTk.PhotoImage(Image.open('sprites/props/coffreF.png').resize((75,75)))])
                    for o in range(i*35+12, i*35+23):
                        for p in range(j*35+12, j*35+23):Var.grille[p][o]=chr(randint(97, 105))
                if salles[j][i][0]==2:
                    for o in range(i*35+9, i*35+26):
                        for p in range(j*35+9, j*35+26):Var.grille[p][o]=chr(randint(97, 105))
                if salles[j][i][0]==3:
                        for o in range(i*35+6, i*35+29):
                            for p in range(j*35+6, j*35+29):Var.grille[p][o]=chr(randint(97, 105))
                
                if salles[j][i][0]>1 or salles[j][i][1]>2:
                    if j>0:
                        if salles[j-1][i][0]!=0 and (salles[j-1][i]!=[1,2] or [i,j]!=first) and (salles[j-1][i]!=[1,1] or [i,j]==first or Var.level%3==0):
                            for o in range(i*35+15, i*35+20):
                                for p in range(j*35-20, j*35+20):
                                    if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
                    if j<4:
                        if salles[j+1][i][0]!=0 and (salles[j+1][i]!=[1,2] or [i,j]!=first) and (salles[j+1][i]!=[1,1] or [i,j]==first or Var.level%3==0):
                            for o in range(i*35+15, i*35+20):
                                for p in range(j*35+20, j*35+50):
                                    if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
                    if i>0:
                        if salles[j][i-1][0]!=0 and (salles[j][i-1]!=[1,2] or [i,j]!=first) and (salles[j][i-1]!=[1,1] or [i,j]==first or Var.level%3==0):
                            for o in range(i*35-20, i*35+20):
                                for p in range(j*35+15, j*35+20):
                                    if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
                    if i<4:
                        if salles[j][i+1][0]!=0 and (salles[j][i+1]!=[1,2] or [i,j]!=first) and (salles[j][i+1]!=[1,1] or [i,j]==first or Var.level%3==0):
                            for o in range(i*35+20, i*35+50):
                                for p in range(j*35+15, j*35+20):
                                    if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
    n=0; Combat.index=[]
    for i in range(5):#Création des Combat.index
        for j in range(5):
            if salles[j][i][0]==2:
                rand=randint(4,6);Combat.index.append(Combat(2, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand, False))
                with open('files/roomLayers/2/'+str(randint(0,7))+'.txt', 'r') as file:
                    var=0
                    for line in file:
                        for o in range(17):
                            if line[o]=='1':Var.grille[j*(35)+9+o][i*(35)+9+var]='0'
                            if line[o]=='2':Var.grilleP[j*(35)+9+o][i*(35)+9+var]='9'; Var.grille[j*(35)+9+o][i*(35)+9+var]='0'
                        var+=1
                for o in range(rand):
                    boule=True
                    while boule:
                        posP=[randint(i*(35*40)+(35*40)/2-8*40,i*(35*40)+(35*40)/2+8*40), randint(j*(35*40)+(35*40)/2-8*40,j*(35*40)+(35*40)/2+8*40)]
                        if (Var.grille[int((posP[1]+16)/40)][int((posP[0]+16)/40)]!='0' and Var.grille[int((posP[1]+16)/40)][int((posP[0]-16)/40)]!='0'
                            and Var.grille[int((posP[1]-16)/40)][int((posP[0]+16)/40)]!='0' and Var.grille[int((posP[1]-16)/40)][int((posP[0]-16)/40)]!='0'):boule=False
                    rand=randint(0,2); Ennemi.index.append(Ennemi(n, Var.bestiaire[rand][0], posP[0], posP[1], Var.bestiaire[rand][0], Var.bestiaire[rand][1], 0, 0, Var.bestiaire[rand][2],Var.arsenal[Var.bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[Var.bestiaire[rand][3]][1]+'/'+Var.arsenal[Var.bestiaire[rand][3]][1]+str(int(Var.arsenal[Var.bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,Var.arsenal[Var.bestiaire[rand][3]][8], Var.bestiaire[rand][4], rand))
                n+=1
            if salles[j][i][0]==3 and Var.level%3!=0:#Niveau Classique
                rand=randint(6,8);Combat.index.append(Combat(3, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand, False))
                with open('files/roomLayers/3/'+str(randint(0,5))+'.txt', 'r') as file:
                    var=0
                    for line in file:
                        for o in range(23):
                            if line[o]=='1':Var.grille[j*(35)+6+o][i*(35)+6+var]='0'
                            if line[o]=='2':Var.grilleP[j*(35)+6+o][i*(35)+6+var]='9'; Var.grille[j*(35)+6+o][i*(35)+6+var]='0'
                        var+=1
                for o in range(rand):
                    boule=True
                    while boule:
                        posP=[randint(i*(35*40)+(35*40)/2-11*40,i*(35*40)+(35*40)/2+11*40), randint(j*(35*40)+(35*40)/2-11*40,j*(35*40)+(35*40)/2+11*40)]
                        if (Var.grille[int((posP[1]+16)/40)][int((posP[0]+16)/40)]!='0' and Var.grille[int((posP[1]+16)/40)][int((posP[0]-16)/40)]!='0'
                            and Var.grille[int((posP[1]-16)/40)][int((posP[0]+16)/40)]!='0' and Var.grille[int((posP[1]-16)/40)][int((posP[0]-16)/40)]!='0'):boule=False
                    rand=randint(0,2); Ennemi.index.append(Ennemi(n, Var.bestiaire[rand][0], posP[0], posP[1], Var.bestiaire[rand][0], Var.bestiaire[rand][1], 0, 0, Var.bestiaire[rand][2],Var.arsenal[Var.bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[Var.bestiaire[rand][3]][1]+'/'+Var.arsenal[Var.bestiaire[rand][3]][1]+str(int(Var.arsenal[Var.bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,Var.arsenal[Var.bestiaire[rand][3]][8], Var.bestiaire[rand][4], rand))
                n+=1

                if randint(1,2)==1:#Creation d'un monolith
                    rand=randint(6,8);Combat.index.append(Combat(3, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand, True, len(Var.monolith[0])))
                    for o in range(rand):
                        boule=True
                        while boule:
                            posP=[randint(i*(35*40)+(35*40)/2-11*40,i*(35*40)+(35*40)/2+11*40), randint(j*(35*40)+(35*40)/2-11*40,j*(35*40)+(35*40)/2+11*40)]
                            if (Var.grille[int((posP[1]+16)/40)][int((posP[0]+16)/40)]!='0' and Var.grille[int((posP[1]+16)/40)][int((posP[0]-16)/40)]!='0'
                                and Var.grille[int((posP[1]-16)/40)][int((posP[0]+16)/40)]!='0' and Var.grille[int((posP[1]-16)/40)][int((posP[0]-16)/40)]!='0'):boule=False
                        rand=randint(0,2); Ennemi.index.append(Ennemi(n, Var.bestiaire[rand][0], posP[0], posP[1], Var.bestiaire[rand][0], Var.bestiaire[rand][1], 0, 0, Var.bestiaire[rand][2],Var.arsenal[Var.bestiaire[rand][3]][:], 
                        ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[Var.bestiaire[rand][3]][1]+'/'+Var.arsenal[Var.bestiaire[rand][3]][1]+str(int(Var.arsenal[Var.bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                        time(),0,Var.arsenal[Var.bestiaire[rand][3]][8], Var.bestiaire[rand][4], rand))
                    boule=True
                    while boule:
                        posP=[6+randint(0,23), 6+randint(0,23)]
                        if Var.grille[j*35+posP[1]][i*35+posP[0]]!='0' and Var.grille[j*35+posP[1]+1][i*35+posP[0]]!='0':boule=False
                    Var.monolith[0].append([(i*35+posP[0])*40+20, (j*35+posP[1])*40, n-1, n, False, False, time()])
                    n+=1

            elif salles[j][i][0]==3:#Boss
                Combat.index.append(Combat(3, 2*(35*40)+(35*40)/2, 2*(35*40)+(35*40)/2, False, 1, False)); rand=randint(3,4)
                Ennemi.index.append(Ennemi(0, Var.bestiaire[rand][0], 2*(35*40)+(35*40)/2, 2*(35*40)+(35*40)/2, Var.bestiaire[rand][0], Var.bestiaire[rand][1], 0, 0, Var.bestiaire[rand][2],Var.arsenal[Var.bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[Var.bestiaire[rand][3]][1]+'/'+Var.arsenal[Var.bestiaire[rand][3]][1]+str(int(Var.arsenal[Var.bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,Var.arsenal[Var.bestiaire[rand][3]][8], Var.bestiaire[rand][4], rand))

    Var.monde=Image.open("sprites/level/blank.png")
    for i in range(35*5):
        for j in range(35*5):
            if Var.grilleP[j][i]=='9':Var.grille[j][i]=chr(randint(97, 105))#...
            if Var.grille[j][i]!='0':
                Image.Image.paste(Var.monde, Image.open("sprites/level/tiles/"+Var.grille[j][i]+".png"), (i*40, j*40))
            elif i>1 and i<35*5-2 and j>1 and j<35*5-2:
                if Var.grilleP[j][i]!='9':
                    if (Var.grille[j+1][i]!='0' or Var.grille[j][i-1]!='0' or Var.grille[j][i+1]!='0' or Var.grille[j+1][i+1]!='0' 
                        or Var.grille[j+1][i-1]!='0'or Var.grilleP[j][i-1]=='9' or Var.grilleP[j][i+1]=='9'):
                        Image.Image.paste(Var.monde, Image.open("sprites/level/tiles/"+str(randint(1,3))+".png"), (i*40, j*40-20)); Var.grilleP[j][i]='a'
                    if Var.grille[j-1][i]!='0':Var.grilleP[j][i]=str(randint(3,5))
    
    for i in range(35*5):#BLOC PROVISOIRE !!!!!
        for j in range(35*5):
            if i>1 and i<35*5-2 and j>1 and j<35*5-2:
                if Var.grilleP[j-1][i]=='a' and Var.grilleP[j][i]=='0' and Var.grille[j][i]=='0':Var.grilleP[j][i]=str(randint(3,5))
            if Var.grilleP[j][i]=='9':Var.grille[j][i]='0'#... ui c'est stupide

    for i in range(len(Var.monolith[0])):#Provisoire aussi, jusqu'à ce que j'ai plus la flemme...
        Var.grille[int((Var.monolith[0][i][1])/40)][int((Var.monolith[0][i][0]-20)/40)]='0'

    map=ImageTk.PhotoImage(Var.monde.resize((200, 200), Image.ANTIALIAS)); Var.monde=ImageTk.PhotoImage(Var.monde)

    state=True; nL=True
    main()

def clavier(event):
    global lInput, state, state, nL, angle, menuState, config
    var=event.keysym

    if not config or not menuState[2] or menuState[0]!='Binds':
        if var==Var.binds[0][2]:lInput[0]=True #Droite
        if var==Var.binds[1][2]:lInput[1]=True #Gauche
        if var==Var.binds[2][2]:lInput[2]=True #Haut
        if var==Var.binds[3][2]:lInput[3]=True #Bas
        if var==Var.binds[4][2]:lInput[4]=True #Tirer

        if var==Var.binds[5][2]: #Compétence
            if Joueur.stats[4]>0:Joueur.powers[Joueur.stats[6]][1]=True; lInput[-1]=True
            else:Joueur.powers[Joueur.stats[6]][1]=False; lInput[-1]=False

        if var=='Escape':
            if menuState[2]==True and menuState[0]=='Binds':saveConfig()
            elif menuState[2]!=True:menuState[2]=True; print(menuState)

        if var==Var.binds[6][2]: #Interaction

            if menuState[2]==True:
                if menuState[0]=='Main':
                    if menuState[1]==0:
                        menuState[2]=False, tk.after(5, init)
                    if menuState[1]==1:menuState[0]='Binds'; menuState[1]=0; menuState[3]=time()
                    if menuState[1]==2:tk.destroy()
                if menuState[0]=='Binds':
                    if not config and (time()-menuState[3])>0.33:config=True

            else:
                if not state and nL and Var.Xp[1]>Var.Xp[2] and time()-Var.modList[3]>0.5:
                    Var.Xp[2]+=1
                    for i in range(6):
                        if modsC[Var.modList[0][Var.modList[1]]][i]!=0:Joueur.mods[i]=Joueur.mods[i]*modsC[Var.modList[0][Var.modList[1]]][i]
                    Joueur.mods[6]=max(Joueur.mods[6],modsC[Var.modList[0][Var.modList[1]]][6]); Joueur.mods[7]=max(modsC[Var.modList[0][Var.modList[1]]][7],Joueur.mods[7])
                Var.modList[0]=[-1,-1,-1]
                for i in range(3):#Selection de la nouvelle liste de modificateurs à proposer si lvl. up
                    condition=True
                    while condition:
                        n=randint(0,5)
                        if n not in Var.modList[0]:condition=False
                    Var.modList[0][i]=n

                if Joueur.stats[1]==0 and state:state=False; nL=False; init()
                if Joueur.pos[0]>Var.portal[0]-50 and Joueur.pos[0]<Var.portal[0]+50 and Joueur.pos[1]>Var.portal[1]-90 and Joueur.pos[1]<Var.portal[1]+90:state=False; Var.modList[3]=time()
                else:
                    for i in range(len(Var.lObj)):
                        if Joueur.pos[0]>Var.lObj[i][2]-50 and Joueur.pos[0]<Var.lObj[i][2]+50 and Joueur.pos[1]>Var.lObj[i][3]-50 and Joueur.pos[1]<Var.lObj[i][3]+50:
                            Var.lObj.append([Joueur.wStats[0], Joueur.wStats[1], Joueur.pos[0], Joueur.pos[1], 
            ImageTk.PhotoImage(Image.open('sprites/armes/'+Joueur.wStats[1]+'/'+Joueur.wStats[1]+str(int(Joueur.wStats[2]))+'.png').resize((100, 100), Image.ANTIALIAS))])
                            Joueur.wStats=Var.arsenal[int(Var.lObj[i][0])]; Var.lObj.pop(i)
                    for i in range(len(Var.lCoffre)):
                        if Joueur.pos[0]>Var.lCoffre[i][1]-50 and Joueur.pos[0]<Var.lCoffre[i][1]+50 and Joueur.pos[1]>Var.lCoffre[i][2]-50 and Joueur.pos[1]<Var.lCoffre[i][2]+50 and Var.lCoffre[i][0]:
                            var=randint(0,7); Var.lObj.append([var, Var.arsenal[var][1], Var.lCoffre[i][1]+randint(-10,10), Var.lCoffre[i][2]+randint(-10,10), 
                            ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[var][1]+'/'+Var.arsenal[var][1]+str(int(Joueur.wStats[2]))+'.png').resize((100, 100), Image.ANTIALIAS))])
                            Var.lCoffre[i][0]=False; Var.lCoffre[i][3]=ImageTk.PhotoImage(Image.open('sprites/props/coffreO.png').resize((75,75)))
                    for i in range(len(Var.monolith[0])):
                        if (Joueur.pos[0]>Var.monolith[0][i][0]-50 and Joueur.pos[0]<Var.monolith[0][i][0]+50 and Joueur.pos[1]>Var.monolith[0][i][1]-50 and Joueur.pos[1]<Var.monolith[0][i][1]+50 
                            and Combat.index[Var.monolith[0][i][2]].Pop==0 and not Var.monolith[0][i][4]):
                            Var.monolith[0][i][4]=True
    
    else:
        config=False
        if var!='Escape':Var.binds[menuState[1]][2]=var

def clavierRelease(event):
    global lInput
    var=event.keysym

    if var==Var.binds[0][2]:lInput[0]=False
    if var==Var.binds[1][2]:lInput[1]=False
    if var==Var.binds[2][2]:lInput[2]=False
    if var==Var.binds[3][2]:lInput[3]=False
    if var==Var.binds[4][2]:lInput[4]=False

    if var==Var.binds[5][2]:Joueur.powers[Joueur.stats[6]][1]=False; lInput[-1]=False

def twin(event):
    global curseur

    if Joueur.stats[1]>0:curseur=[event.x, event.y]

def saveConfig():
    with open(environ['LOCALAPPDATA']+"\\LoneStickShooter\\binds.csv", 'w') as file:
        save=writer(file)
        save.writerows(Var.binds)

    menuState[0]='Main'; menuState[1]=1

def chargement():
    can.delete('all')
    can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, text='CHARGEMENT...', 
                    font=('Ubuntu', 45), fill='white', anchor='center')
    can.update_idletasks()#beurk
    tk.after(160,generationNiveau)

#Récupération / Création des fichiers de sauvegarde
if path.exists(environ['LOCALAPPDATA']+"\\LoneStickShooter"):
    lecteur=reader(open(environ['LOCALAPPDATA']+"\\LoneStickShooter\\binds.csv", 'r'))
    for line in lecteur:
        if line!=[]:Var.binds.append(line)
    print(environ['LOCALAPPDATA']+"\\LoneStickShooter\\binds.csv")
else:
    lecteur=reader(open('files/config/binds.csv', 'r'))
    for line in lecteur:
        if line!=[]:Var.binds.append(line)
    makedirs(environ['LOCALAPPDATA']+"\\LoneStickShooter")
    saveConfig()

can=Canvas(height=tk.winfo_screenheight(), width=tk.winfo_screenwidth(), bg='black')
can.focus_set()
can.bind("<Key>", clavier); can.bind("<KeyRelease>", clavierRelease)
menus()
can.pack()

tk.mainloop()