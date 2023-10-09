from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk
from math import cos, sin, atan, pi, sqrt
from random import randint, randrange, random
from time import time
from csv import reader

from modules.classes import Joueur, Combat, Ennemi, Projectile, Orbe
from modules.globales import Var

tk=Tk()
tk.attributes('-fullscreen', True)
tk.iconbitmap('sprites/UI/icone.ico')

tic=time(); fpsLimiter=time(); animP=[[1,5],[1,6]]; state=False; lObj=[]; lCoffre=[]
lInput=[False, False, False, False, False, False]; anim=1; Joueur.wStats=[0, 'FAMAS', 1]
Projectile.index=[]; salles=[]; portal=[None, None]; modList=[[], 0, time(), None]
Combat.index=[]; Ennemi.index=[]; nL=True; angle=pi/100; fps=0
bonus=[1,1,0]; lXp=[]; Xp=[0,1,1]
filter=ImageTk.PhotoImage(Image.open('sprites/UI/filter.png').resize((int(tk.winfo_screenwidth()/2), int(tk.winfo_screenheight()))))

perso=[None, 'Idle', 0]; weapon=None; monde=None; map=None

for i in range(len(Var.animE)):#Découpe des Sprite Sheets
    for j in range(Var.animE[i][1]):
        Var.animE[i][6].append(ImageTk.PhotoImage(
Image.open('sprites/ennemies/'+Var.animE[i][4]+'.png').crop((0+24*(j),0,24+24*(j),24)).resize((Var.animE[i][5], Var.animE[i][5]))))
        Var.animE[i][7].append(ImageTk.PhotoImage(
Image.open('sprites/ennemies/'+Var.animE[i][4]+'.png').crop((0+24*(j),0,24+24*(j),24)).resize((Var.animE[i][5], Var.animE[i][5])).transpose(Image.FLIP_LEFT_RIGHT)))

modsC=[]; lecteur=reader(open('files/mods.csv', 'r'))
for line in lecteur:modsC.append(line)
for i in range(len(modsC)):
    for j in range(len(modsC[i])):modsC[i][j]=float(modsC[i][j])
wSprites={}
Joueur.wStats=Var.arsenal[0]

WeaponsP=[[Image.open('sprites/armes/'+Var.arsenal[i][1]+'/'+Var.arsenal[i][1]+str(j)+'.png')
           for j in range(1,4)] for i in range(len(Var.arsenal))]
animO=[[1,4,None, [Image.open('sprites/portal/'+str(i)+'.png') for i in range(1,5)]]]

Joueur.powers=[[False, False, ImageTk.PhotoImage(Image.open('sprites/perso/shield.png').resize((100, 100)))],
        [False, False, ImageTk.PhotoImage(Image.open('sprites/perso/fire.png').resize((100, 100)))],
        [True, False, ImageTk.PhotoImage(Image.open('sprites/perso/wings.png').resize((100, 100)))]]

mur=[PhotoImage(file='sprites/level/tiles/1.png'),PhotoImage(file='sprites/level/tiles/2.png'),PhotoImage(file='sprites/level/tiles/3.png')]
murH=[PhotoImage(file='sprites/level/tiles/mur1H.png'),PhotoImage(file='sprites/level/tiles/mur2H.png'),PhotoImage(file='sprites/level/tiles/mur3H.png')]
door=PhotoImage(file='sprites/level/tiles/door.png'); doorH=PhotoImage(file='sprites/level/tiles/doorH.png')
ded1=ImageTk.PhotoImage(Image.open('sprites/ennemies/troupierDed.png').resize((100,100)))
ded2=ImageTk.PhotoImage(Image.open('sprites/ennemies/troupierDed.png').resize((200,200))); lDed=[]
modsText=[PhotoImage(file='sprites/UI/texts/'+str(i)+'.png') for i in range(6)]
Joueur.mods=[1,1,1,1,1,1,0,0]#Dmg, mul.tir, pré, vit, crit, mult.crit, GLOCK

def init():
    global bonus, Xp
    can.delete('all')

    Joueur.wStats=Var.arsenal[0]; Joueur.stats=[0, 100, 100, 250, 100, 100, randint(0,2)]; bonus=[1,1,0]; Xp=[0,1,1]
    Var.level=0; Ennemi.index=[]; Projectile.index=[]; Combat.index=[]; Var.gStats=[time(), 0]; Var.pression=0; Joueur.mods=[1,1,1,1,1,1,0,0]
    chargement()

