from random import *
import math
import turtle


s = turtle.getscreen()
t = turtle.Turtle(visible=False)
t.speed(0)



pi = math.pi

# Programme qui cree un graphe G quelconque a n sommets pour n entre 0 et 10.

# On utilise une matrice d'adjacents, ou G = M pour M une matrice generee,
# M[i][j] = 1 signifie que les sommets i et j sont relies par un arete
# et M[i][j] = 0 singifie qu'il n'y a pas d'arete entre ces deux sommets.

###########################################################################################
# PARTIE INITIALISATION DU GRAPHE
###########################################################################################

def generer_graphe(n): # fonction qui genere quasi-aleatoirement un graphe quelconque, 
  g = []              # represente par une matrice d'adjacents
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

#def creer_variable(*g):
#        (a, b) = g
#        var = ''.join((str(a),str(b)))
#        return var

###########################################################################################
# PARTIE FNC ET CONVERSION EN DIMACS
###########################################################################################

def formule_depuis_graphe(G, n, C):
    aretes = trouver_ens_aretes(G, n)
    fnc = []
    for j in range(len(C)):
            clause1 = [''.join((str(i+1), str(j+1))) for i in range(n)]
            fnc.append(clause1)
            for couple in aretes:
                l = couple[0]
                k = couple[1]
                clause2 = [''.join((str(-l), str(j+1))), ''.join((str(-k), str(j+1)))] 
                fnc.append(clause2)
    return fnc

def liste_var(n, m): #cree une liste de toute variable possible du probleme, ou 41 signifie que 
                    # le sommet 4 est de couleur 1, et -41 et la negation de cette variable
    vari = []
    
    for i in range(n):
        for j in range(m):

            var = ''.join((str(i+1), str(j+1)))
            vari.append(var)
            
    return vari

def dic_vars_enumere(n, m): # a chaque variable stockee dans la liste de toute variable possible,
                            # on lui assigne un chiffre entre 1 et n*m
                            # pour rendre possible l'interpretation DIMACS. on garde cette information
    vari = liste_var(n, m)  # dans un dictionnaire
    dic = {}
    
    for i in range(n*m):
        dic[vari[i]] = i+1
        
    return dic

def fnc_en_dimacs(formule, n, m): # fonction qui convertis une formule FNC comme definie ci-dessus en format
                                  # DIMACS
    nb_variables = n*m
    nb_clauses = len(formule)
    dic = dic_vars_enumere(n, m)
    
    resultat = f"p cnf {nb_variables} {nb_clauses}\n"
    
    for clause in formule:
        for lit in clause:
          if lit[0] == '-':
            l = dic[lit[1:]]
            resultat += f" -{l}"
          else:
            l = dic[lit]
            resultat += f" {l}"
        resultat += ' 0 \n'
    return resultat

def write_file_dimacs(formule, *N):
    (n, V, C) = N
    f = open(f"graphe_({n}-{V}-{C}).tct", "x")
    f.write(formule)
    f.close()

def read_file_dimacs(*N):
    (n, V, C) = N
    f = open(f"graphe_({n}-{V}-{C}).tct", "r")
    print(f.read())
    f.close()
    
  
###########################################################################################          
#PARTIE DESSIN DU GRAPHE
###########################################################################################

def coords_sur_circum(r,n): #calcule les coordonnes des sommets sur un plan
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n)]
  
def remplir_dic(A, coords, dic):
  for (l, k) in A:
      dic[l][0].append(k)
      dic[k][0].append(l)
        
  for i in range(n):
      dic[i+1][1] = coords[i]
  return dic
        

def dessine_sommets(dic, n):
      r = 80 / (n+1)
      t.fillcolor('black')
      t.penup()
      for i in range(n):
          (x, y) = dic[i+1][1]
          t.goto(x, y)
          t.pendown()
          t.begin_fill()
          t.circle(r)
          t.end_fill()
          t.penup()

def dessine_aretes(dic, n):
      r = 80 / (n+1)
      t.penup()
      for i in range(n):
        
          (x1, y1) = dic[i+1][1]
           
          for j in dic[i+1][0]:
              (x2, y2) = dic[j][1]
              t.goto(x1, y1+r)
              t.pendown()
              t.goto(x2, y2+r)
              t.penup()

def dessine_graphe(dic, n):
    dessine_sommets(dic, n)
    dessine_aretes(dic, n)
              


###########################################################################################
# PARTIE TESTS
###########################################################################################

n = randint(0, 10)
G = generer_graphe(n)
A = trouver_ens_aretes(G, n)
C = gen_ens_couleurs(n)
V = len(A)
N = (n, V, C) # N for 'network' (= reseau), ce 3-uplet definie le graphe G en termes tres generaux
              # de n sommets, V aretes et C couleurs. on utiliesera ce 3-uplet pour la creation des fichiers.
              
dic = { i+1 : [[],0] for i in range(n) }
coords = coords_sur_circum(70, n)
d = remplir_dic(A, coords, dic) #dictionnaire des coordonnes des sommets

formule = formule_depuis_graphe(G, n, C)
dic2 = dic_vars_enumere(n, len(C)) # dictionnaire des variables et leurs chiffres DIMACS

dimacs = fnc_en_dimacs(formule, n, len(C)) # string de format DIMACS

print('n : ', n)
print('\n')
print('\n')
print('matrice d adjacents : ', G)
print('\n')
print('\n')
print('ens d aretes : ', A)
print('\n')
print('\n')

print('dico ',d)
print('\n')

print(coords)
dessine_graphe(d, n)
print('\n')
print('\n')
print('\n')

print('ens de couleurs : ',C)
print('\n')

print('dic2 : ', dic2)
print('\n')
print('\n')
print('\n')

print('formule en fnc representee : ',formule)
print('\n')
print('\n')
print('\n')

write_file_dimacs(dimacs, *N)
read_file_dimacs(*N)

