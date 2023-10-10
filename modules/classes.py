from PIL import Image, ImageTk
from time import time
from random import random, randint
from math import cos, sin, atan, pi, sqrt

from modules.globales import Var

class Joueur:

    powers=[]
    wStats=[]; stats=[0, 100, 100, 250, 100, 100, randint(0,2)]
    mods=[]
    perso=[None, 'Idle', 0]

    pos=[-50, -50]

    def __init__(self):
        pass

class Combat:

    index=[]

    def __init__(self, size, X, Y, actif, Pop):
        self.size, self.X, self.Y, self.actif, self.Pop = size, X, Y, actif, Pop

    def startnstop(self):
        if (self.actif==False and self.size==2 and self.Pop>0 and Joueur.pos[0]>self.X-8*40 and Joueur.pos[0]<self.X+8*40
        and Joueur.pos[1]>self.Y-8*40 and Joueur.pos[1]<self.Y+8*40-20):
            self.actif=True; Var.tac=0
            for j in range(5):
                if Var.grille[int(self.Y/40)-9][int(self.X/40)-2+j]!='0':
                    Var.grille[int(self.Y/40)-9][int(self.X/40)-2+j]='0';Var.grilleP[int(self.Y/40)-9][int(self.X/40)-2+j]='2'
                if Var.grille[int(self.Y/40)+9][int(self.X/40)-2+j]!='0':
                    Var.grille[int(self.Y/40)+9][int(self.X/40)-2+j]='0';Var.grilleP[int(self.Y/40)+9][int(self.X/40)-2+j]='2'
                if Var.grille[int(self.Y/40)-2+j][int(self.X/40)-9]!='0':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)-9]='0';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)-9]='2'
                if Var.grille[int(self.Y/40)-2+j][int(self.X/40)+9]!='0':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)+9]='0';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)+9]='2'
        if (self.actif==False and self.size==3 and self.Pop>0 and Joueur.pos[0]>self.X-11*40 and Joueur.pos[0]<self.X+11*40
        and Joueur.pos[1]>self.Y-11*40 and Joueur.pos[1]<self.Y+11*40-20):
            self.actif=True; Var.tac=0
            for j in range(5):
                if Var.grille[int(self.Y/40)-12][int(self.X/40)-2+j]!='0':
                    Var.grille[int(self.Y/40)-12][int(self.X/40)-2+j]='0';Var.grilleP[int(self.Y/40)-12][int(self.X/40)-2+j]='2'
                if Var.grille[int(self.Y/40)+12][int(self.X/40)-2+j]!='0':
                    Var.grille[int(self.Y/40)+12][int(self.X/40)-2+j]='0';Var.grilleP[int(self.Y/40)+12][int(self.X/40)-2+j]='2'
                if Var.grille[int(self.Y/40)-2+j][int(self.X/40)-12]!='0':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)-12]='0';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)-12]='2'
                if Var.grille[int(self.Y/40)-2+j][int(self.X/40)+12]!='0':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)+12]='0';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)+12]='2'
        if self.actif and self.Pop==0:
            self.actif=False; Projectile.index=[]
            for j in range(5):
                if Var.grilleP[int(self.Y/40)-9][int(self.X/40)-2+j]=='2':
                    Var.grille[int(self.Y/40)-9][int(self.X/40)-2+j]='1';Var.grilleP[int(self.Y/40)-9][int(self.X/40)-2+j]='0'
                if Var.grilleP[int(self.Y/40)+9][int(self.X/40)-2+j]=='2':
                    Var.grille[int(self.Y/40)+9][int(self.X/40)-2+j]='1';Var.grilleP[int(self.Y/40)+9][int(self.X/40)-2+j]='0'
                if Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)-9]=='2':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)-9]='1';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)-9]='0'
                if Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)+9]=='2':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)+9]='1';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)+9]='0'
                if Var.grilleP[int(self.Y/40)-12][int(self.X/40)-2+j]=='2':
                    Var.grille[int(self.Y/40)-12][int(self.X/40)-2+j]='1';Var.grilleP[int(self.Y/40)-12][int(self.X/40)-2+j]='0'
                if Var.grilleP[int(self.Y/40)+12][int(self.X/40)-2+j]=='2':
                    Var.grille[int(self.Y/40)+12][int(self.X/40)-2+j]='1';Var.grilleP[int(self.Y/40)+12][int(self.X/40)-2+j]='0'
                if Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)-12]=='2':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)-12]='1';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)-12]='0'
                if Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)+12]=='2':
                    Var.grille[int(self.Y/40)-2+j][int(self.X/40)+12]='1';Var.grilleP[int(self.Y/40)-2+j][int(self.X/40)+12]='0'

