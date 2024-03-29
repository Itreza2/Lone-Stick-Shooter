from tkinter  import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk

from modules.globales import Var
from modules.classes import *

#Fonction de refresh de la fenêtre Tk lors du jeu
def affichage(tk, can, lInput, curseur, state, weapon, modsText, fps, ded1, ded2,
              murH, mur, doorH, door, nL, map, filter, box, hud):
    can.delete('all')

    can.create_image(
        -Joueur.pos[0]+(tk.winfo_screenwidth()/2), -Joueur.pos[1]+(tk.winfo_screenheight()/2), image=Var.monde, anchor='nw'
    )
    can.create_image(Var.portal[0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.portal[1]-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                    image=Var.animO[0][2], anchor='center')
    if Joueur.pos[0]>Var.portal[0]-50 and Joueur.pos[0]<Var.portal[0]+50 and Joueur.pos[1]>Var.portal[1]-90 and Joueur.pos[1]<Var.portal[1]+90:
        can.create_text(Var.portal[0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.portal[1]-110-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                        text='Entrer dans le portail', anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(Var.lDed)):
        can.create_image(Var.lDed[i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lDed[i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2), image=(ded1 if Var.level%3!=0 else ded2), anchor='center')
    for i in range(len(Orbe.index)):
        can.create_oval(Orbe.index[i].posX-4-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Orbe.index[i].posY-4-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                        Orbe.index[i].posX+4-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Orbe.index[i].posY+4-Joueur.pos[1]+(tk.winfo_screenheight()/2), outline='green', fill='lightgreen')
    CheikPoint=[]
    for j in range(int((Joueur.pos[1]-tk.winfo_screenheight()/2)/40), int((Joueur.pos[1]+20)/40+3)):
        for i in range(len(Ennemi.index)):
            if Ennemi.index[i].posY<(j)*40+20 and (not Combat.index[Ennemi.index[i].combat].gauntlet or Combat.index[Ennemi.index[i].combat].actif) and i not in CheikPoint:
                if Ennemi.index[i].posX<Joueur.pos[0]:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][2], anchor='center')
                else:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][3], anchor='center')
                if j!=int((Joueur.pos[1]+20)/40+3)-1:CheikPoint.append(i)
                can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2)+8, image=Ennemi.index[i].img, anchor='center')
        for i in range(len(Var.monolith[0])):
            if Var.monolith[0][i][1]<(j)*40+20:
                img=(1 if Combat.index[Var.monolith[0][i][3]].actif else (0 if (Combat.index[Var.monolith[0][i][2]].Pop==0 and not Var.monolith[0][i][5]) else 2))
                can.create_image(Var.monolith[0][i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.monolith[0][i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                                 image=Var.monolith[1][img], anchor='center')
                if Combat.index[Var.monolith[0][i][3]].actif:
                    can.create_text(Var.monolith[0][i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.monolith[0][i][1]-50-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                                    text=str(int(26-(time()-Var.monolith[0][i][6]))), fill='red', font=('Arial', 18), anchor='center')
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
                if Var.grilleP[j][i]=='9':
                    if Var.grille[j+1][i]=='0' or Var.grilleP[j+1][i]==('2' or '9'):
                        can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=box[1], anchor='nw')
                    else:can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=box[0], anchor='nw')

    for i in range(len(Var.lCoffre)):
        can.create_image(Var.lCoffre[i][1]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lCoffre[i][2]-Joueur.pos[1]+(tk.winfo_screenheight()/2), image=Var.lCoffre[i][3], anchor='center')
        if Joueur.pos[0]>Var.lCoffre[i][1]-50 and Joueur.pos[0]<Var.lCoffre[i][1]+50 and Joueur.pos[1]>Var.lCoffre[i][2]-50 and Joueur.pos[1]<Var.lCoffre[i][2]+50 and Var.lCoffre[i][0]:
            can.create_text(Var.lCoffre[i][1]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lCoffre[i][2]-Joueur.pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Ouvrir Coffre', anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(Var.lObj)):
        can.create_image(Var.lObj[i][2]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lObj[i][3]-Joueur.pos[1]+(tk.winfo_screenheight()/2), image=Var.lObj[i][4], anchor='center')
        if Joueur.pos[0]>Var.lObj[i][2]-50 and Joueur.pos[0]<Var.lObj[i][2]+50 and Joueur.pos[1]>Var.lObj[i][3]-50 and Joueur.pos[1]<Var.lObj[i][3]+50:
            can.create_text(Var.lObj[i][2]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lObj[i][3]-Joueur.pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Ramasser : '+Var.lObj[i][1], anchor='center', fill='blue', font=('Arial', 12))

    for i in range(len(Var.monolith[0])):
        if (Joueur.pos[0]>Var.monolith[0][i][0]-50 and Joueur.pos[0]<Var.monolith[0][i][0]+50 and Joueur.pos[1]>Var.monolith[0][i][1]-50 and Joueur.pos[1]<Var.monolith[0][i][1]+50 
            and Combat.index[Var.monolith[0][i][2]].Pop==0 and not Var.monolith[0][i][4]):
            can.create_text(Var.monolith[0][i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.monolith[0][i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2)-50, 
                            text='Activer le Monolithe', anchor='center', fill='blue', font=('Arial', 12))

    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=Joueur.perso[0], anchor='center')
    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+8, image=weapon, anchor='center')
    for i in range(len(Joueur.powers)):
        if Joueur.powers[i][1]:can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=Joueur.powers[i][2], anchor='center')
    if Var.monolith[2]:can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2-35, image=hud[1], anchor='center')

    for j in range(int((Joueur.pos[1]+20)/40), int((Joueur.pos[1]+tk.winfo_screenheight()/2)/40+3)):
        for i in range(len(Ennemi.index)):
            if Ennemi.index[i].posY<(j)*40+20 and (not Combat.index[Ennemi.index[i].combat].gauntlet or Combat.index[Ennemi.index[i].combat].actif) and i not in CheikPoint:
                if Ennemi.index[i].posX<Joueur.pos[0]:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][2], anchor='center')
                else:can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                                image=Var.animE[Ennemi.index[i].sprite][3], anchor='center')
                CheikPoint.append(i)
                can.create_image(Ennemi.index[i].posX-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Ennemi.index[i].posY-Joueur.pos[1]+(tk.winfo_screenheight()/2)+8, image=Ennemi.index[i].img, anchor='center')
        for i in range(len(Var.monolith[0])):
            if Var.monolith[0][i][1]>(j)*40+20:
                img=(1 if Combat.index[Var.monolith[0][i][3]].actif else (0 if (Combat.index[Var.monolith[0][i][2]].Pop==0 and not Var.monolith[0][i][5]) else 2))
                can.create_image(Var.monolith[0][i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.monolith[0][i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                                 image=Var.monolith[1][img], anchor='center')
                if Combat.index[Var.monolith[0][i][3]].actif:
                    can.create_text(Var.monolith[0][i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.monolith[0][i][1]-50-Joueur.pos[1]+(tk.winfo_screenheight()/2),
                                    text=str(int(26-(time()-Var.monolith[0][i][6]))), fill='red', font=('Arial', 18), anchor='center')
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
                if Var.grilleP[j][i]=='9':
                    if Var.grille[j+1][i]=='0' or Var.grilleP[j+1][i]==('2' or '9'):
                        can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=box[1], anchor='nw')
                    else:can.create_image(i*40-Joueur.pos[0]+(tk.winfo_screenwidth()/2), j*40-Joueur.pos[1]+(tk.winfo_screenheight()/2)-20, image=box[0], anchor='nw')

    for i in range(len(Projectile.index)):#Affichage Projectiles
        can.create_oval(
            Projectile.index[i].posX-Projectile.index[i].r-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Projectile.index[i].posY-Projectile.index[i].r-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
            Projectile.index[i].posX+Projectile.index[i].r-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Projectile.index[i].posY+Projectile.index[i].r-Joueur.pos[1]+(tk.winfo_screenheight()/2),
            fill=Projectile.index[i].color, outline=Projectile.index[i].outline
        )
    Holocost=[]; Hitlof=0
    for i in range(len(Var.lText)):
        can.create_text(Var.lText[i][0]-Joueur.pos[0]+(tk.winfo_screenwidth()/2), Var.lText[i][1]-Joueur.pos[1]+(tk.winfo_screenheight()/2), 
                        text=Var.lText[i][3], fill=Var.lText[i][2], font=('Arial', Var.lText[i][6], 'bold'), anchor='center')
        if time()-Var.lText[i][4]>Var.lText[i][5]:Holocost.append(i)
    for i in range(len(Holocost)):Var.lText.pop(Holocost[i]-Hitlof); Hitlof+=1

    if Joueur.stats[1]>0 and nL:#UI partie en cours
        if state:#Jeu normal
            can.create_image(tk.winfo_screenwidth()-75, 75, image=hud[0], anchor='ne')
            can.create_image(tk.winfo_screenwidth()-75, 75, image=map[0], anchor='ne')
            ratio=7000-(2800 if (map[1][0] and map[1][1]) else (1400 if (map[1][0] or map[1][1] or map[1][2] or map[1][3]) else 0))
            correct=[1400 if (map[1][1] or map[1][3]) else 0, 1400 if (map[1][1] or map[1][2]) else 0]
            pl=[50 if ((map[1][1] or map[1][3]) and not (map[1][0] or map[1][2])) else (-50 if ((map[1][0] or map[1][2]) and not (map[1][1] or map[1][3])) else 0), 
                50 if ((map[1][1] or map[1][2]) and not (map[1][0] or map[1][3])) else (-50 if ((map[1][0] or map[1][3]) and not (map[1][1] or map[1][2])) else 0)]
            can.create_oval(tk.winfo_screenwidth()-275+((Joueur.pos[0]-correct[0])/ratio*200)-3+pl[0], 75+((Joueur.pos[1]-correct[1])/ratio*200)-3+pl[1],
                            tk.winfo_screenwidth()-275+((Joueur.pos[0]-correct[0])/ratio*200)+3+pl[0], 75+((Joueur.pos[1]-correct[1])/ratio*200)+3+pl[1], fill='pink')
            can.create_oval(tk.winfo_screenwidth()-275+((Var.portal[0]-correct[0])/ratio*200)-3+pl[0], 75+((Var.portal[1]-correct[1])/ratio*200)-3+pl[1],
                            tk.winfo_screenwidth()-275+((Var.portal[0]-correct[0])/ratio*200)+3+pl[0], 75+((Var.portal[1]-correct[1])/ratio*200)+3+pl[1], fill='blue')
            can.create_text(tk.winfo_screenwidth()-275, 300, text='Zone : '+str(Var.level), anchor='w', fill='gainsboro', font=('Ubuntu', 16))
            can.create_rectangle(75, 75, 102, 177, outline='white', width=3)
            can.create_rectangle(76, 76+(100/200*(200-Var.Xp[0])), 101, 177, fill='lightgreen', width=0)
            if Var.Xp[1]>Var.Xp[2]:can.create_text(88.5, 195, text='Niv. Sup !', anchor='center', fill='gainsboro', font=('Ubuntu', 16))
            can.create_text(75+(27/2), 75+51, text=str(Var.Xp[1]), fill='white', font=('Ubuntu', 22), anchor='center')
            can.create_rectangle(165, tk.winfo_screenheight()-75, 565, tk.winfo_screenheight()-100, width=3, outline='white', fill='black')
            can.create_rectangle(166, tk.winfo_screenheight()-76, 165+398/Joueur.stats[2]*Joueur.stats[1], tk.winfo_screenheight()-99, width=0, fill='brown')
            can.create_text(365, tk.winfo_screenheight()-87.5, text=str(Joueur.stats[1])+' / '+str(Joueur.stats[2]), anchor='center', fill='white')
            can.create_rectangle(165, tk.winfo_screenheight()-107, 565, tk.winfo_screenheight()-115, width=0, fill='white')
            can.create_rectangle(166, tk.winfo_screenheight()-107, 165+398/Joueur.stats[5]*Joueur.stats[4], tk.winfo_screenheight()-115, width=0, fill='lightblue')
            can.create_oval(75,tk.winfo_screenheight()-107-50, 175, tk.winfo_screenheight()-107+50, fill='gainsboro', outline='brown')
            can.create_image(125, tk.winfo_screenheight()-107, image=Joueur.powers[Joueur.stats[6]][2], anchor='center')
            if Var.level%3==0 and Combat.index[0].actif:#Barre de vie du Boss
                try:
                    can.create_rectangle(tk.winfo_screenwidth()/2-300, 75, tk.winfo_screenwidth()/2+300, 115, outline='gainsboro')
                    can.create_rectangle(tk.winfo_screenwidth()/2-299, 76, tk.winfo_screenwidth()/2-299+598*(Ennemi.index[0].pv/int(Var.bestiaire[Ennemi.index[0].type][1]/(Var.lvlCoeff/2))),
                                        114, width=0, fill='brown')
                except IndexError:pass
        else:#Menu Selection mod.
            can.create_image(tk.winfo_screenwidth()/4, 0, image=filter, anchor='nw')
            can.create_text(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/6, text='NIV.  SUP.  !', fill='blue', font=('Papyrus', 34))
            for i in range(3):
                can.create_rectangle(tk.winfo_screenwidth()/2-137.5+i*100, (tk.winfo_screenheight()-75)/2,
                                     tk.winfo_screenwidth()/2-137.5+i*100+75, (tk.winfo_screenheight()+75)/2,
                                     outline=('red' if Var.modList[1]==i else 'black'))
            can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2+250, image=modsText[Var.modList[0][Var.modList[1]]], anchor='center')

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

#Même chose mais pour les menus séparés, histoire de rendre le tout plus lisible...
def affichageMenus(tk, can, menuState, config, bg):
    if menuState[2]==True:
        can.delete('all')

        #Ouai je me suis emmelé les pinceaux, donc système D ! 
        can.create_image(-bg[1]+tk.winfo_screenwidth()/2,-bg[2]+tk.winfo_screenheight()/2,image=bg[0], anchor='nw')

        if menuState[0]=='Main':
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2-200,
                            text='Lone Stick Shooter', font=('Ubuntu', 44, 'bold'), fill='gainsboro' ,anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2-150,
                            text='(Un twin stick shooter, mais avec un seul stick)', font=('Ubuntu', 17), fill='lightblue' , anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2-70, text='Jouer', 
                            font=('Ubuntu', 35 if menuState[1]==0 else 25), fill=('yellow' if menuState[1]==0 else 'white') , anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2, text='Commandes', 
                            font=('Ubuntu', 35 if menuState[1]==1 else 25), fill=('yellow' if menuState[1]==1 else 'white') , anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2+70, text='Quitter', 
                            font=('Ubuntu', 35 if menuState[1]==2 else 25), fill=('yellow' if menuState[1]==2 else 'white') , anchor='w')
        
        if menuState[0]=='lvl':
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2-150,
                            text='Niveau de Difficulté :', font=('Ubuntu', 25, 'bold'), fill='gainsboro' , anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2-70, text='Facile', 
                            font=('Ubuntu', 35 if menuState[1]==0 else 25), fill=('lightgreen' if menuState[1]==0 else 'white') , anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2, text='Normal', 
                            font=('Ubuntu', 35 if menuState[1]==1 else 25), fill=('yellow' if menuState[1]==1 else 'white') , anchor='w')
            can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2+70, text='Hardcore', 
                            font=('Ubuntu', 35 if menuState[1]==2 else 25), fill=('red' if menuState[1]==2 else 'white') , anchor='w')

        if menuState[0]=='Binds':
            for i in range(len(Var.binds)):
                can.create_text(tk.winfo_screenwidth()/8, tk.winfo_screenheight()/2+70*(i-menuState[1]), text=Var.binds[i][1], 
                                font=('Ubuntu', 25), fill=('lightblue' if menuState[1]==i else 'white') , anchor='w') 
                can.create_text(tk.winfo_screenwidth()/8+300, tk.winfo_screenheight()/2+70*(i-menuState[1]), text=Var.binds[i][2], 
                                font=('Ubuntu', 35 if menuState[1]==i else 25), fill=(
                                    ('orange' if config else 'yellow') if menuState[1]==i else 'white') , anchor='w')     