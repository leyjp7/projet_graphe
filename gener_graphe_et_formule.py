from random import *
import math
import turtle


s = turtle.getscreen()
t = turtle.Turtle()

pi = math.pi

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


def coords_sur_circum(r,n):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n)]
    

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

def formule_depuis_graphe(G, n, C):
    aretes = trouver_ens_aretes(G, n)
    fnc = []
    for j in range(len(C)):
            clause1 = [(i+1, j+1) for i in range(n)]
            fnc.append(clause1)
            for couple in aretes:
                l = couple[0]
                k = couple[1]
                clause2 = [(-l, j+1), (-k, j+1)]
                fnc.append(clause2)
    return fnc

def remplir_dic(A, coords, dic):
  
    for (l, k) in A:
        dic[l][0].append(k)
        dic[k][0].append(l)
        
    for i in range(n):
        dic[i+1][1] = coords[i]
    return dic
        

dic = { i+1 : [[],0] for i in range(n) }

coords = coords_sur_circum(70, n)

def dessine_sommets(dic, n):
      r = 70 / n
      t.penup()
      for i in range(n):
          (x, y) = dic[i+1][1]
          t.goto(x, y)
          t.pendown()
          t.circle(r)
          t.penup()

def dessine_aretes(dic, n):
      t.penup()
      for i in range(n):
        
          (x1, y1) = dic[i+1][1]
           
          for j in dic[i+1][0]:
              (x2, y2) = dic[j][1]
              t.goto(x1, y1)
              t.pendown()
              t.goto(x2, y2)
              t.penup()

def dessine_graphe(dic, n):
    dessine_sommets(dic, n)
    dessine_aretes(dic, n)
              
    
print(coords)

    

print('n : ', n)
G = generer_graphe(n)
print('matrice d adjacents : ', G)
print('\n')
A = trouver_ens_aretes(G, n)
print('ens d aretes : ', A)
d = remplir_dic(A, coords, dic)
print('dico ',d)
print('\n')
dessine_graphe(d, n)
print('\n')
print('\n')
print('\n')
C = gen_ens_couleurs(n)
print('ens de couleurs : ',C)
print('\n')
formule = formule_depuis_graphe(G, n, C)
print('formule en fnc representee : ',formule)
#G = definition_graphe(n, g)
#print(G)