def affichage():
    global perso, portal, animO, lObj, lCoffre, lDed, ded1, ded2, modList
    can.delete('all')

    can.create_image(
        -Joueur.pos[0]+(tk.winfo_screenwidth()/2), -Joueur.pos[1]+(tk.winfo_screenheight()/2), image=monde, anchor='nw'
    )
    can.create_image(portal[0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), portal[1]-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                    image=animO[0][2], anchor='center')
    if Joueur.pos[0]>portal[0]-50 and Joueur.pos[0]<portal[0]+50 and Joueur.pos[1]>portal[1]-90 and Joueur.pos[1]<portal[1]+90:
        can.create_text(portal[0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), portal[1]-110-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                        text='Entrer dans le portail', anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(lDed)):
        can.create_image(lDed[i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lDed[i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2), image=(ded1 if Var.level%3!=0 else ded2), anchor='center')
    for i in range(len(lXp)):
        can.create_oval(lXp[i][0]-4-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lXp[i][1]-4-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                        lXp[i][0]+4-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lXp[i][1]+4-Joueur.pos[1]+(tk.winfo_screenheight()/2), outline='green', fill='lightgreen')
    CheikPoint=[]
    for j in range(int((Joueur.pos[1]-tk.winfo_screenheight()/2)/40), int((Joueur.pos[1]+20)/40+3)):
        for i in range(len(Ennemi.index)):
            if Ennemi.index[i].posY<(j)*40 and i not in CheikPoint:
                if Ennemi.index[i].posX<Joueur.pos[0]:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][2], anchor='center'); CheikPoint.append(i)
                else:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][3], anchor='center'); CheikPoint.append(i)
                can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2)+8, image=Ennemi.index[i].img, anchor='center')
        for i in range(int((Joueur.pos[0]-tk.winfo_screenwidth()/2)/40-40), int((Joueur.pos[0]+tk.winfo_screenwidth()/2)/40+40)):
            if i>3 and i<7000/40-3 and j>3 and j<7000/40-3:
                if ord(Var.grilleP[j][i])<97:
                    if int(Var.grilleP[j][i])>=3 and int(Var.grilleP[j][i])<=5:
                        if Var.grilleP[j+1][i]=='a':
                            can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=murH[int(Var.grilleP[j][i])-3], anchor='nw')
                        else:can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=mur[int(Var.grilleP[j][i])-3], anchor='nw')
                if Var.grilleP[j][i]=='2':
                    if Var.grille[j+1][i]=='0' or Var.grilleP[j+1][i]=='2':
                        can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=doorH, anchor='nw')
                    else:can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=door, anchor='nw')

    for i in range(len(lCoffre)):
        can.create_image(lCoffre[i][1]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lCoffre[i][2]-Joueur.pos[1]+(tk.winfo_screenheight()/2), image=lCoffre[i][3], anchor='center')
        if Joueur.pos[0]>lCoffre[i][1]-50 and Joueur.pos[0]<lCoffre[i][1]+50 and Joueur.pos[1]>lCoffre[i][2]-50 and Joueur.pos[1]<lCoffre[i][2]+50 and lCoffre[i][0]:
            can.create_text(lCoffre[i][1]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lCoffre[i][2]-Joueur.pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Ouvrir Coffre', anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(lObj)):
        can.create_image(lObj[i][2]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lObj[i][3]-Joueur.pos[1]+(tk.winfo_screenheight()/2), image=lObj[i][4], anchor='center')
        if Joueur.pos[0]>lObj[i][2]-50 and Joueur.pos[0]<lObj[i][2]+50 and Joueur.pos[1]>lObj[i][3]-50 and Joueur.pos[1]<lObj[i][3]+50:
            can.create_text(lObj[i][2]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), lObj[i][3]-Joueur.pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Ramasser : '+lObj[i][1], anchor='center', fill='blue', font=('Arial', 12))

    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=perso[0], anchor='center')
    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+8, image=weapon, anchor='center')
    for i in range(len(Joueur.powers)):
        if Joueur.powers[i][1]:can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=Joueur.powers[i][2], anchor='center')

    for j in range(int((Joueur.pos[1]+20)/40), int((Joueur.pos[1]+tk.winfo_screenheight()/2)/40+3)):
        for i in range(len(Ennemi.index)):
            if Ennemi.index[i].posY<(j)*40 and i not in CheikPoint:
                if Ennemi.index[i].posX<Joueur.pos[0]:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][2], anchor='center'); CheikPoint.append(i)
                else:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][3], anchor='center'); CheikPoint.append(i)
                can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2)+8, image=Ennemi.index[i].img, anchor='center')
        for i in range(int((Joueur.pos[0]-tk.winfo_screenwidth()/2)/40-40), int((Joueur.pos[0]+tk.winfo_screenwidth()/2)/40+40)):
            if i>3 and i<7000/40-3 and j>3 and j<7000/40-3:
                if ord(Var.grilleP[j][i])<97:
                    if int(Var.grilleP[j][i])>=3 and int(Var.grilleP[j][i])<=5:
                        if Var.grilleP[j+1][i]=='a':
                            can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=murH[int(Var.grilleP[j][i])-3], anchor='nw')
                        else:can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=mur[int(Var.grilleP[j][i])-3], anchor='nw')
                if Var.grilleP[j][i]=='2':
                    if Var.grille[j+1][i]=='0' or Var.grilleP[j+1][i]=='2':
                        can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=doorH, anchor='nw')
                    else:can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=door, anchor='nw')

    for i in range(len(Projectile.index)):#Affichage Projectiles
        if Joueur.wStats[-1]==0 or Projectile.index[i][7]==False:
            can.create_oval(
                Projectile.index[i].posX-Projectile.index[i].r-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Projectile.index[i].posY-Projectile.index[i].r-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                Projectile.index[i].posX+Projectile.index[i].r-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Projectile.index[i].posY+Projectile.index[i].r-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                fill=Projectile.index[i].color, outline=Projectile.index[i].outline
            )
    Holocost=[]; Hitlof=0
    for i in range(len(Var.lText)):
        can.create_text(Var.lText[i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lText[i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                        text=Var.lText[i][3], fill=Var.lText[i][2], font=('Arial', Var.lText[i][6]), anchor='center')
        if time()-Var.lText[i][4]>Var.lText[i][5]:Holocost.append(i)
    for i in range(len(Holocost)):Var.lText.pop(Holocost[i]-Hitlof); Hitlof+=1

    if lInput[4] and Joueur.stats[1]>0 and Joueur.powers[0][1]==False and Joueur.wStats[-1]==1:#Affichage Laser !
        n=2
        if ((tk.winfo_screenwidth()/2)-curseur[0])!=0:#Calcul angle
            if curseur[0]>tk.winfo_screenwidth()/2:angle=atan(((tk.winfo_screenheight()/2)-curseur[1])/((tk.winfo_screenwidth()/2)-curseur[0]))
            else:angle=pi+atan(((tk.winfo_screenheight()/2)-curseur[1])/((tk.winfo_screenwidth()/2)-curseur[0]))
        else:angle=0
        while Var.grille[int((Joueur.pos[1]+(Joueur.wStats[3]+n)*sin(angle))/40)][int((Joueur.pos[0]+(Joueur.wStats[3]+n)*cos(angle))/40)]!='0':n+=2
        can.create_line(tk.winfo_screenwidth()/2+Joueur.wStats[3]*cos(angle), tk.winfo_screenheight()/2+Joueur.wStats[3]*sin(angle), 
                        tk.winfo_screenwidth()/2+(Joueur.wStats[3]+n)*cos(angle), tk.winfo_screenheight()/2+(Joueur.wStats[3]+n)*sin(angle),fill='lightblue', width=4)

    if Joueur.stats[1]>0 and nL:#UI partie en cours
        if state:#Jeu normal
            can.create_image(tk.winfo_screenwidth()-75, 75, image=map, anchor='ne')
            can.create_rectangle(tk.winfo_screenwidth()-275, 75, tk.winfo_screenwidth()-75, 275, outline='brown', width=4)
            can.create_oval(tk.winfo_screenwidth()-275+(Joueur.pos[0]/7000*200)-3, 75+(Joueur.pos[1]/7000*200)-3,
                            tk.winfo_screenwidth()-275+(Joueur.pos[0]/7000*200)+3, 75+(Joueur.pos[1]/7000*200)+3, fill='pink')
            can.create_oval(tk.winfo_screenwidth()-275+(portal[0]/7000*200)-3, 75+(portal[1]/7000*200)-3,
                            tk.winfo_screenwidth()-275+(portal[0]/7000*200)+3, 75+(portal[1]/7000*200)+3, fill='blue')
            can.create_text(tk.winfo_screenwidth()-275, 300, text='Zone : '+str(Var.level), anchor='w', fill='gainsboro', font=('Ubuntu', 16))
            can.create_rectangle(75, 75, 102, 177, outline='white', width=3)
            can.create_rectangle(76, 76+(100/200*(200-Xp[0])), 101, 177, fill='lightgreen', width=0)
            if Xp[1]>Xp[2]:can.create_text(88.5, 195, text='Niv. Sup !', anchor='center', fill='gainsboro', font=('Ubuntu', 16))
            can.create_text(75+(27/2), 75+51, text=str(Xp[1]), fill='white', font=('Ubuntu', 22), anchor='center')
            can.create_rectangle(165, tk.winfo_screenheight()-75, 565, tk.winfo_screenheight()-100, width=3, outline='white', fill='black')
            can.create_rectangle(166, tk.winfo_screenheight()-76, 165+398/Joueur.stats[2]*Joueur.stats[1], tk.winfo_screenheight()-99, width=0, fill='brown')
            can.create_text(365, tk.winfo_screenheight()-87.5, text=str(Joueur.stats[1])+' / '+str(Joueur.stats[2]), anchor='center', fill='white')
            can.create_rectangle(165, tk.winfo_screenheight()-107, 565, tk.winfo_screenheight()-115, width=0, fill='white')
            can.create_rectangle(166, tk.winfo_screenheight()-107, 165+398/Joueur.stats[5]*Joueur.stats[4], tk.winfo_screenheight()-115, width=0, fill='lightblue')
            can.create_oval(75,tk.winfo_screenheight()-107-50, 175, tk.winfo_screenheight()-107+50, fill='gainsboro', outline='brown')
            can.create_image(125, tk.winfo_screenheight()-107, image=Joueur.powers[Joueur.stats[6]][2], anchor='center')
            if Var.level%3==0 and Combat.index[0][3]:#Barre de vie du Boss
                try:
                    can.create_rectangle(tk.winfo_screenwidth()/2-300, 75, tk.winfo_screenwidth()/2+300, 115, outline='gainsboro')
                    can.create_rectangle(tk.winfo_screenwidth()/2-299, 76, tk.winfo_screenwidth()/2-299+598*(Ennemi.index[0].pv/Var.bestiaire[Ennemi.index[0].type][1]),
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
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2-100, text='Zone atteinte : '+str(Var.level), 
                        fill='White', font=('Ubuntu', 18))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, text='Ennemis tués : '+str(Var.gStats[1]), 
                        fill='White', font=('Ubuntu', 18))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+100, text='Durée de la run : '+str((Var.gStats[0])/60)[:4]+'min', 
                        fill='White', font=('Ubuntu', 18))
        can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()-tk.winfo_screenheight()/6, text='-[Interagir] pour recommencer-', 
                        fill='white', font=('Ubuntu', 22))

    can.create_text(10,10,text=str(int(fps))+' fps', fill=('green' if fps>40 else ('orange' if fps>20 else 'red')), anchor='nw')

