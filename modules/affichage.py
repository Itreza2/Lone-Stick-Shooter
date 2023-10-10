from tkinter  import Tk, Canvas, PhotoImage
from PIL import Image, ImageTk

from modules.globales import Var
from modules.classes import *

def affichage(tk, can, lInput, curseur, state, weapon, modsText, fps, ded1, ded2,
              murH, mur, doorH, door, nL, map, filter):
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

    can.create_image(tk.winfo_screenwidth()/2, tk.winfo_screenheight()/2, image=Joueur.perso[0], anchor='center')
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
            can.create_oval(tk.winfo_screenwidth()-275+(Var.portal[0]/7000*200)-3, 75+(Var.portal[1]/7000*200)-3,
                            tk.winfo_screenwidth()-275+(Var.portal[0]/7000*200)+3, 75+(Var.portal[1]/7000*200)+3, fill='blue')
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
                    can.create_rectangle(tk.winfo_screenwidth()/2-299, 76, tk.winfo_screenwidth()/2-299+598*(Ennemi.index[0].pv/Var.bestiaire[Ennemi.index[0].type][1]),
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