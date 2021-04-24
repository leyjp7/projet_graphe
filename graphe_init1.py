from random import *

# Programme qui cree un graphe G quelconque a n sommets pour n entre 0 et 10.

# On utilise une matrice d'adjacents, ou G = M pour M une matrice generee,
# M[i][j] = 1 signifie que les sommets i et j sont relies par un arete
# et M[i][j] = 0 singifie qu'il n'y a pas d'arete entre ces deux sommets.

n = randint(0, 10)

def generer_graphe(n):
  g = []
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
  
#def definition_graphe(n, g):
#  for i in range(0, n):
#    for j in range(0, n):
#      b = randint(0, 1)
#      g[i][j] = b
#  return g

def trouver_ens_aretes(G, n):
    ens = []
    for i in range(n):
      for j in range(n):
        if G[i][j] == 1:
          a = (i+1,j+1)
          ens.append(a)
    return ens

def gen_ens_couleurs(n):
    C = []
    m = randint(0, n)
    for i in range(0,m):
        C.append(i+1)
    return C
  
print(n)
G = generer_graphe(n)
print(G)
aretes = trouver_ens_aretes(G, n)
print(aretes)
C = gen_ens_couleurs(n)
print(C)
#G = definition_graphe(n, g)
#print(G)