class Ennemi:

    index=[]

    def __init__(self, combat, firstSprite, posX, posY, sprite, pv, vitX, vitY, vit, arme, img, tic, angle, dmg, r, type):
        self.combat, self.firstSprite, self.posX = combat, firstSprite, posX
        self.posY, self.sprite, self.pv, self.vitX = posY, sprite, pv, vitX
        self.vitY, self.vit, self.arme, self.img = vitY, vit, arme, img
        self.tic, self.angle, self.dmg, self.r, self.type = tic, angle, dmg, r, type

    def comportement(self):
        if Combat.index[self.combat].actif:

            if ((time()-self.tic)>self.arme[6]*2 and ((self.vitX==0 and self.vitY==0) or Var.level%3==0) and Var.debordeur<1 
            and ((time()-Joueur.stats[0])<Joueur.wStats[6]/2 or (time()-Joueur.stats[0])>Joueur.wStats[6]*2)):
                self.tic=time(); Var.debordeur+=5
                for i in range(int(self.arme[4])+Var.pression):
                    disp=self.angle+(2*(0.75**Var.pression if Var.pression>0 else 1))*(-(self.arme[5]/2/180*pi)+random()*(self.arme[5]/180*pi))
                    Joueur.stats[0]=time(); self.arme[2]=3
                    Projectile.index.append(Projectile(
                        self.posX+(self.arme[3])*cos(disp), self.posY+8+(self.arme[3])*sin(disp), self.posX+(self.arme[3])*cos(disp), 
                        self.posY+8+(self.arme[3])*sin(disp), disp, self.arme[7]/(3*(0.85**Var.pression if Var.pression>0 else 1)),
                        False,  self.arme[8]/2, 'red', 'pink', self.dmg))

            if time()-Var.tac>2:
                if randint(1,4)!=1:self.vitX,self.vitY=randint(-1,1),randint(-1,1)
                else:self.vitX,self.vitY=0,0
                if Var.level%3==0:
                    self.arme=Var.arsenal[randint(Var.bestiaire[self.type][3], Var.bestiaire[self.type][3]+1)][:]
            posP=[self.posX,self.posY]
            posP[0]+=(time()-Var.frame)*self.vit*self.vitX;posP[1]+=(time()-Var.frame)*self.vit*self.vitY
            if (Var.grille[int((posP[1]+8)/40)][int((posP[0]-16)/40)]!='0' and Var.grille[int((posP[1]+8)/40)][int((posP[0]+16)/40)]!='0'
                and Var.grille[int((posP[1]+28)/40)][int((posP[0]-16)/40)]!='0' and Var.grille[int((posP[1]+28)/40)][int((posP[0]+16)/40)]!='0'):
                self.posX=posP[0]; self.posY=posP[1]
                if self.vitX!=0 or self.vitY!=0:
                    if (self.posX<Joueur.pos[0] and self.vitX==-1) or (self.posX>Joueur.pos[0] and self.vitX==1):self.sprite=2+self.firstSprite
                    else:self.sprite=1+self.firstSprite
                else:self.sprite=0+self.firstSprite
            else:self.sprite=0+self.firstSprite

    def dmgAnimEnd(self):
        if self.firstSprite==-3 or self.firstSprite==-6:self.firstSprite=Var.bestiaire[self.type][0]

