from PIL import Image, ImageTk
from time import time
from random import random, randint
from math import cos, sin, pi

from modules.globales import Var

class Joueur:

    powers=[]
    wStats=[]; stats=[0, 100, 100, 250, 100, 100, randint(0,2)]
    mods=[]

    pos=[-50, -50]

    def __init__(self):
        pass

class Combat:

    index=[]

    def __init__(self):
        pass

class Ennemi:

    index=[]

    def __init__(self, combat, firstSprite, posX, posY, sprite, pv, vitX, vitY, vit, arme, img, tic, angle, dmg, r, type):
        self.combat, self.firstSprite, self.posX = combat, firstSprite, posX
        self.posY, self.sprite, self.pv, self.vitX = posY, sprite, pv, vitX
        self.vitY, self.vit, self.arme, self.img = vitY, vit, arme, img
        self.tic, self.angle, self.dmg, self.r, self.type = tic, angle, dmg, r, type

    def comportement(self):
        if Combat.index[self.combat][3]:

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
                elif i not in Holocaust and Combat.index[Ennemi.index[j].combat][3]:
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
                    self.spawnX, self.spawnY=self.posX, self.posY
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

    def __init__(self):
        pass