from random import *
import math
import turtle
import pycosat
import subprocess

s = turtle.getscreen()
turtle.hideturtle()
tu = turtle.Turtle(visible=False)
to = turtle.Turtle(visible=False)
wr = turtle.Turtle(visible = False)

wr.speed(0)
tu.speed(0)
to.speed(0)

pi = math.pi

# Programme qui cree un graphe G quelconque a n sommets pour n entre 0 et 10.

# On utilise une matrice d'adjacents, ou G = M pour M une matrice generee,
# M[i][j] = 1 signifie que les sommets i et j sont relies par un arete
# et M[i][j] = 0 singifie qu'il n'y a pas d'arete entre ces deux sommets.

###########################################################################################
# PARTIE INITIALISATION DU GRAPHE
###########################################################################################

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

def generer_graphe_connu(n): # fonction qui genere le graphe qu'on veut, 
  g = []                     # represente par une matrice d'adjacents
  for i in range(n):
      ligne = []
      for j in range(i):
         ligne.append(0)
      for j in range(i, n):
         if i!=j:
           #b = randint(0, 1)
           ligne.append(1)
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
        

def dessine_sommets(dic, n, r1):
      r = (r1+20) / (n+1)
      tu.fillcolor('white')
      tu.penup()
      tu.width(4)
      for i in range(n):
          (x, y) = dic[i+1][1]
          tu.goto(x, y)
          tu.pendown()
          tu.begin_fill()
          tu.circle(r)
          tu.end_fill()
          tu.penup()

def dessine_sommets_col(dic1, dic2, n, r1):
      r = (r1+20) / (n+1)
      tu.penup()
      tu.width(4)
      for i in range(n):
          col = dic2[i+1]
          tu.fillcolor(col)
          (x, y) = dic[i+1][1]
          tu.goto(x, y)
          tu.pendown()
          tu.begin_fill()
          tu.circle(r)
          tu.end_fill()
          tu.penup()

def dessine_aretes(dic, n, r1):
      r = (r1+20) / (n+1)
      to.penup()
      to.width(3)
      for i in range(n):
        
          (x1, y1) = dic[i+1][1]
           
          for j in dic[i+1][0]:
              (x2, y2) = dic[j][1]
              to.goto(x1, y1+r)
              to.pendown()
              to.goto(x2, y2+r)
              to.penup()

def dessine_graphe(dic, n, r, c, V):
   # dessine_sommets(dic, n)
    wr.penup()
    wr.setposition(0,200)
    wr.pendown()
    wr.write(f"{c}-coloration d'un graphe G a {n} sommets et {V} aretes", False, align ="center", font=("Consolas", 20, "normal"))
    wr.penup()
    dessine_aretes(dic, n, r)
    dessine_sommets(dic, n, r)

def dessine_solution(dic1, dic2, n, r, c, V):
   # dessine_sommets(dic, n)
    tu.clear()
    to.clear()
    wr.clear()
    wr.penup()
    wr.setposition(0,200)
    wr.pendown()
    wr.write(f"{c}-coloration d'un graphe G a {n} sommets et {V} aretes : solution", False, align ="center", font=("Consolas", 20, "normal"))
    wr.penup()
    dessine_aretes(dic, n, r)
    dessine_sommets_col(dic1, dic2, n, r)

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
                            # on lui assigne un chiffre entre 1 et n*m pour rendre possible l'interpretation DIMACS.
                            # on garde cette information dans un dictionnaire
    vari = liste_var(n, m)  
    dic = {}
    
    for i in range(n*m):
        dic[vari[i]] = i+1
        
    return dic

def fnc_en_dimacs(formule, n, m): # fonction qui convertis une formule FNC comme definie ci-dessus en format
                                  # DIMACS
    nb_variables = n*m
    nb_clauses = len(formule)
    dic = dic_vars_enumere(n, m)
    
    resultat = f"c on a {nb_variables} variables et {nb_clauses} clauses \n p cnf {nb_variables} {nb_clauses}\n"
    
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


def fnc_en_pycosat(formule, n, m):
  
    dic = dic_vars_enumere(n, m)
    f = []
    for clause in formule:
      li = []
      for lit in clause:
        if lit[0] == '-':
          l = dic[lit[1:]]
          li.append(-l)
        else:
          l = dic[lit]
          li.append(l)
      f.append(li)
    return f
          

