from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk
from math import cos, sin, atan, pi, sqrt
from random import randint, randrange, random
from time import time
from csv import reader

tk=Tk()
tk.attributes('-fullscreen', True)
tk.iconbitmap('sprites/UI/icone.ico')

'''
Déclaration des variables, tout ne marche qu'avec des variables global (vu que je n'utilise pas de classe je sais pas
trop si c'est possible de s'en passer...)
'''
tic=time(); frame=time(); fpsLimiter=time(); animP=[[1,5],[1,6]]; state=False; lObj=[]; level=0; tac=time(); lCoffre=[]
lInput=[False, False, False, False, False, False]; pos=[-50, -50]; anim=1; wStats=[0, 'FAMAS', 1]; lText=[]
lProj=[]; salles=[]; grille=[]; grilleP=[]; portal=[None, None]; debordeur=0; modList=[[], 0, time(), None]
Combats=[]; ennemis=[]; gStats=[time(), 0]; nL=True; pression=0; angle=pi/100; fps=0
pStats=[0, 100, 100, 250, 100, 100, randint(0,2)]; bonus=[1,1,0]; lXp=[]; Xp=[0,1,1]
animE=[[1,4,None,None,'troupierIdle',100, [], []],[1,6,None,None,'troupierWalk',100, [], []],[1,6,None,None,'troupierWalkR',100, [], []],
    [1,4,None,None,'gunnerIdle',100, [], []],[1,6,None,None,'gunnerWalk',100, [], []],[1,6,None,None,'gunnerWalkR',100, [], []],
    [1,4,None,None,'marksmanIdle',100, [], []],[1,6,None,None,'marksmanWalk',100, [], []],[1,6,None,None,'marksmanWalkR',100, [], []],
    [1,4,None,None,'gunnerIdle',200, [], []],[1,6,None,None,'gunnerWalk',200, [], []],[1,6,None,None,'gunnerWalkR',200, [], []],
    [1,4,None,None,'marksmanIdle',200, [], []],[1,6,None,None,'marksmanWalk',200, [], []],[1,6,None,None,'marksmanWalkR',200, [], []]]
filter=ImageTk.PhotoImage(Image.open('sprites/UI/filter.png').resize((int(tk.winfo_screenwidth()/2), int(tk.winfo_screenheight()))))

powers=[[False, False, ImageTk.PhotoImage(Image.open('sprites/perso/shield.png').resize((100, 100)))],
        [False, False, ImageTk.PhotoImage(Image.open('sprites/perso/fire.png').resize((100, 100)))],
        [True, False, ImageTk.PhotoImage(Image.open('sprites/perso/wings.png').resize((100, 100)))]]

perso=[None, 'Idle', 0]; weapon=None; monde=None; map=None

for i in range(len(animE)):#Découpe des Sprite Sheets
    for j in range(animE[i][1]):
        animE[i][6].append(ImageTk.PhotoImage(
Image.open('sprites/ennemies/'+animE[i][4]+'.png').crop((0+24*(j),0,24+24*(j),24)).resize((animE[i][5], animE[i][5]))))
        animE[i][7].append(ImageTk.PhotoImage(
Image.open('sprites/ennemies/'+animE[i][4]+'.png').crop((0+24*(j),0,24+24*(j),24)).resize((animE[i][5], animE[i][5])).transpose(Image.FLIP_LEFT_RIGHT)))

modsC=[]; lecteur=reader(open('files/mods.csv', 'r'))
for line in lecteur:modsC.append(line)
for i in range(len(modsC)):
    for j in range(len(modsC[i])):modsC[i][j]=float(modsC[i][j])
bestiaire=[]; lecteur=reader(open('files/ennemies.csv','r'))
for line in lecteur:bestiaire.append(line)
for i in bestiaire:
    for j in range(len(i)):
        try:i[j]=int(i[j])
        except ValueError:pass
arsenal=[]; wSprites={}; lecteur=reader(open('files/weapons.csv','r'))
for line in lecteur:arsenal.append(line)
for i in arsenal:
    for j in range(len(i)):
        try:i[j]=float(i[j])
        except ValueError:pass
wStats=arsenal[0]

WeaponsP=[[Image.open('sprites/armes/'+arsenal[i][1]+'/'+arsenal[i][1]+str(j)+'.png')
           for j in range(1,4)] for i in range(len(arsenal))]
animO=[[1,4,None, [Image.open('sprites/portal/'+str(i)+'.png') for i in range(1,5)]]]

mur=[PhotoImage(file='sprites/level/tiles/1.png'),PhotoImage(file='sprites/level/tiles/2.png'),PhotoImage(file='sprites/level/tiles/3.png')]
murH=[PhotoImage(file='sprites/level/tiles/mur1H.png'),PhotoImage(file='sprites/level/tiles/mur2H.png'),PhotoImage(file='sprites/level/tiles/mur3H.png')]
door=PhotoImage(file='sprites/level/tiles/door.png'); doorH=PhotoImage(file='sprites/level/tiles/doorH.png')
ded1=ImageTk.PhotoImage(Image.open('sprites/ennemies/troupierDed.png').resize((100,100)))
ded2=ImageTk.PhotoImage(Image.open('sprites/ennemies/troupierDed.png').resize((200,200))); lDed=[]
modsText=[PhotoImage(file='sprites/UI/texts/'+str(i)+'.png') for i in range(6)]
mods=[1,1,1,1,1,1,0,0]#Dmg, mul.tir, pré, vit, crit, mult.crit, GLOCK

'''
fonction dont l'unique rôle est de remettre les variables à leurs valeurs initialle lors du début d'une nouvelle run
appelle la fonction chargement() à la fin de son execution 
'''
def init():
    global wStats, pStats, level, ennemis, lProj, Combats, gStats, bonus, pression, mods, Xp
    can.delete('all')

    wStats=arsenal[0]; pStats=[0, 100, 100, 250, 100, 100, randint(0,2)]; bonus=[1,1,0]; Xp=[0,1,1]
    level=0; ennemis=[]; lProj=[]; Combats=[]; gStats=[time(), 0]; pression=0; mods=[1,1,1,1,1,1,0,0]
    chargement()