class Projectile:
    index=[]

    def __init__(self, posX, posY, spawnX, spawnY, angle, vit, friendly, r, color='black', outline='black', dmg=0):
        
        self.posX, self.posY, self.spawnX, self.spawnY, self.angle, self.dmg = posX, posY, spawnX, spawnY, angle, dmg
        self.vit, self.spawnT, self.friendly, self.r, self.color, self.outline = vit, time(), friendly, r, color, outline
    
    def actualisation(self):
        self.posX=self.spawnX+((time()-self.spawnT)*self.vit)*cos(self.angle)
        self.posY=self.spawnY+((time()-self.spawnT)*self.vit)*sin(self.angle)

    def collision(self, i, Holocaust, Shaw):
        retour=[False, []]

        if Var.grille[int((self.posY+20)/40)][int((self.posX)/40)]=='0':retour[0]=True
        elif self.friendly:
            for j in range(len(Ennemi.index)):
                if (Ennemi.index[j].posX-Var.bestiaire[Ennemi.index[j].type][5]>=self.posX+2 or Ennemi.index[j].posX+Var.bestiaire[Ennemi.index[j].type][5]<=self.posX-2 or
                    Ennemi.index[j].posY-Var.bestiaire[Ennemi.index[j].type][6]>=self.posY+2 or Ennemi.index[j].posY+Var.bestiaire[Ennemi.index[j].type][6]<=self.posY-2):pass
                elif i not in Holocaust and Combat.index[Ennemi.index[j].combat].actif:
                    Ennemi.index[j].firstSprite=(-6 if Var.level%3!=0  else -3)
                    if randint(1, (int(Joueur.wStats[9]/Joueur.mods[4]) if int(Joueur.wStats[9]/Joueur.mods[4])>=1 else 1))==1:
                        if Joueur.wStats[-1]==0:retour[0]=True
                        Ennemi.index[j].pv-=Joueur.wStats[8]*(1.5*Joueur.mods[5])*Joueur.mods[0]
                        Var.lText.append([self.posX, self.posY, 'orange', str(-Joueur.wStats[8]*(1.5*Joueur.mods[5])*Joueur.mods[0])[:5], time(),0.2, 14])
                    else:
                        if Joueur.wStats[-1]==0:retour[0]=True
                        Ennemi.index[j].pv-=Joueur.wStats[8]*Joueur.mods[0]
                        Var.lText.append([self.posX, self.posY, 'yellow', str(-Joueur.wStats[8]*Joueur.mods[0])[:5], time(),0.2, 12])
                    if Ennemi.index[j].pv<=0 and j not in Shaw:retour[1].append(j)
        elif not self.friendly:
            if (Joueur.pos[0]-18>=self.posX+2 or Joueur.pos[0]+18<=self.posX-2 or
                Joueur.pos[1]-22>=self.posY+2 or Joueur.pos[1]+22<=self.posY-2):pass
            elif i not in Holocaust:
                if Joueur.powers[0][1] and Joueur.stats[4]>10:
                    Var.lText.append([self.posX, self.posY, 'lightblue', str(-self.dmg), time(),0.2, 16])
                    self.spawnX, self.spawnY=self.posX, self.posY; self.vit=self.vit*2
                    self.angle+=pi; self.spawnT=time(); self.friendly=True; self.color,self.outline='lightblue','lightgreen'
                else:
                    boule=True
                    if Joueur.stats[1]<=0:boule=False
                    retour[0]=True;Joueur.stats[1]-=self.dmg
                    if Joueur.stats[1]<0:
                        Joueur.stats[1]=0; Joueur.powers[Joueur.stats[6]][1]=False
                        if boule:Var.gStats[0]=time()-Var.gStats[0]
                    Var.lText.append([self.posX, self.posY, 'red', str(-self.dmg), time(),0.2, 16])
        
        return retour

class Orbe:

    index=[]

    def __init__(self, posX, posY, vitX, vitY):
        self.posX, self.posY, self.vitX, self.vitY = posX, posY, vitX, vitY
        self.tic, self.t = time(), time()

    def move(self, i, Adolf):
        if sqrt((Joueur.pos[0]-self.posX)**2+(Joueur.pos[1]-self.posY)**2)<25:
            Adolf.append(i); Var.Xp[0]+=1.2
            if Var.Xp[0]>=200:Var.Xp[0]-=200; Var.Xp[1]+=1
        elif sqrt((Joueur.pos[0]-self.posX)**2+(Joueur.pos[1]-self.posY)**2)<300:#calcul vitesse en fonction de la distance au joueur
            #Calcul de l'angle entre le joueur et l'orbe
            angleO=None
            if (self.posX>Joueur.pos[0]):angleO=atan((self.posY-Joueur.pos[1])/(self.posX-Joueur.pos[0]))
            else:angleO=pi+atan((self.posY-Joueur.pos[1])/(self.posX-Joueur.pos[0]))
            #Attribution de la nouvelle vitesse
            self.vitX=-(300-sqrt((Joueur.pos[0]-self.posX)**2+(Joueur.pos[1]-self.posY)**2))*1.5*cos(angleO)
            self.vitY=-(300-sqrt((Joueur.pos[0]-self.posX)**2+(Joueur.pos[1]-self.posY)**2))*1.5*sin(angleO)
        else:self.vitX, self.vitY=0,0
        self.posX+=self.vitX*(time()-self.tic); self.posY+=self.vitY*(time()-self.tic)
        self.tic=time()

        return Adolf