def write_file_dimacs(formule, *N):
    (n, V, C) = N
    f = open(f"graphe_{n}_{V}_{C}.txt", "x")
    f.write(formule)
    f.close()
    print(f"fichier ecrit : graphe_{n}_{V}_{C}.txt")

def read_file_dimacs(*N):
    (n, V, C) = N
    f = open(f"graphe_{n}_{V}_{C}.txt", "r")
    print(f.read())
    f.close()

def read_solution(*N):
    (n , V, C) = N
    f = open(f"solution_{n}_{V}_{C}.txt", "r")
    print(f.read())
    f.close()
    
def parse_solution(*N):
    (n , V, C) = N
    f = open(f"solution_{n}_{V}_{C}.txt", "r")
    l = f.read()
    f.close()
    m = l[4:-3]
    parse = m.split(' ')
    return parse

def interpret_parse(liste):
    pos_vari = []
    for var in liste:
        if var[0] != '-':
          pos_vari.append(var)
    return pos_vari
  
def trouver_cle(v, dic):
    for var, vardim in dic.items():
      if vardim == int(v):
        return var
        
def reconvertir_de_dimacs(liste, dic):
    solution_convertie = []
    for var in liste:
      v = trouver_cle(var, dic)
      solution_convertie.append(v)
    return solution_convertie
      
    

####def write_solution(*N)
##    (n, V, C) = N
    
    
def solution(formule):
    sols = []
    for sol in pycosat.itersolve(formule):
      sols.append(sol)
      print(sol)
    return sols
  
###########################################################################################
# PARTIE TESTS
###########################################################################################

n = randint(0, 5)
#n = 5
G = generer_graphe(n)
G1 = generer_graphe_connu(n)
A = trouver_ens_aretes(G, n)
#C = gen_ens_couleurs(n)
C = [i+1 for i in range(randint(0, 5))]
c = n
V = len(A)
N = (n, V, c) # N for 'network' (= reseau), ce 3-uplet definie le graphe G en termes tres generaux
              # de n sommets, V aretes et C couleurs. on utiliesera ce 3-uplet pour la creation des fichiers.

r = 100              
dic = { i+1 : [[],0] for i in range(n) }
coords = coords_sur_circum(r, n)
d = remplir_dic(A, coords, dic) #dictionnaire des coordonnes des sommets

couleurs = {1 : 'red' , 2 : 'green', 3 : 'blue', 4 : 'cyan', 5 : 'magenta', 6 : 'yellow', 7 : 'orange', 8 : 'deeppink', 9 : 'lime', 10 : 'maroon'}

formule = formule_depuis_graphe(G, n, C)

def formule_int(forumle):
    f = []
    for i in formule:
      c = []
      for j in i:
        c.append(int(j))
      f.append(c)
    return f
  
#formuleint = formule_int(formule)
formuleint = fnc_en_pycosat(formule, n, len(C))
dic_var_dimac = dic_vars_enumere(n, c) # dictionnaire des variables et leurs chiffres DIMACS

#dimacs = fnc_en_dimacs(formule, n, c) # string de format DIMACS

print('n : ', n)
print('\n')
print('\n')
print('matrice d adjacents : \n', G)
print('\n')
print('\n')
print('ens d aretes : ', A)
print('\n')
print('\n')

print('dico ',d)
print('\n')

print(coords)
dessine_graphe(d, n, r, c, V)
print('\n')
print('\n')
print('\n')

print('ens de couleurs : ',C)
print('\n')

print('dic de var en forme dimacs : ', dic_var_dimac)
print('\n')
print('\n')
print('\n')

print('formule en fnc representee : ',formule)
print('\n')
print('\n')
print('\n')
print(formuleint)
sol = solution(formuleint)
#solution_convertie = reconvertir_de_dimacs(sol, dic_var_dimac)
##print(solution_convertie)

##write_file_dimacs(dimacs, *N)
##read_file_dimacs(*N)
##read_solution(*N)
##parse = parse_solution(*N)
##print(interpret_parse(parse))
##parse2 = interpret_parse(parse)
##solution_convertie = reconvertir_de_dimacs(parse2, dic_var_dimac)
##print(solution_convertie)

#dessine_solution(d, couleurs, n, r, c, V)