'''
Comme son nom l'indique, cette fonction s'occuppe d'afficher l'interface
'''
def affichage():
    global perso, lProj, grilleP, pos, portal, animO, lObj, lCoffre, lDed, ded1, ded2, powers, modList
    can.delete('all')

    can.create_image(
        -pos[0]+(tk.winfo_screenwidth()/2), -pos[1]+(tk.winfo_screenheight()/2), image=monde, anchor='nw'
    )
    can.create_image(portal[0]-pos[0]+(tk.winfo_screenwidth()/2), portal[1]-pos[1]+(tk.winfo_screenheight()/2), 
                    image=animO[0][2], anchor='center')
    if pos[0]>portal[0]-50 and pos[0]<portal[0]+50 and pos[1]>portal[1]-90 and pos[1]<portal[1]+90:
        can.create_text(portal[0]-pos[0]+(tk.winfo_screenwidth()/2), portal[1]-110-pos[1]+(tk.winfo_screenheight()/2), 
                        text='Entrer dans le portail', anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(lDed)):
        can.create_image(lDed[i][0]-pos[0]+(tk.winfo_screenwidth()/2), lDed[i][1]-pos[1]+(tk.winfo_screenheight()/2), image=(ded1 if level%3!=0 else ded2), anchor='center')
    for i in range(len(lXp)):
        can.create_oval(lXp[i][0]-4-pos[0]+(tk.winfo_screenwidth()/2), lXp[i][1]-4-pos[1]+(tk.winfo_screenheight()/2),
                        lXp[i][0]+4-pos[0]+(tk.winfo_screenwidth()/2), lXp[i][1]+4-pos[1]+(tk.winfo_screenheight()/2), outline='green', fill='lightgreen')
    CheikPoint=[]
    for j in range(int((pos[1]-tk.winfo_screenheight()/2)/40), int((pos[1]+20)/40+3)):
        for i in range(len(ennemis)):
            if ennemis[i][3]<(j)*40 and i not in CheikPoint:
                if ennemis[i][2]<pos[0]:can.create_image(ennemis[i][2]-pos[0]+(tk.winfo_screenwidth()/2), ennemis[i][3]-pos[1]+(tk.winfo_screenheight()/2), 
                                image=animE[ennemis[i][4]][2], anchor='center'); CheikPoint.append(i)
                else:can.create_image(ennemis[i][2]-pos[0]+(tk.winfo_screenwidth()/2), ennemis[i][3]-pos[1]+(tk.winfo_screenheight()/2), 
                                image=animE[ennemis[i][4]][3], anchor='center'); CheikPoint.append(i)
                can.create_image(ennemis[i][2]-pos[0]+(tk.winfo_screenwidth()/2), ennemis[i][3]-pos[1]+(tk.winfo_screenheight()/2)+8, image=ennemis[i][10], anchor='center')
        for i in range(int((pos[0]-tk.winfo_screenwidth()/2)/40-40), int((pos[0]+tk.winfo_screenwidth()/2)/40+40)):
            if i>3 and i<7000/40-3 and j>3 and j<7000/40-3:
                if ord(grilleP[j][i])<97:
                    if int(grilleP[j][i])>=3 and int(grilleP[j][i])<=5:
                        if grilleP[j+1][i]=='a':
                            can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=murH[int(grilleP[j][i])-3], anchor='nw')
                        else:can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=mur[int(grilleP[j][i])-3], anchor='nw')
                if grilleP[j][i]=='2':
                    if grille[j+1][i]=='0' or grilleP[j+1][i]=='2':
                        can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=doorH, anchor='nw')
                    else:can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=door, anchor='nw')

    for i in range(len(lCoffre)):
        can.create_image(lCoffre[i][1]-pos[0]+(tk.winfo_screenwidth()/2), lCoffre[i][2]-pos[1]+(tk.winfo_screenheight()/2), image=lCoffre[i][3], anchor='center')
        if pos[0]>lCoffre[i][1]-50 and pos[0]<lCoffre[i][1]+50 and pos[1]>lCoffre[i][2]-50 and pos[1]<lCoffre[i][2]+50 and lCoffre[i][0]:
            can.create_text(lCoffre[i][1]-pos[0]+(tk.winfo_screenwidth()/2), lCoffre[i][2]-pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Ouvrir Coffre', anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(lObj)):
        can.create_image(lObj[i][2]-pos[0]+(tk.winfo_screenwidth()/2), lObj[i][3]-pos[1]+(tk.winfo_screenheight()/2), image=lObj[i][4], anchor='center')
        if pos[0]>lObj[i][2]-50 and pos[0]<lObj[i][2]+50 and pos[1]>lObj[i][3]-50 and pos[1]<lObj[i][3]+50:
            can.create_text(lObj[i][2]-pos[0]+(tk.winfo_screenwidth()/2), lObj[i][3]-pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Ramasser : '+lObj[i][1], anchor='center', fill='blue', font=('Arial', 12))

    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=perso[0], anchor='center')
    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+8, image=weapon, anchor='center')
    for i in range(len(powers)):
        if powers[i][1]:can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=powers[i][2], anchor='center')

    for j in range(int((pos[1]+20)/40), int((pos[1]+tk.winfo_screenheight()/2)/40+3)):
        for i in range(len(ennemis)):
            if ennemis[i][3]<(j)*40 and i not in CheikPoint:
                if ennemis[i][2]<pos[0]:can.create_image(ennemis[i][2]-pos[0]+(tk.winfo_screenwidth()/2), ennemis[i][3]-pos[1]+(tk.winfo_screenheight()/2), 
                                image=animE[ennemis[i][4]][2], anchor='center'); CheikPoint.append(i)
                else:can.create_image(ennemis[i][2]-pos[0]+(tk.winfo_screenwidth()/2), ennemis[i][3]-pos[1]+(tk.winfo_screenheight()/2), 
                                image=animE[ennemis[i][4]][3], anchor='center'); CheikPoint.append(i)
                can.create_image(ennemis[i][2]-pos[0]+(tk.winfo_screenwidth()/2), ennemis[i][3]-pos[1]+(tk.winfo_screenheight()/2)+8, image=ennemis[i][10], anchor='center')
        for i in range(int((pos[0]-tk.winfo_screenwidth()/2)/40-40), int((pos[0]+tk.winfo_screenwidth()/2)/40+40)):
            if i>3 and i<7000/40-3 and j>3 and j<7000/40-3:
                if ord(grilleP[j][i])<97:
                    if int(grilleP[j][i])>=3 and int(grilleP[j][i])<=5:
                        if grilleP[j+1][i]=='a':
                            can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=murH[int(grilleP[j][i])-3], anchor='nw')
                        else:can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=mur[int(grilleP[j][i])-3], anchor='nw')
                if grilleP[j][i]=='2':
                    if grille[j+1][i]=='0' or grilleP[j+1][i]=='2':
                        can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=doorH, anchor='nw')
                    else:can.create_image(i*40-pos[0]+(tk.winfo_screenwidth()/2), j*40-pos[1]+(tk.winfo_screenheight()/2)-20, image=door, anchor='nw')

    for i in range(len(lProj)):#Affichage Projectiles
        if wStats[-1]==0 or lProj[i][7]==False:
            can.create_oval(
                lProj[i][0]-lProj[i][8]-pos[0]+(tk.winfo_screenwidth()/2), lProj[i][1]-lProj[i][8]-pos[1]+(tk.winfo_screenheight()/2), 
                lProj[i][0]+lProj[i][8]-pos[0]+(tk.winfo_screenwidth()/2), lProj[i][1]+lProj[i][8]-pos[1]+(tk.winfo_screenheight()/2),
                fill=lProj[i][9], outline=lProj[i][10]
            )
    Holocost=[]; Hitlof=0
    for i in range(len(lText)):
        can.create_text(lText[i][0]-pos[0]+(tk.winfo_screenwidth()/2), lText[i][1]-pos[1]+(tk.winfo_screenheight()/2), 
                        text=lText[i][3], fill=lText[i][2], font=('Arial', lText[i][6]), anchor='center')
        if time()-lText[i][4]>lText[i][5]:Holocost.append(i)
    for i in range(len(Holocost)):lText.pop(Holocost[i]-Hitlof); Hitlof+=1

    if lInput[4] and pStats[1]>0 and powers[0][1]==False and wStats[-1]==1:#Affichage Laser !
        n=2
        if ((tk.winfo_screenwidth()/2)-curseur[0])!=0:#Calcul angle
            if curseur[0]>tk.winfo_screenwidth()/2:angle=atan(((tk.winfo_screenheight()/2)-curseur[1])/((tk.winfo_screenwidth()/2)-curseur[0]))
            else:angle=pi+atan(((tk.winfo_screenheight()/2)-curseur[1])/((tk.winfo_screenwidth()/2)-curseur[0]))
        else:angle=0
        while grille[int((pos[1]+(wStats[3]+n)*sin(angle))/40)][int((pos[0]+(wStats[3]+n)*cos(angle))/40)]!='0':n+=2
        can.create_line(tk.winfo_screenwidth()/2+wStats[3]*cos(angle), tk.winfo_screenheight()/2+wStats[3]*sin(angle), 
                        tk.winfo_screenwidth()/2+(wStats[3]+n)*cos(angle), tk.winfo_screenheight()/2+(wStats[3]+n)*sin(angle),fill='lightblue', width=4)

    if pStats[1]>0 and nL:#UI partie en cours
        if state:#Jeu normal
            can.create_image(tk.winfo_screenwidth()-75, 75, image=map, anchor='ne')
            can.create_rectangle(tk.winfo_screenwidth()-275, 75, tk.winfo_screenwidth()-75, 275, outline='brown', width=4)
            can.create_oval(tk.winfo_screenwidth()-275+(pos[0]/7000*200)-3, 75+(pos[1]/7000*200)-3,
                            tk.winfo_screenwidth()-275+(pos[0]/7000*200)+3, 75+(pos[1]/7000*200)+3, fill='pink')
            can.create_oval(tk.winfo_screenwidth()-275+(portal[0]/7000*200)-3, 75+(portal[1]/7000*200)-3,
                            tk.winfo_screenwidth()-275+(portal[0]/7000*200)+3, 75+(portal[1]/7000*200)+3, fill='blue')
            can.create_text(tk.winfo_screenwidth()-275, 300, text='Zone : '+str(level), anchor='w', fill='gainsboro', font=('Ubuntu', 16))
            can.create_rectangle(75, 75, 102, 177, outline='white', width=3)
            can.create_rectangle(76, 76+(100/200*(200-Xp[0])), 101, 177, fill='lightgreen', width=0)
            if Xp[1]>Xp[2]:can.create_text(88.5, 195, text='Niv. Sup !', anchor='center', fill='gainsboro', font=('Ubuntu', 16))
            can.create_text(75+(27/2), 75+51, text=str(Xp[1]), fill='white', font=('Ubuntu', 22), anchor='center')
            can.create_rectangle(165, tk.winfo_screenheight()-75, 565, tk.winfo_screenheight()-100, width=3, outline='white', fill='black')
            can.create_rectangle(166, tk.winfo_screenheight()-76, 165+398/pStats[2]*pStats[1], tk.winfo_screenheight()-99, width=0, fill='brown')
            can.create_text(365, tk.winfo_screenheight()-87.5, text=str(pStats[1])+' / '+str(pStats[2]), anchor='center', fill='white')
            can.create_rectangle(165, tk.winfo_screenheight()-107, 565, tk.winfo_screenheight()-115, width=0, fill='white')
            can.create_rectangle(166, tk.winfo_screenheight()-107, 165+398/pStats[5]*pStats[4], tk.winfo_screenheight()-115, width=0, fill='lightblue')
            can.create_oval(75,tk.winfo_screenheight()-107-50, 175, tk.winfo_screenheight()-107+50, fill='gainsboro', outline='brown')
            can.create_image(125, tk.winfo_screenheight()-107, image=powers[pStats[6]][2], anchor='center')
            if level%3==0 and Combats[0][3]:#Barre de vie du Boss
                try:
                    can.create_rectangle(tk.winfo_screenwidth()/2-300, 75, tk.winfo_screenwidth()/2+300, 115, outline='gainsboro')
                    can.create_rectangle(tk.winfo_screenwidth()/2-299, 76, tk.winfo_screenwidth()/2-299+598*(ennemis[0][5]/bestiaire[ennemis[0][-1]][1]),
                                        114, width=0, fill='brown')
                except IndexError:pass
        else:#Menu Selection mod.
            can.create_image(tk.winfo_screenwidth()/4, 0, image=filter, anchor='nw')
            can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/6, text='NIV.  SUP.  !', fill='blue', font=('Papyrus', 34))
            for i in range(3):
                can.create_rectangle(tk.winfo_screenwidth()/2-137.5+i*100, (tk.winfo_screenheight()-75)/2,
                                     tk.winfo_screenwidth()/2-137.5+i*100+75, (tk.winfo_screenheight()+75)/2,
                                     outline=('red' if modList[1]==i else 'black'))
            can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+250, image=modsText[modList[0][modList[1]]], anchor='center')

    else:#UI mort
        can.create_image(tk.winfo_screenwidth()/4, 0, image=filter, anchor='nw')
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/6, text='TU   ES   MORT', fill='red', font=('Papyrus', 28))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2-100, text='Zone atteinte : '+str(level), 
                        fill='White', font=('Ubuntu', 18))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, text='Ennemis tués : '+str(gStats[1]), 
                        fill='White', font=('Ubuntu', 18))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+100, text='Durée de la run : '+str((gStats[0])/60)[:4]+'min', 
                        fill='White', font=('Ubuntu', 18))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()-tk.winfo_screenheight()/6, text='-[Interagir] pour recommencer-', 
                        fill='white', font=('Ubuntu', 22))

    can.create_text(10,10,text=str(int(fps))+' fps', fill=('green' if fps>40 else ('orange' if fps>20 else 'red')), anchor='nw')

