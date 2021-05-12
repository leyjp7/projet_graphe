from random import *
import math


# Programme qui cree un graphe G quelconque a n sommets pour n entre 0 et 10.

# On utilise une matrice d'adjacents, ou G = M pour M une matrice generee,
# M[i][j] = 1 signifie que les sommets i et j sont relies par un arete
# et M[i][j] = 0 singifie qu'il n'y a pas d'arete entre ces deux sommets.


def generer_graphe(n): # fonction qui genere quasi-aleatoirement un graphe quelconque, 
  g = []               # represente par une matrice d'adjacents
  for i in range(n):
      ligne = []
      for j in range(i):
         ligne.append(0)
      for j in range(i, n):
         if i!=j:
           b = randint(0, 1)
           ligne.append(b)
         else:
           ligne.append(0)
      
      g.append(ligne)
  return g

def generer_graphe_avec_nb_aretes(n, nb_aretes):
  g = []                # represente par une matrice d'adjacents
  
  for i in range(n):
      g.append( [ 0 for j in range(n) ] )
      
  if nb_aretes == 0:
    
    return g
  
  else:
   # nb_aretes = min(n*(n-1)/2, nb_aretes)
    for i in range(nb_aretes):
      s1 = randint(0, n-1)
      s2 = randint(0, n-1)
      while (s1 == s2 or g[min(s1,s2)][max(s1,s2)] == 1):
        s1 = randint(0, n-1)
        s2 = randint(0, n-1)
      g[min(s1,s2)][max(s1,s2)] = 1
    return g
      

def trouver_ens_aretes(G, n): # a partir d'un graphe quelconque et sa matrice d'adjacents, cette fonction
    ens = []                  # cree une liste des aretes du graphe, definis comme le couple des sommets qu'ils relient
    for i in range(n):
      for j in range(n):
        if G[i][j] == 1:
          a = (i+1,j+1)
          ens.append(a)
    return ens

def gen_ens_couleurs(n): #genere un ensemble de 'couleurs' representees par les entiers entre 0 et n
    C = []
    m = randint(0, n)
    for i in range(0,m):
        C.append(i+1)
    return C