def main():
    global tic,  fpsLimiter, animP, perso, weapon, anim, animO, state
    global lDed, bonus, angle, lXp, Xp, modList, fps

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
        if Combat.index[i][3] and Combat.index[i][4]>0:
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
        for i in range(len(animO)):
            animO[i][0]+=1
            if animO[i][0]>animO[i][1]:animO[i][0]=1
        for i in range(len(Var.animE)):
            Var.animE[i][0]+=1
            if Var.animE[i][0]>Var.animE[i][1]:Var.animE[i][0]=1
        for i in range(len(Ennemi.index)):
            if Combat.index[Ennemi.index[i].combat][3]:
                if Ennemi.index[i].arme[2]>1:Ennemi.index[i].arme[2]-=1
        if Joueur.wStats[2]>1:Joueur.wStats[2]-=1
        tic=time()

    perso[1]='Idle'; perso[2]=0
    if lInput[0] or lInput[1] or lInput[2] or lInput[3]:perso[1]='walk'; perso[2]=1

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
    if lInput[4] and Joueur.stats[1]>0 and Joueur.powers[0][1]==False:#Tir de l'Arme (JOUEUR)
        if (time()-Joueur.stats[0])>Joueur.wStats[6]:
            for i in range(int(Joueur.wStats[4]*bonus[1]*Joueur.mods[1])):
                disp=angle+(-((Joueur.wStats[5]*Joueur.mods[2])/2/180*pi)+random()*((Joueur.wStats[5]*Joueur.mods[2])/180*pi))
                Joueur.stats[0]=time(); Joueur.wStats[2]=3
                Projectile.index.append(Projectile(
                        Joueur.pos[0]+(Joueur.wStats[3])*cos(disp), Joueur.pos[1]+8+(Joueur.wStats[3])*sin(disp), Joueur.pos[0]+(Joueur.wStats[3])*cos(disp), 
                        Joueur.pos[1]+8+(Joueur.wStats[3])*sin(disp),disp, Joueur.wStats[7]*1.5, True, 3*bonus[0]
                ))
            while time()-rustine<1/60:0==0

    for i in range(len(Combat.index)):#Déclenchement/Arrêt Combat.index
        if (Combat.index[i][3]==False and Combat.index[i][0]==2 and Combat.index[i][4]>0 and Joueur.pos[0]>Combat.index[i][1]-8*40 and Joueur.pos[0]<Combat.index[i][1]+8*40
        and Joueur.pos[1]>Combat.index[i][2]-8*40 and Joueur.pos[1]<Combat.index[i][2]+8*40-20):
            Combat.index[i][3]=True; Var.tac=0
            for j in range(5):
                if Var.grille[int(Combat.index[i][2]/40)-9][int(Combat.index[i][1]/40)-2+j]!='0':
                    Var.grille[int(Combat.index[i][2]/40)-9][int(Combat.index[i][1]/40)-2+j]='0';Var.grilleP[int(Combat.index[i][2]/40)-9][int(Combat.index[i][1]/40)-2+j]='2'
                if Var.grille[int(Combat.index[i][2]/40)+9][int(Combat.index[i][1]/40)-2+j]!='0':
                    Var.grille[int(Combat.index[i][2]/40)+9][int(Combat.index[i][1]/40)-2+j]='0';Var.grilleP[int(Combat.index[i][2]/40)+9][int(Combat.index[i][1]/40)-2+j]='2'
                if Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-9]!='0':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-9]='0';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-9]='2'
                if Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+9]!='0':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+9]='0';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+9]='2'
        if (Combat.index[i][3]==False and Combat.index[i][0]==3 and Combat.index[i][4]>0 and Joueur.pos[0]>Combat.index[i][1]-11*40 and Joueur.pos[0]<Combat.index[i][1]+11*40
        and Joueur.pos[1]>Combat.index[i][2]-11*40 and Joueur.pos[1]<Combat.index[i][2]+11*40-20):
            Combat.index[i][3]=True; Var.tac=0
            for j in range(5):
                if Var.grille[int(Combat.index[i][2]/40)-12][int(Combat.index[i][1]/40)-2+j]!='0':
                    Var.grille[int(Combat.index[i][2]/40)-12][int(Combat.index[i][1]/40)-2+j]='0';Var.grilleP[int(Combat.index[i][2]/40)-12][int(Combat.index[i][1]/40)-2+j]='2'
                if Var.grille[int(Combat.index[i][2]/40)+12][int(Combat.index[i][1]/40)-2+j]!='0':
                    Var.grille[int(Combat.index[i][2]/40)+12][int(Combat.index[i][1]/40)-2+j]='0';Var.grilleP[int(Combat.index[i][2]/40)+12][int(Combat.index[i][1]/40)-2+j]='2'
                if Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-12]!='0':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-12]='0';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-12]='2'
                if Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+12]!='0':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+12]='0';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+12]='2'
        if Combat.index[i][3] and Combat.index[i][4]==0:
            Combat.index[i][3]=False; Projectile.index=[]
            for j in range(5):
                if Var.grilleP[int(Combat.index[i][2]/40)-9][int(Combat.index[i][1]/40)-2+j]=='2':
                    Var.grille[int(Combat.index[i][2]/40)-9][int(Combat.index[i][1]/40)-2+j]='1';Var.grilleP[int(Combat.index[i][2]/40)-9][int(Combat.index[i][1]/40)-2+j]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)+9][int(Combat.index[i][1]/40)-2+j]=='2':
                    Var.grille[int(Combat.index[i][2]/40)+9][int(Combat.index[i][1]/40)-2+j]='1';Var.grilleP[int(Combat.index[i][2]/40)+9][int(Combat.index[i][1]/40)-2+j]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-9]=='2':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-9]='1';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-9]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+9]=='2':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+9]='1';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+9]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)-12][int(Combat.index[i][1]/40)-2+j]=='2':
                    Var.grille[int(Combat.index[i][2]/40)-12][int(Combat.index[i][1]/40)-2+j]='1';Var.grilleP[int(Combat.index[i][2]/40)-12][int(Combat.index[i][1]/40)-2+j]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)+12][int(Combat.index[i][1]/40)-2+j]=='2':
                    Var.grille[int(Combat.index[i][2]/40)+12][int(Combat.index[i][1]/40)-2+j]='1';Var.grilleP[int(Combat.index[i][2]/40)+12][int(Combat.index[i][1]/40)-2+j]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-12]=='2':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-12]='1';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)-12]='0'
                if Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+12]=='2':
                    Var.grille[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+12]='1';Var.grilleP[int(Combat.index[i][2]/40)-2+j][int(Combat.index[i][1]/40)+12]='0'

    Adolf=[]; OlowCost=0
    for i in range(len(lXp)):#Actualisation vitesse et position des orbes d'Xp
        if sqrt((Joueur.pos[0]-lXp[i][0])**2+(Joueur.pos[1]-lXp[i][1])**2)<25:
            Adolf.append(i); Xp[0]+=1.2
            if Xp[0]>=200:Xp[0]-=200; Xp[1]+=1
        elif sqrt((Joueur.pos[0]-lXp[i][0])**2+(Joueur.pos[1]-lXp[i][1])**2)<300:#calcul vitesse en fonction de la distance au joueur
            #Calcul de l'angle entre le joueur et l'orbe
            angleO=None
            if (lXp[i][0]>Joueur.pos[0]):angleO=atan((lXp[i][1]-Joueur.pos[1])/(lXp[i][0]-Joueur.pos[0]))
            else:angleO=pi+atan((lXp[i][1]-Joueur.pos[1])/(lXp[i][0]-Joueur.pos[0]))
            #Attribution de la nouvelle vitesse
            lXp[i][2]=-(300-sqrt((Joueur.pos[0]-lXp[i][0])**2+(Joueur.pos[1]-lXp[i][1])**2))*1.5*cos(angleO)
            lXp[i][3]=-(300-sqrt((Joueur.pos[0]-lXp[i][0])**2+(Joueur.pos[1]-lXp[i][1])**2))*1.5*sin(angleO)
        else:lXp[i][2], lXp[i][3]=0,0
        lXp[i][0]+=lXp[i][2]*(time()-lXp[i][4]); lXp[i][1]+=lXp[i][3]*(time()-lXp[i][4])
        lXp[i][4]=time()
    for i in Adolf:lXp.pop(i-OlowCost); OlowCost+=1


    for i in Projectile.index:#Actualisation position Projectiles
        i.actualisation()

    Holocaust=[]; Hitlof=0; Shaw=[]; Musso=0
    for i in range(len(Projectile.index)):#Collisions Projectiles
        retour=Projectile.index[i].collision(i, Holocaust, Shaw)
        if retour[0]:Holocaust.append(i)
        Shaw+=retour[1]
    for i in range(len(Holocaust)):Projectile.index.pop(Holocaust[i]-Hitlof); Hitlof+=1
    for k in range(len(Shaw)):
        for j in range(randint(5,10)*(12 if Var.level%3==0 else 1)):
            lXp.append([Ennemi.index[Shaw[k]-Musso].posX+randint(-25*(2 if Var.level%3==0 else 1),25*(2 if Var.level%3==0 else 1)), 
                        Ennemi.index[Shaw[k]-Musso].posY+randint(-25*(2 if Var.level%3==0 else 1),25*(2 if Var.level%3==0 else 1)),
                        0,0,time(),time()])
        lDed.append([Ennemi.index[Shaw[k]-Musso].posX, Ennemi.index[Shaw[k]-Musso].posY])
        Combat.index[Ennemi.index[Shaw[k]-Musso].combat][4]-=1; Ennemi.index.pop(Shaw[k]-Musso); Var.gStats[1]+=1; Musso+=1

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
                perso[0]=ImageTk.PhotoImage(Image.open('sprites/perso/'+perso[1]+str(animP[perso[2]][0])+'.png').resize((100, 100), Image.ANTIALIAS))
                weapon=ImageTk.PhotoImage(WeaponsP[int(Joueur.wStats[0])][int(Joueur.wStats[2])-1].rotate(angle*180/pi).resize((100, 100), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
            else:
                perso[0]=ImageTk.PhotoImage(Image.open('sprites/perso/'+perso[1]+str(animP[perso[2]][0])+'.png').resize((100, 100), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                weapon=ImageTk.PhotoImage(WeaponsP[int(Joueur.wStats[0])][int(Joueur.wStats[2])-1].rotate(180-angle*180/pi).resize((100, 100), Image.ANTIALIAS))
        animO[0][2]=ImageTk.PhotoImage(animO[0][3][animO[0][0]-1].resize((100, 180)))
        for i in range(len(Var.animE)):
            Var.animE[i][2]=Var.animE[i][6][Var.animE[i][0]-1]
            Var.animE[i][3]=Var.animE[i][7][Var.animE[i][0]-1]
        for i in range(len(Ennemi.index)):#Sprites Armes Ennemies
            size=(200 if Var.level%3==0 else 100)
            if ((Ennemi.index[i].posX)**2-Joueur.pos[0]**2)!=0 and Combat.index[Ennemi.index[i].combat][3]:
                if Joueur.pos[0]>Ennemi.index[i].posX:
                    angle=atan(((Ennemi.index[i].posY)-Joueur.pos[1])/((Ennemi.index[i].posX)-Joueur.pos[0])); Ennemi.index[i].angle=angle
                    Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(angle*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                else:
                    angle=pi+atan(((Ennemi.index[i].posY)-Joueur.pos[1])/((Ennemi.index[i].posX)-Joueur.pos[0])); Ennemi.index[i].angle=angle
                    Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(180-angle*180/pi).resize((size, size), Image.ANTIALIAS))
            elif (Combat.index[Ennemi.index[i].combat][3]==False and Ennemi.index[i].posX>Joueur.pos[0]-tk.winfo_screenwidth()/2-40 and Ennemi.index[i].posX<Joueur.pos[0]+tk.winfo_screenwidth()/2+40
            and Ennemi.index[i].posY>Joueur.pos[1]-tk.winfo_screenheight()/2-40 and Ennemi.index[i].posY<Joueur.pos[1]-tk.winfo_screenheight()/2+40):
                if Joueur.pos[0]>Ennemi.index[i].posX:Ennemi.index[i].img=ImageTk.PhotoImage(Image.open('sprites/armes/'+Ennemi.index[i].arme[1]+'/'+Ennemi.index[i].arme[1]+str(int(Ennemi.index[i].arme[2]))+'.png').rotate(0*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT))
                else:Ennemi.index[i].img=ImageTk.PhotoImage(WeaponsP[int(Ennemi.index[i].arme[0])][int(Ennemi.index[i].arme[2])-1].rotate(180-0*180/pi).resize((size, size), Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))
        affichage()

        for i in Ennemi.index:i.dmgAnimEnd()

    if state:tk.after(1, main)
    elif nL and Xp[1]>Xp[2]:#Menu selection mod.
        if time()-modList[2]>0.33:
            if lInput[0]:modList[1]+=1; modList[2]=time()
            if modList[1]>2:modList[1]=0
            if lInput[1]:modList[1]-=1; modList[2]=time()
            if modList[1]<0:modList[1]=2
        tk.after(1, main)
    elif nL:chargement()

def generationNiveau():
    global salles, monde, map, portal, state, lObj, lCoffre, lDed, nL, lXp, modList

    generation=True; lObj=[]; lCoffre=[]; Ennemi.index=[]; Combat.index=[]; lDed=[]; lXp=[]; Var.level+=1

    if Joueur.mods[6]==1:Joueur.mods[6]=0; Joueur.wStats=Var.arsenal[5]
    if Joueur.mods[7]==1:Joueur.mods[7]=0; Joueur.stats[1]=100

    modList[0]=[-1,-1,-1]
    for i in range(3):#Selection de la liste de modificateurs à proposer si lvl. up
        condition=True
        while condition:
            n=randint(0,5)
            if n not in modList[0]:condition=False
        modList[0][i]=n

    if Var.level%3==1 and Var.level!=1:Var.pression+=1
    while generation:#Layer du niveau
        generation=False; salles=[[[0,0] for i in range(5)] for j in range(5)]

        if Var.level%3!=0:#Niveau classique
            Joueur.pos=[randint(0,4), randint(0,4)]; salles[Joueur.pos[1]][Joueur.pos[0]]=[1,1]
            for i in range(4):
                condition=True; var=0
                while condition:
                    posP=[Joueur.pos[0], Joueur.pos[1]]; var+=1
                    if randint(0,1)==0:posP[0]+=randrange(-1,1,2)
                    else:posP[1]+=randrange(-1,1,2)
                    if posP[0]>=0 and Joueur.pos[0]<5 and posP[1]>=0 and Joueur.pos[1]<5:
                        if salles[posP[1]][posP[0]][0]!=1:condition=False
                    if var>10:condition=False; generation=True
                Joueur.pos[0]=posP[0]; Joueur.pos[1]=posP[1]
                if i==3:salles[posP[1]][posP[0]]=[1,2]
                else:
                    salles[posP[1]][posP[0]][0]=randint(2,3)
                    if randint(0,1)==0:posP[0]+=randint(-1,1)
                    else:posP[1]+=randint(-1,1)
                    if posP[0]>=0 and posP[0]<5 and posP[1]>=0 and posP[1]<5:
                        if salles[posP[1]][posP[0]][0]==0:salles[posP[1]][posP[0]]=[1,3]
        else:#Boss
            salles[3][2]=[1,1]; salles[2][2]=[3,0]; salles[1][2]=[1,2]

    Var.grille=[['0' for i in range(35*5)] for j in range(35*5)]; Var.grilleP=[['0' for i in range(35*5)] for j in range(35*5)]
    for i in range(5):#Création de la matrice
        for j in range(5):
            if salles[j][i][0]!=0:
                if salles[j][i][0]==1:
                    if salles[j][i][1]==1:Joueur.pos=[i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2]
                    elif salles[j][i][1]==2:portal=[i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2]
                    elif salles[j][i][1]==3:
                        lCoffre.append([True, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, 
                        ImageTk.PhotoImage(Image.open('sprites/props/coffreF.png').resize((75,75)))])
                    for o in range(i*35+12, i*35+23):
                        for p in range(j*35+12, j*35+23):Var.grille[p][o]=chr(randint(97, 105))
                if salles[j][i][0]==2:
                    for o in range(i*35+9, i*35+26):
                        for p in range(j*35+9, j*35+26):Var.grille[p][o]=chr(randint(97, 105))
                if salles[j][i][0]==3:
                        for o in range(i*35+6, i*35+29):
                            for p in range(j*35+6, j*35+29):Var.grille[p][o]=chr(randint(97, 105))
                
                if j>0:
                    if salles[j-1][i][0]!=0:
                        for o in range(i*35+15, i*35+20):
                            for p in range(j*35-20, j*35+20):
                                if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
                if j<4:
                    if salles[j+1][i][0]!=0:
                        for o in range(i*35+15, i*35+20):
                            for p in range(j*35+20, j*35+50):
                                if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
                if i>0:
                    if salles[j][i-1][0]!=0:
                        for o in range(i*35-20, i*35+20):
                            for p in range(j*35+15, j*35+20):
                                if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
                if i<4:
                    if salles[j][i+1][0]!=0:
                        for o in range(i*35+20, i*35+50):
                            for p in range(j*35+15, j*35+20):
                                if Var.grille[p][o]=='0':Var.grille[p][o]=chr(randint(97, 105))
    n=0; Combat.index=[]
    for i in range(5):#Création des Combat.index
        for j in range(5):
            if salles[j][i][0]==2:
                rand=randint(4,6);Combat.index.append([2, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand])
                with open('files/roomLayers/2/'+str(randint(0,5))+'.txt', 'r') as file:
                    var=0
                    for line in file:
                        for o in range(17):
                            if line[o]=='1':
                                Var.grille[j*(35)+9+o][i*(35)+9+var]='0'
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
                rand=randint(6,8);Combat.index.append([3, i*(35*40)+(35*40)/2, j*(35*40)+(35*40)/2, False, rand])
                with open('files/roomLayers/3/'+str(randint(0,3))+'.txt', 'r') as file:
                    var=0
                    for line in file:
                        for o in range(23):
                            if line[o]=='1':
                                Var.grille[j*(35)+6+o][i*(35)+6+var]='0'
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
            elif salles[j][i][0]==3:#Boss
                Combat.index.append([3, 2*(35*40)+(35*40)/2, 2*(35*40)+(35*40)/2, False, 1]); rand=randint(3,4)
                Ennemi.index.append(Ennemi(0, Var.bestiaire[rand][0], 2*(35*40)+(35*40)/2, 2*(35*40)+(35*40)/2, Var.bestiaire[rand][0], Var.bestiaire[rand][1], 0, 0, Var.bestiaire[rand][2],Var.arsenal[Var.bestiaire[rand][3]][:], 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[Var.bestiaire[rand][3]][1]+'/'+Var.arsenal[Var.bestiaire[rand][3]][1]+str(int(Var.arsenal[Var.bestiaire[rand][3]][2]))+'.png').resize((100, 100))), 
                    time(),0,Var.arsenal[Var.bestiaire[rand][3]][8], Var.bestiaire[rand][4], rand))

    monde=Image.open("sprites/level/blank.png")
    for i in range(35*5):
        for j in range(35*5):
            if Var.grille[j][i]!='0':Image.Image.paste(monde, Image.open("sprites/level/tiles/"+Var.grille[j][i]+".png"), (i*40, j*40))
            elif i>1 and i<35*5-2 and j>1 and j<35*5-2:
                if Var.grille[j+1][i]!='0' or Var.grille[j][i-1]!='0' or Var.grille[j][i+1]!='0' or Var.grille[j+1][i+1]!='0' or Var.grille[j+1][i-1]!='0':
                    Image.Image.paste(monde, Image.open("sprites/level/tiles/"+str(randint(1,3))+".png"), (i*40, j*40-20)); Var.grilleP[j][i]='a'
                if Var.grille[j-1][i]!='0':Var.grilleP[j][i]=str(randint(3,5))
    
    for i in range(35*5):#BLOC PROVISOIRE !!!!!
        for j in range(35*5):
            if i>1 and i<35*5-2 and j>1 and j<35*5-2:
                if Var.grilleP[j-1][i]=='a' and Var.grilleP[j][i]=='0' and Var.grille[j][i]=='0':Var.grilleP[j][i]=str(randint(3,5))

    map=ImageTk.PhotoImage(monde.resize((200, 200), Image.ANTIALIAS)); monde=ImageTk.PhotoImage(monde)

    state=True; nL=True
    main()

def clavier(event):
    global lInput, portal, state, lObj, lCoffre, state, nL, angle, modList, Xp
    var=event.keysym

    if var=='Right':lInput[0]=True
    if var=='Left':lInput[1]=True
    if var=='Up':lInput[2]=True
    if var=='Down':lInput[3]=True
    if var=='r':lInput[4]=True

    if var=='t':
        if Joueur.stats[4]>0:Joueur.powers[Joueur.stats[6]][1]=True; lInput[-1]=True
        else:Joueur.powers[Joueur.stats[6]][1]=False; lInput[-1]=False

    if var=='Escape':tk.destroy()

    if var=='y':
        if not state and nL and Xp[1]>Xp[2] and time()-modList[3]>0.5:
            Xp[2]+=1
            for i in range(6):
                if modsC[modList[0][modList[1]]][i]!=0:Joueur.mods[i]=Joueur.mods[i]*modsC[modList[0][modList[1]]][i]
            Joueur.mods[6]=modsC[modList[0][modList[1]]][6]; Joueur.mods[7]=modsC[modList[0][modList[1]]][7]

        if Joueur.stats[1]==0 and state:state=False; nL=False; init()
        if Joueur.pos[0]>portal[0]-50 and Joueur.pos[0]<portal[0]+50 and Joueur.pos[1]>portal[1]-90 and Joueur.pos[1]<portal[1]+90:state=False; modList[3]=time()
        else:
            for i in range(len(lObj)):
                if Joueur.pos[0]>lObj[i][2]-50 and Joueur.pos[0]<lObj[i][2]+50 and Joueur.pos[1]>lObj[i][3]-50 and Joueur.pos[1]<lObj[i][3]+50:
                    lObj.append([Joueur.wStats[0], Joueur.wStats[1], Joueur.pos[0], Joueur.pos[1], 
    ImageTk.PhotoImage(Image.open('sprites/armes/'+Joueur.wStats[1]+'/'+Joueur.wStats[1]+str(int(Joueur.wStats[2]))+'.png').resize((100, 100), Image.ANTIALIAS))])
                    Joueur.wStats=Var.arsenal[int(lObj[i][0])]; lObj.pop(i)
            for i in range(len(lCoffre)):
                if Joueur.pos[0]>lCoffre[i][1]-50 and Joueur.pos[0]<lCoffre[i][1]+50 and Joueur.pos[1]>lCoffre[i][2]-50 and Joueur.pos[1]<lCoffre[i][2]+50 and lCoffre[i][0]:
                    var=randint(0,5); lObj.append([var, Var.arsenal[var][1], lCoffre[i][1]+randint(-10,10), lCoffre[i][2]+randint(-10,10), 
                    ImageTk.PhotoImage(Image.open('sprites/armes/'+Var.arsenal[var][1]+'/'+Var.arsenal[var][1]+str(int(Joueur.wStats[2]))+'.png').resize((100, 100), Image.ANTIALIAS))])
                    lCoffre[i][0]=False; lCoffre[i][3]=ImageTk.PhotoImage(Image.open('sprites/props/coffreO.png').resize((75,75)))

def clavierRelease(event):
    global lInput
    var=event.keysym

    if var=='Right':lInput[0]=False
    if var=='Left':lInput[1]=False
    if var=='Up':lInput[2]=False
    if var=='Down':lInput[3]=False
    if var=='r':lInput[4]=False

    if var=='t':Joueur.powers[Joueur.stats[6]][1]=False; lInput[-1]=False

def twin(event):
    global curseur

    if Joueur.stats[1]>0:curseur=[event.x, event.y]

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