'''
Cette fonction gére à peu près tout, elle s'appelle elle même à la fin de chaque execution, exepté si un chargement est
en cours (le booléen "state" s'occupe de cela)
Appelle generationNiveau() quand le joueur traverse un portail
Appelle la fonction affichage() toutes les 1/60 secondes, ou plus bien sur dans les moments les plus critiques
'''
def main():
    global tic, frame, fpsLimiter, animP, perso, weapon, anim, animO, pStats, lProj, wStats, pos, state, ennemis, animE
    global lText, tac, debordeur, lDed, gStats, powers, bonus, angle, lXp, Xp, modList, fps

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

    for i in range(len(Combats)):#Calcul visée auto
        if Combats[i][3] and Combats[i][4]>0:
            target=[0,0]
            for j in range(len(ennemis)):
                if ennemis[j][0]==i and sqrt(((ennemis[j][2]-pos[0])**2)+((ennemis[j][3]-pos[1])**2))<sqrt(((target[0]-pos[0])**2)+((target[1]-pos[1])**2)):
                    try:#Y'a t'il un obstacle ? (ouai c'est moche... mais ca fonctionne !)
                        condition=True
                        if (ennemis[j][2]>pos[0]):angleP=atan((ennemis[j][3]-pos[1])/(ennemis[j][2]-pos[0]))
                        else:angleP=pi+atan((ennemis[j][3]-pos[1])/(ennemis[j][2]-pos[0]))
                        for p in range(10,int(sqrt(((ennemis[j][2]-pos[0])**2)+((ennemis[j][3]-pos[1])**2)))-10,10):
                            if grille[int((pos[1]+p*sin(angleP))/40)][int((pos[0]+p*cos(angleP))/40)]=='0':condition=False
                        if condition:target=[ennemis[j][2],ennemis[j][3]]
                    except ZeroDivisionError:pass
            if target==[0,0]:#Si aucun ennemis n'est "accessible", prendre le plus proche quand même (rustine provisoire)
                for j in range(len(ennemis)):
                    if ennemis[j][0]==i and sqrt(((ennemis[j][2]-pos[0])**2)+((ennemis[j][3]-pos[1])**2))<sqrt(((target[0]-pos[0])**2)+((target[1]-pos[1])**2)):
                        target=[ennemis[j][2],ennemis[j][3]]
            if (target[0]-pos[0])!=0 and target!=[0,0]:
                if (target[0]>pos[0]):angle=atan((target[1]-pos[1])/(target[0]-pos[0]))
                else:angle=pi+atan((target[1]-pos[1])/(target[0]-pos[0]))

    if time()-tic>1/10:#Animation
        for i in range(len(animP)):
            animP[i][0]+=anim
            if animP[i][0]>animP[i][1]:animP[i][0]=1
            elif animP[i][0]<1:animP[i][0]=animP[i][1]
        for i in range(len(animO)):
            animO[i][0]+=1
            if animO[i][0]>animO[i][1]:animO[i][0]=1
        for i in range(len(animE)):
            animE[i][0]+=1
            if animE[i][0]>animE[i][1]:animE[i][0]=1
        for i in range(len(ennemis)):
            if Combats[ennemis[i][0]][3]:
                if ennemis[i][9][2]>1:ennemis[i][9][2]-=1
        if wStats[2]>1:wStats[2]-=1
        tic=time()

    perso[1]='Idle'; perso[2]=0
    if lInput[0] or lInput[1] or lInput[2] or lInput[3]:perso[1]='walk'; perso[2]=1

    anim=1; posP=pos[:]
    if pStats[1]>0 and state:
        if lInput[0]:
            if angle>pi/2 and angle <3*pi/2:anim=-1
            posP[0]+=(time()-frame)*(pStats[3]+bonus[2])*mods[3]
        if lInput[1]:
            if angle<pi/2 or angle>3*pi/2:anim=-1
            posP[0]-=(time()-frame)*(pStats[3]+bonus[2])*mods[3]
        if lInput[2]:posP[1]-=(time()-frame)*(pStats[3]+bonus[2])*mods[3]
        if lInput[3]:posP[1]+=(time()-frame)*(pStats[3]+bonus[2])*mods[3]

    if (powers[0][1]==False and grille[int((posP[1]+8)/40)][int((posP[0]-16)/40)]!='0' and grille[int((posP[1]+8)/40)][int((posP[0]+16)/40)]!='0'
        and grille[int((posP[1]+28)/40)][int((posP[0]-16)/40)]!='0' and grille[int((posP[1]+28)/40)][int((posP[0]+16)/40)]!='0'): pos=posP[:]

    debordeur-=1; rustine=time()
    if lInput[4] and pStats[1]>0 and powers[0][1]==False:#Tir de l'Arme (JOUEUR)
        if (time()-pStats[0])>wStats[6]:
            for i in range(int(wStats[4]*bonus[1]*mods[1])):
                disp=angle+(-((wStats[5]*mods[2])/2/180*pi)+random()*((wStats[5]*mods[2])/180*pi))
                pStats[0]=time(); wStats[2]=3
                lProj.append([
                        pos[0]+(wStats[3])*cos(disp), pos[1]+8+(wStats[3])*sin(disp), pos[0]+(wStats[3])*cos(disp), pos[1]+8+(wStats[3])*sin(disp),
                        disp, wStats[7]*1.5, time(), True, 3*bonus[0], 'black', 'black'
                ])
            while time()-rustine<1/60:0==0

    for i in range(len(Combats)):#Déclenchement/Arrêt Combats
        if (Combats[i][3]==False and Combats[i][0]==2 and Combats[i][4]>0 and pos[0]>Combats[i][1]-8*40 and pos[0]<Combats[i][1]+8*40
        and pos[1]>Combats[i][2]-8*40 and pos[1]<Combats[i][2]+8*40-20):
            Combats[i][3]=True; tac=0
            for j in range(5):
                if grille[int(Combats[i][2]/40)-9][int(Combats[i][1]/40)-2+j]!='0':
                    grille[int(Combats[i][2]/40)-9][int(Combats[i][1]/40)-2+j]='0';grilleP[int(Combats[i][2]/40)-9][int(Combats[i][1]/40)-2+j]='2'
                if grille[int(Combats[i][2]/40)+9][int(Combats[i][1]/40)-2+j]!='0':
                    grille[int(Combats[i][2]/40)+9][int(Combats[i][1]/40)-2+j]='0';grilleP[int(Combats[i][2]/40)+9][int(Combats[i][1]/40)-2+j]='2'
                if grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-9]!='0':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-9]='0';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-9]='2'
                if grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+9]!='0':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+9]='0';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+9]='2'
        if (Combats[i][3]==False and Combats[i][0]==3 and Combats[i][4]>0 and pos[0]>Combats[i][1]-11*40 and pos[0]<Combats[i][1]+11*40
        and pos[1]>Combats[i][2]-11*40 and pos[1]<Combats[i][2]+11*40-20):
            Combats[i][3]=True; tac=0
            for j in range(5):
                if grille[int(Combats[i][2]/40)-12][int(Combats[i][1]/40)-2+j]!='0':
                    grille[int(Combats[i][2]/40)-12][int(Combats[i][1]/40)-2+j]='0';grilleP[int(Combats[i][2]/40)-12][int(Combats[i][1]/40)-2+j]='2'
                if grille[int(Combats[i][2]/40)+12][int(Combats[i][1]/40)-2+j]!='0':
                    grille[int(Combats[i][2]/40)+12][int(Combats[i][1]/40)-2+j]='0';grilleP[int(Combats[i][2]/40)+12][int(Combats[i][1]/40)-2+j]='2'
                if grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-12]!='0':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-12]='0';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-12]='2'
                if grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+12]!='0':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+12]='0';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+12]='2'
        if Combats[i][3] and Combats[i][4]==0:
            Combats[i][3]=False; lProj=[]
            for j in range(5):
                if grilleP[int(Combats[i][2]/40)-9][int(Combats[i][1]/40)-2+j]=='2':
                    grille[int(Combats[i][2]/40)-9][int(Combats[i][1]/40)-2+j]='1';grilleP[int(Combats[i][2]/40)-9][int(Combats[i][1]/40)-2+j]='0'
                if grilleP[int(Combats[i][2]/40)+9][int(Combats[i][1]/40)-2+j]=='2':
                    grille[int(Combats[i][2]/40)+9][int(Combats[i][1]/40)-2+j]='1';grilleP[int(Combats[i][2]/40)+9][int(Combats[i][1]/40)-2+j]='0'
                if grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-9]=='2':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-9]='1';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-9]='0'
                if grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+9]=='2':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+9]='1';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+9]='0'
                if grilleP[int(Combats[i][2]/40)-12][int(Combats[i][1]/40)-2+j]=='2':
                    grille[int(Combats[i][2]/40)-12][int(Combats[i][1]/40)-2+j]='1';grilleP[int(Combats[i][2]/40)-12][int(Combats[i][1]/40)-2+j]='0'
                if grilleP[int(Combats[i][2]/40)+12][int(Combats[i][1]/40)-2+j]=='2':
                    grille[int(Combats[i][2]/40)+12][int(Combats[i][1]/40)-2+j]='1';grilleP[int(Combats[i][2]/40)+12][int(Combats[i][1]/40)-2+j]='0'
                if grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-12]=='2':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-12]='1';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)-12]='0'
                if grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+12]=='2':
                    grille[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+12]='1';grilleP[int(Combats[i][2]/40)-2+j][int(Combats[i][1]/40)+12]='0'

    Adolf=[]; OlowCost=0
    for i in range(len(lXp)):#Actualisation vitesse et position des orbes d'Xp
        if sqrt((pos[0]-lXp[i][0])**2+(pos[1]-lXp[i][1])**2)<25:
            Adolf.append(i); Xp[0]+=1.2
            if Xp[0]>=200:Xp[0]-=200; Xp[1]+=1
        elif sqrt((pos[0]-lXp[i][0])**2+(pos[1]-lXp[i][1])**2)<300:#calcul vitesse en fonction de la distance au joueur
            #Calcul de l'angle entre le joueur et l'orbe
            angleO=None
            if (lXp[i][0]>pos[0]):angleO=atan((lXp[i][1]-pos[1])/(lXp[i][0]-pos[0]))
            else:angleO=pi+atan((lXp[i][1]-pos[1])/(lXp[i][0]-pos[0]))
            #Attribution de la nouvelle vitesse
            lXp[i][2]=-(300-sqrt((pos[0]-lXp[i][0])**2+(pos[1]-lXp[i][1])**2))*1.5*cos(angleO)
            lXp[i][3]=-(300-sqrt((pos[0]-lXp[i][0])**2+(pos[1]-lXp[i][1])**2))*1.5*sin(angleO)
        else:lXp[i][2], lXp[i][3]=0,0
        lXp[i][0]+=lXp[i][2]*(time()-lXp[i][4]); lXp[i][1]+=lXp[i][3]*(time()-lXp[i][4])
        lXp[i][4]=time()
    for i in Adolf:lXp.pop(i-OlowCost); OlowCost+=1


    for i in range(len(lProj)):#Actualisation position Projectiles
        lProj[i][0]=lProj[i][2]+((time()-lProj[i][6])*lProj[i][5])*cos(lProj[i][4])
        lProj[i][1]=lProj[i][3]+((time()-lProj[i][6])*lProj[i][5])*sin(lProj[i][4])

    Holocaust=[]; Hitlof=0; Shaw=[]; Musso=0
    for i in range(len(lProj)):#Collisions Projectiles
        if grille[int((lProj[i][1]+20)/40)][int((lProj[i][0])/40)]=='0':Holocaust.append(i)
        elif lProj[i][7]:
            for j in range(len(ennemis)):
                if (ennemis[j][2]-bestiaire[ennemis[j][-1]][5]>=lProj[i][0]+2 or ennemis[j][2]+bestiaire[ennemis[j][-1]][5]<=lProj[i][0]-2 or
                    ennemis[j][3]-bestiaire[ennemis[j][-1]][6]>=lProj[i][1]+2 or ennemis[j][3]+bestiaire[ennemis[j][-1]][6]<=lProj[i][1]-2):pass
                elif i not in Holocaust and Combats[ennemis[j][0]][3]:
                    if randint(1, (int(wStats[9]/mods[4]) if int(wStats[9]/mods[4])>=1 else 1))==1:
                        if wStats[-1]==0:Holocaust.append(i)
                        ennemis[j][5]-=wStats[8]*(1.5*mods[5])*mods[0]
                        lText.append([lProj[i][0], lProj[i][1], 'orange', str(-wStats[8]*(1.5*mods[5])*mods[0])[:5], time(),0.2, 14])
                    else:
                        if wStats[-1]==0:Holocaust.append(i)
                        ennemis[j][5]-=wStats[8]*mods[0]
                        lText.append([lProj[i][0], lProj[i][1], 'yellow', str(-wStats[8]*mods[0])[:5], time(),0.2, 12])
                    if ennemis[j][5]<=0 and j not in Shaw:Shaw.append(j)
        elif lProj[i][7]==False:
            if (pos[0]-18>=lProj[i][0]+2 or pos[0]+18<=lProj[i][0]-2 or
                pos[1]-22>=lProj[i][1]+2 or pos[1]+22<=lProj[i][1]-2):pass
            elif i not in Holocaust:
                if powers[0][1] and pStats[4]>10:
                    lText.append([lProj[i][0], lProj[i][1], 'lightblue', str(-lProj[i][-1]), time(),0.2, 16])
                    lProj[i][2], lProj[i][3]=lProj[i][0], lProj[i][1]
                    lProj[i][4]+=pi; lProj[i][6]=time(); lProj[i][7]=True; lProj[i][9],lProj[i][10]='lightblue','lightgreen'
                else:
                    boule=True
                    if pStats[1]<=0:boule=False
                    Holocaust.append(i);pStats[1]-=lProj[i][-1]
                    if pStats[1]<0:
                        pStats[1]=0; powers[pStats[6]][1]=False
                        if boule:gStats[0]=time()-gStats[0]
                    lText.append([lProj[i][0], lProj[i][1], 'red', str(-lProj[i][-1]), time(),0.2, 16])
    for i in range(len(Holocaust)):lProj.pop(Holocaust[i]-Hitlof); Hitlof+=1
    for k in range(len(Shaw)):
        for j in range(randint(5,10)*(12 if level%3==0 else 1)):
            lXp.append([ennemis[Shaw[k]-Musso][2]+randint(-25*(2 if level%3==0 else 1),25*(2 if level%3==0 else 1)), 
                        ennemis[Shaw[k]-Musso][3]+randint(-25*(2 if level%3==0 else 1),25*(2 if level%3==0 else 1)),
                        0,0,time(),time()])
        lDed.append([ennemis[Shaw[k]-Musso][2], ennemis[Shaw[k]-Musso][3]])
        Combats[ennemis[Shaw[k]-Musso][0]][4]-=1; ennemis.pop(Shaw[k]-Musso); gStats[1]+=1; Musso+=1

    for i in range(len(ennemis)):#"IA" des Ennemis
        if Combats[ennemis[i][0]][3]:

            if (time()-ennemis[i][11])>ennemis[i][9][6]*2 and ((ennemis[i][6]==0 and ennemis[i][7]==0) or level%3==0) and debordeur<1 and ((time()-pStats[0])<wStats[6]/2 or (time()-pStats[0])>wStats[6]*2):
                ennemis[i][11]=time(); debordeur+=5
                for j in range(int(ennemis[i][9][4])+pression):
                    disp=ennemis[i][12]+(2*(0.75**pression if pression>0 else 1))*(-(ennemis[i][9][5]/2/180*pi)+random()*(ennemis[i][9][5]/180*pi))
                    pStats[0]=time(); ennemis[i][9][2]=3; lProj.append([
                        ennemis[i][2]+(ennemis[i][9][3])*cos(disp), ennemis[i][3]+8+(ennemis[i][9][3])*sin(disp), ennemis[i][2]+(ennemis[i][9][3])*cos(disp), 
                        ennemis[i][3]+8+(ennemis[i][9][3])*sin(disp), disp, ennemis[i][9][7]/(3*(0.85**pression if pression>0 else 1)), time(), False, ennemis[i][-2], 'red', 'pink', ennemis[i][-3]])

            if time()-tac>2:
                if randint(1,4)!=1:ennemis[i][6],ennemis[i][7]=randint(-1,1),randint(-1,1)
                else:ennemis[i][6],ennemis[i][7]=0,0
                if level%3==0:
                    ennemis[i][9]=arsenal[randint(bestiaire[ennemis[i][-1]][3], bestiaire[ennemis[i][-1]][3]+1)][:]
            posP=[ennemis[i][2],ennemis[i][3]]
            posP[0]+=(time()-frame)*ennemis[i][8]*ennemis[i][6];posP[1]+=(time()-frame)*ennemis[i][8]*ennemis[i][7]
            if (grille[int((posP[1]+8)/40)][int((posP[0]-16)/40)]!='0' and grille[int((posP[1]+8)/40)][int((posP[0]+16)/40)]!='0'
                and grille[int((posP[1]+28)/40)][int((posP[0]-16)/40)]!='0' and grille[int((posP[1]+28)/40)][int((posP[0]+16)/40)]!='0'):
                ennemis[i][2]=posP[0]; ennemis[i][3]=posP[1]
                if ennemis[i][6]!=0 or ennemis[i][7]!=0:
                    if (ennemis[i][2]<pos[0] and ennemis[i][6]==-1) or (ennemis[i][2]>pos[0] and ennemis[i][6]==1):ennemis[i][4]=2+ennemis[i][1]
                    else:ennemis[i][4]=1+ennemis[i][1]
                else:ennemis[i][4]=0+ennemis[i][1]
            else:ennemis[i][4]=0+ennemis[i][1]

    if lInput[-1] and pStats[4]>0:pStats[4]-=40*(time()-frame)
    elif lInput[-1]==False and pStats[4]<pStats[5]:pStats[4]+=10*(time()-frame)
    if pStats[4]<0:lInput[-1]=False; pStats[4]=0; powers[pStats[6]][1]=False
    if pStats[4]>pStats[5]:pStats[4]=pStats[5]
    if lInput[-1]:
        if pStats[6]==1 and pStats[4]>0:bonus[0]=2; bonus[1]=2
        else:bonus[0]=1; bonus[1]=1
        if pStats[6]==2 and pStats[4]>0:bonus[2]=200
        else:bonus[2]=75
    else:bonus[0]=1; bonus[1]=1; bonus[2]=0

    frame=time()
    if time()-tac>2:tac=time()

    if time()-fpsLimiter>1/60:#Affichage
        fps=1/(time()-fpsLimiter)
        fpsLimiter=time()
        if angle!=0:
            if angle<pi/2 or angle>3*pi/2:
                perso[0]=ImageTk.PhotoImage(Image.open('sprites/perso/'+perso[1]+str(animP[perso[2]][0])+'.png').resize((100, 100), Image.ANTIALIAS))
                weapon=ImageTk.PhotoImage(WeaponsP[int(wStats[0])][int(wStats[2])-1].rotate(angle*180/pi).resize((100, 100), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
            else:
                perso[0]=ImageTk.PhotoImage(Image.open('sprites/perso/'+perso[1]+str(animP[perso[2]][0])+'.png').resize((100, 100), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                weapon=ImageTk.PhotoImage(WeaponsP[int(wStats[0])][int(wStats[2])-1].rotate(180-angle*180/pi).resize((100, 100), Image.ANTIALIAS))
        animO[0][2]=ImageTk.PhotoImage(animO[0][3][animO[0][0]-1].resize((100, 180)))
        for i in range(len(animE)):
            animE[i][2]=animE[i][6][animE[i][0]-1]
            animE[i][3]=animE[i][7][animE[i][0]-1]
        for i in range(len(ennemis)):#Sprites Armes Ennemies
            size=(200 if level%3==0 else 100)
            if ((ennemis[i][2])**2-pos[0]**2)!=0 and Combats[ennemis[i][0]][3]:
                if pos[0]>ennemis[i][2]:
                    angle=atan(((ennemis[i][3])-pos[1])/((ennemis[i][2])-pos[0])); ennemis[i][12]=angle
                    ennemis[i][10]=ImageTk.PhotoImage(WeaponsP[int(ennemis[i][9][0])][int(ennemis[i][9][2])-1].rotate(angle*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                else:
                    angle=pi+atan(((ennemis[i][3])-pos[1])/((ennemis[i][2])-pos[0])); ennemis[i][12]=angle
                    ennemis[i][10]=ImageTk.PhotoImage(WeaponsP[int(ennemis[i][9][0])][int(ennemis[i][9][2])-1].rotate(180-angle*180/pi).resize((size, size), Image.ANTIALIAS))
            elif (Combats[ennemis[i][0]][3]==False and ennemis[i][2]>pos[0]-tk.winfo_screenwidth()/2-40 and ennemis[i][2]<pos[0]+tk.winfo_screenwidth()/2+40
            and ennemis[i][3]>pos[1]-tk.winfo_screenheight()/2-40 and ennemis[i][3]<pos[1]-tk.winfo_screenheight()/2+40):
                if pos[0]>ennemis[i][2]:ennemis[i][10]=ImageTk.PhotoImage(Image.open('sprites/armes/'+ennemis[i][9][1]+'/'+ennemis[i][9][1]+str(int(ennemis[i][9][2]))+'.png').rotate(0*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                else:ennemis[i][10]=ImageTk.PhotoImage(WeaponsP[int(ennemis[i][9][0])][int(ennemis[i][9][2])-1].rotate(180-0*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))
        affichage()

    if state:tk.after(1, main)
    elif nL and Xp[1]>Xp[2]:#Menu selection mod.
        if time()-modList[2]>0.33:
            if lInput[0]:modList[1]+=1; modList[2]=time()
            if modList[1]>2:modList[1]=0
            if lInput[1]:modList[1]-=1; modList[2]=time()
            if modList[1]<0:modList[1]=2
        tk.after(1, main)
    elif nL:chargement()

'''
Cette fonction génére la map (grille de collision + image de tous les objets dériére lesquels le joueur ne peut passer, de
facon à faciliter l'affichage), ainsi que les groupes d'ennemis.
Appelle main() à la fin de son execution
'''
def generationNiveau():
    global salles, grille, grilleP, monde, map, pos, portal, state, lObj, lCoffre, level, Combats, ennemis, lDed, nL, pression, lXp
    global mods, wStats, pStats, modList

    generation=True; lObj=[]; lCoffre=[]; ennemis=[]; Combats=[]; lDed=[]; lXp=[]; level+=1

    if mods[6]==1:mods[6]=0; wStats=arsenal[5]
    if mods[7]==1:mods[7]=0; pStats[1]=100

    modList[0]=[-1,-1,-1]
    for i in range(3):#Selection de la liste de modificateurs à proposer si lvl. up
        condition=True
        while condition:
            n=randint(0,5)
            if n not in modList[0]:condition=False
        modList[0][i]=n

    if level%3==1 and level!=1:pression+=1
    while generation:#Layer du niveau
        generation=False; salles=[[[0,0] for i in range(5)] for j in range(5)]

        if level%3!=0:#Niveau classique
            pos=[randint(0,4), randint(0,4)]; salles[pos[1]][pos[0]]=[1,1]
            for i in range(4):
                condition=True; var=0
                while condition:
                    posP=[pos[0], pos[1]]; var+=1
                    if randint(0,1)==0:posP[0]+=randrange(-1,1,2)
                    else:posP[1]+=randrange(-1,1,2)
                    if posP[0]>=0 and pos[0]<5 and posP[1]>=0 and pos[1]<5:
                        if salles[posP[1]][posP[0]][0]!=1:condition=False
                    if var>10:condition=False; generation=True
                pos[0]=posP[0]; pos[1]=posP[1]
                if i==3:salles[posP[1]][posP[0]]=[1,2]
                else:
                    salles[posP[1]][posP[0]][0]=randint(2,3)
                    if randint(0,1)==0:posP[0]+=randint(-1,1)
                    else:posP[1]+=randint(-1,1)
                    if posP[0]>=0 and posP[0]<5 and posP[1]>=0 and posP[1]<5:
                        if salles[posP[1]][posP[0]][0]==0:salles[posP[1]][posP[0]]=[1,3]
        else:#Boss
            salles[3][2]=[1,1]; salles[2][2]=[3,0]; salles[1][2]=[1,2]

    grille=[['0' for i in range(35*5)] for j in range(35*5)]; grilleP=[['0' for i in range(35*5)] for j in range(35*5)]
    for i in range(5):#Création de la matrice
        for j in range(5):
            if salles[j][i][0]!=0:
                if salles[j][i][0]==1:
                    if salles[j][i][1]==1:pos=[i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2]
                    elif salles[j][i][1]==2:portal=[i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2]
                    elif salles[j][i][1]==3:
                        lCoffre.append([True, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, 
                        ImageTk.PhotoImage(Image.open('sprites/props/coffreF.png').resize((75,75)))])
                    for o in range(i*35+12, i*35+23):
                        for p in range(j*35+12, j*35+23):grille[p][o]=chr(randint(97, 105))
                if salles[j][i][0]==2:
                    for o in range(i*35+9, i*35+26):
                        for p in range(j*35+9, j*35+26):grille[p][o]=chr(randint(97, 105))
                if salles[j][i][0]==3:
                        for o in range(i*35+6, i*35+29):
                            for p in range(j*35+6, j*35+29):grille[p][o]=chr(randint(97, 105))
                
                if j>0:
                    if salles[j-1][i][0]!=0:
                        for o in range(i*35+15, i*35+20):
                            for p in range(j*35-20, j*35+20):
                                if grille[p][o]=='0':grille[p][o]=chr(randint(97, 105))
                if j<4:
                    if salles[j+1][i][0]!=0:
                        for o in range(i*35+15, i*35+20):
                            for p in range(j*35+20, j*35+50):
                                if grille[p][o]=='0':grille[p][o]=chr(randint(97, 105))
                if i>0:
                    if salles[j][i-1][0]!=0:
                        for o in range(i*35-20, i*35+20):
                            for p in range(j*35+15, j*35+20):
                                if grille[p][o]=='0':grille[p][o]=chr(randint(97, 105))
                if i<4:
                    if salles[j][i+1][0]!=0:
                        for o in range(i*35+20, i*35+50):
                            for p in range(j*35+15, j*35+20):
                                if grille[p][o]=='0':grille[p][o]=chr(randint(97, 105))
    n=0; Combats=[]
    for i in range(5):#Création des Combats
        for j in range(5):
            if salles[j][i][0]==2:
                rand=randint(4,6);Combats.append([2, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand])
                with open('files/roomLayers/2/'+str(randint(0,5))+'.txt', 'r') as file:
                    var=0
                    for line in file:
                        for o in range(17):
                            if line[o]=='1':
                                grille[j*(35)+9+o][i*(35)+9+var]='0'
                        var+=1
                for o in range(rand):
                    boule=True
                    while boule:
                        posP=[randint(i*(35*40)+(35*40)/2-8*40,i*(35*40)+(35*40)/2+8*40), randint(j*(35*40)+(35*40)/2-8*40,j*(35*40)+(35*40)/2+8*40)]
                        if (grille[int((posP[1]+16)/40)][int((posP[0]+16)/40)]!='0' and grille[int((posP[1]+16)/40)][int((posP[0]-16)/40)]!='0'
                            and grille[int((posP[1]-16)/40)][int((posP[0]+16)/40)]!='0' and grille[int((posP[1]-16)/40)][int((posP[0]-16)/40)]!='0'):boule=False
                    rand=randint(0,2); ennemis.append([n, bestiaire[rand][0], posP[0], posP[1], bestiaire[rand][0], bestiaire[rand][1], 0, 0, bestiaire[rand][2],arsenal[bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+arsenal[bestiaire[rand][3]][1]+'/'+arsenal[bestiaire[rand][3]][1]+str(int(arsenal[bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,arsenal[bestiaire[rand][3]][8], bestiaire[rand][4], rand])
                n+=1
            if salles[j][i][0]==3 and level%3!=0:#Niveau Classique
                rand=randint(6,8);Combats.append([3, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand])
                with open('files/roomLayers/3/'+str(randint(0,3))+'.txt', 'r') as file:
                    var=0
                    for line in file:
                        for o in range(23):
                            if line[o]=='1':
                                grille[j*(35)+6+o][i*(35)+6+var]='0'
                        var+=1
                for o in range(rand):
                    boule=True
                    while boule:
                        posP=[randint(i*(35*40)+(35*40)/2-11*40,i*(35*40)+(35*40)/2+11*40), randint(j*(35*40)+(35*40)/2-11*40,j*(35*40)+(35*40)/2+11*40)]
                        if (grille[int((posP[1]+16)/40)][int((posP[0]+16)/40)]!='0' and grille[int((posP[1]+16)/40)][int((posP[0]-16)/40)]!='0'
                            and grille[int((posP[1]-16)/40)][int((posP[0]+16)/40)]!='0' and grille[int((posP[1]-16)/40)][int((posP[0]-16)/40)]!='0'):boule=False
                    rand=randint(0,2); ennemis.append([n, bestiaire[rand][0], posP[0], posP[1], bestiaire[rand][0], bestiaire[rand][1], 0, 0, bestiaire[rand][2],arsenal[bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+arsenal[bestiaire[rand][3]][1]+'/'+arsenal[bestiaire[rand][3]][1]+str(int(arsenal[bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,arsenal[bestiaire[rand][3]][8], bestiaire[rand][4], rand])
                n+=1
            elif salles[j][i][0]==3:#Boss
                Combats.append([3, 2*(35*40)+(35*40)/2, 2*(35*40)+(35*40)/2, False, 1]); rand=randint(3,4)
                ennemis.append([0, bestiaire[rand][0], 2*(35*40)+(35*40)/2, 2*(35*40)+(35*40)/2, bestiaire[rand][0], bestiaire[rand][1], 0, 0, bestiaire[rand][2],arsenal[bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+arsenal[bestiaire[rand][3]][1]+'/'+arsenal[bestiaire[rand][3]][1]+str(int(arsenal[bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,arsenal[bestiaire[rand][3]][8], bestiaire[rand][4], rand])

    monde=Image.open("sprites/level/blank.png")
    for i in range(35*5):
        for j in range(35*5):
            if grille[j][i]!='0':Image.Image.paste(monde, Image.open("sprites/level/tiles/"+grille[j][i]+".png"), (i*40, j*40))
            elif i>1 and i<35*5-2 and j>1 and j<35*5-2:
                if grille[j+1][i]!='0' or grille[j][i-1]!='0' or grille[j][i+1]!='0' or grille[j+1][i+1]!='0' or grille[j+1][i-1]!='0':
                    Image.Image.paste(monde, Image.open("sprites/level/tiles/"+str(randint(1,3))+".png"), (i*40, j*40-20)); grilleP[j][i]='a'
                if grille[j-1][i]!='0':grilleP[j][i]=str(randint(3,5))
    
    for i in range(35*5):#BLOC PROVISOIRE !!!!!
        for j in range(35*5):
            if i>1 and i<35*5-2 and j>1 and j<35*5-2:
                if grilleP[j-1][i]=='a' and grilleP[j][i]=='0' and grille[j][i]=='0':grilleP[j][i]=str(randint(3,5))

    map=ImageTk.PhotoImage(monde.resize((200, 200), Image.ANTIALIAS)); monde=ImageTk.PhotoImage(monde)

    state=True; nL=True
    main()

'''
event Tk gérant les inputs clavier
'''
def clavier(event):
    global lInput, pos, portal, state, lObj, wStats, pStats, lCoffre, state, nL, powers, angle, modList, mods, Xp
    var=event.keysym

    if var=='Right':lInput[0]=True
    if var=='Left':lInput[1]=True
    if var=='Up':lInput[2]=True
    if var=='Down':lInput[3]=True
    if var=='r':lInput[4]=True

    if var=='t':
        if pStats[4]>0:powers[pStats[6]][1]=True; lInput[-1]=True
        else:powers[pStats[6]][1]=False; lInput[-1]=False

    if var=='Escape':tk.destroy()

    if var=='y':
        if not state and nL and Xp[1]>Xp[2] and time()-modList[3]>0.5:
            Xp[2]+=1
            for i in range(6):
                if modsC[modList[0][modList[1]]][i]!=0:mods[i]=mods[i]*modsC[modList[0][modList[1]]][i]
            mods[6]=modsC[modList[0][modList[1]]][6]; mods[7]=modsC[modList[0][modList[1]]][7]

        if pStats[1]==0 and state:state=False; nL=False; init()
        if pos[0]>portal[0]-50 and pos[0]<portal[0]+50 and pos[1]>portal[1]-90 and pos[1]<portal[1]+90:state=False; modList[3]=time()
        else:
            for i in range(len(lObj)):
                if pos[0]>lObj[i][2]-50 and pos[0]<lObj[i][2]+50 and pos[1]>lObj[i][3]-50 and pos[1]<lObj[i][3]+50:
                    lObj.append([wStats[0], wStats[1], pos[0], pos[1], 
    ImageTk.PhotoImage(Image.open('sprites/armes/'+wStats[1]+'/'+wStats[1]+str(int(wStats[2]))+'.png').resize((100, 100), Image.ANTIALIAS))])
                    wStats=arsenal[int(lObj[i][0])]; lObj.pop(i)
            for i in range(len(lCoffre)):
                if pos[0]>lCoffre[i][1]-50 and pos[0]<lCoffre[i][1]+50 and pos[1]>lCoffre[i][2]-50 and pos[1]<lCoffre[i][2]+50 and lCoffre[i][0]:
                    var=randint(0,5); lObj.append([var, arsenal[var][1], lCoffre[i][1]+randint(-10,10), lCoffre[i][2]+randint(-10,10), 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+arsenal[var][1]+'/'+arsenal[var][1]+str(int(wStats[2]))+'.png').resize((100, 100), Image.ANTIALIAS))])
                    lCoffre[i][0]=False; lCoffre[i][3]=ImageTk.PhotoImage(Image.open('sprites/props/coffreO.png').resize((75,75)))

def clavierRelease(event):
    global lInput, pStats, powers
    var=event.keysym

    if var=='Right':lInput[0]=False
    if var=='Left':lInput[1]=False
    if var=='Up':lInput[2]=False
    if var=='Down':lInput[3]=False
    if var=='r':lInput[4]=False

    if var=='t':powers[pStats[6]][1]=False; lInput[-1]=False

def twin(event):
    global curseur

    if pStats[1]>0:curseur=[event.x, event.y]

'''
Force l'affichage d'un écran de chargement avant de lancer generationNiveau()
'''
def chargement():
    can.delete('all')
    can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, text='CHARGEMENT...', 
                    font=('Ubuntu', 45), fill='white', anchor='center')
    can.update_idletasks()#beurk
    tk.after(160,generationNiveau)

can=Canvas(height=tk.winfo_screenheight(), width=tk.winfo_screenwidth(), bg='black')
can.focus_set()
can.bind("<Key>", clavier); can.bind("<KeyRelease>", clavierRelease)
chargement()
can.pack()

tk.mainloop()