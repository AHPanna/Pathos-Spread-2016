# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:02:09 2016

@author: 3522343
"""
import random
import numpy as np

    #constantes a predefinir

size=100
nb_pers=1000
pt_eau=60
nb_inf=5
proba_inf=10
proba_dead=10
proba_immun=1

                  
def new(size,nb_pers,pt_eau,nb_inf,proba_inf, proba_dead, proba_immun):
    mat=np.zeros([size,size])
    n=mat.shape[0]
    m=mat.shape[1]
    cmp=0
    cpt=0
    c=0
    nb_mer=0
   
    
    if (pt_eau>0):
        while(nb_mer<3):
            i=random.randint(0,size-1)
            j=random.randint(0,size-1)
            mat[i,j]=-1
            while (cpt<pt_eau):
                for i in range(n):
                    for j in range(m):
                        k=random.randint(-1,1)
                        l=random.randint(-1,1)
                        if (mat[i,j]==-1 and mat[(i+k)%n,(j+l)%m]==0):
                            mat[(i+k)%n,(j+l)%m]=-1
                            cpt=cpt+1
            cpt=0
            nb_mer=nb_mer+1
        
    while (cmp<nb_pers):
        i=random.randint(0,size-1)
        j=random.randint(0,size-1)
        if (mat[i,j]==0):
            mat[i,j]=1
            cmp=cmp+1
    
    while (c<nb_inf):
        i=random.randint(0,size-1)
        j=random.randint(0,size-1)
        if (mat[i,j]==1):
            mat[i,j]=2
            c=c+1
    
    return mat #retourne la matrice avec tout les points.
    


        #changement des points dans mat avec des probabilités  
def iteration(cells,proba_inf,proba_dead,proba_immun):
    n=cells.shape[0]
    m=cells.shape[1]
    cpt_morts=0
    cells2 = np.copy(cells)
    etat2=np.copy(cells2)
    for i in range(n):
        for j in range(m):
            k=random.randint(-1,1)
            l=random.randint(-1,1)
            
        #deplacement des personnes (infectes et sains) 
            if (cells2[i,j]==1 and cells2[(i+k)%n,(j+l)%m]==0):
                cells2[(i+k)%n,(j+l)%m]=1
                etat2[(i+k)%n,(j+l)%m]=etat2[(i+k)%n,(j+l)%m]+1
                etat2[i,j]=etat2[i,j]-1            
            elif (cells2[i,j]==2 and cells2[(i+k)%n,(j+l)%m]==0):
                cells2[(i+k)%n,(j+l)%m]=2
                etat2[(i+k)%n,(j+l)%m]=etat2[(i+k)%n,(j+l)%m]+2
                etat2[i,j]=etat2[i,j]-2
            elif (cells2[i,j]==3 and cells2[(i+k)%n,(j+l)%m]==0):
                cells2[(i+k)%n,(j+l)%m]=3
                etat2[(i+k)%n,(j+l)%m]=etat2[(i+k)%n,(j+l)%m]+3
                etat2[i,j]=etat2[i,j]-3
              
        #infection des gens sains
            elif (cells2[i,j]==2 and cells2[(i+k)%n,(j+l)%m]==1):
                f=random.randint(1,100)           #pourcentage de chance d'etre infecte
                if (f>100-proba_inf):
                    cells2[(i+k)%n,(j+l)%m]=2
                    etat2[(i+k)%n,(j+l)%m]=etat2[(i+k)%n,(j+l)%m]+1
            
        #transformation des infectes (mort ou vif)
            if(cells2[i,j]==2):
                g=random.randint(1,1000)          #calcul du risque de mourir
                h=random.randint(1,1000)          #calcul de chance d'etre immunise contre la maladie
                if(g<=proba_dead):
                    etat2[i,j]=-5
                    cpt_morts=cpt_morts+1
                elif(h<=proba_immun):
                    etat2[i,j]=3
            
            
            if (etat2[i,j]==1):
                cells2[i,j]=1
            elif (etat2[i,j]==2) :
                cells2[i,j]=2
            elif (etat2[i,j]==3) :
                cells2[i,j]=3
            elif (etat2[i,j]==-1):
                cells2[i,j]=-1
            else:
                cells2[i,j]=0
    
    return cells2

def iteration_fin(mat,proba_inf,proba_dead,proba_immun):
    i=0
    while ((2 in mat) and (i<300)):
        mat=iteration(mat,proba_inf,proba_dead,proba_immun)
        i=i+1
#    print(i)
    return mat

def stats(mat,nb_personnes):
   
    survivants=0
    nb_immun=0
    n=mat.shape[0]
    m=mat.shape[1]
    for i in range(n):
        for j in range(m):
            if(mat[i,j]==3):
                nb_immun=nb_immun+1
            if(mat[i,j]==1):
                survivants=survivants+1
    survivants=nb_immun+survivants
    p_survivants=survivants*100/nb_personnes
    p_immun=nb_immun*100/nb_personnes
    p_morts=(nb_personnes-survivants)*100/nb_personnes
    return (p_morts,p_survivants,p_immun)



def simulation(size,nb_pers,pt_eau,nb_inf,proba_inf, proba_dead, proba_immun):
    
    cells=new(size,nb_pers,pt_eau,nb_inf,proba_inf, proba_dead, proba_immun)
    cells = iteration_fin(cells,proba_inf,proba_dead,proba_immun)
    p_morts,p_survivants,p_immun = stats(cells,nb_pers )
    
    return p_morts              #à modifier en fonction de l'objet d'étude




def moyenne(size,nb_pers,pt_eau,nb_inf,proba_inf, proba_dead, proba_immun,maxi):
    compteur=0
    somme=0
    while compteur<maxi:
        somme=somme+simulation(size,nb_pers,pt_eau,nb_inf,proba_inf, proba_dead, proba_immun)
        compteur=compteur+1
    return somme/maxi

cells=new(size,nb_pers,pt_eau,nb_inf,proba_inf,proba_dead,proba_immun)

from matplotlib import pyplot
from matplotlib import colors
import matplotlib.animation as animation

cmap = colors.ListedColormap(['cyan','grey','yellow','red','white'])
                      
import matplotlib.pyplot as plt
size = np.array(cells.shape)
dpi = 72
figsize= size[1]/float(dpi),size[0]/float(dpi)
fig = plt.figure(figsize = (10,10), dpi = dpi, facecolor = "white")
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
im=plt.imshow(cells, interpolation = 'nearest', cmap=cmap,vmin=-1,vmax=3)
plt.xticks([]), plt.yticks([])

def update(*args):
   global cells
   cells = iteration(cells,proba_inf,proba_dead,proba_immun)
   im.set_array(cells)
   return im,

ani = animation.FuncAnimation(fig, update, frames=range(20), interval=100)
plt.show()
        

#import matplotlib.pyplot as plt
#
#x = np.linspace(1,19,10)
#print(x)            #si jamais les x ne sont pas des entiers, le programme ne fonctionnera pas
#y = [moyenne(size,nb_pers,pt_eau,nb_inf,proba_inf,proba_dead,p,5) for p in x ]
#plt.plot(x,y,'ro')
#plt.show()
            