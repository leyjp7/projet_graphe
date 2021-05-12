from random import *
from fnc import *
from dessin import *
from generer import *
from pathlib import *
import os

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
# PARTIE TESTS
###########################################################################################

#n = randint(0, 10)
n = int(input("entrez un nombre de sommets entre 0 et 10 : "))
while (n>10 or n<0):
    print("nombre non accepté\n")
    n = int(input("entrez un nombre de sommets entre 0 et 10 : "))

#print("entrez un nombre d'aretes entre 0 et ", n*(n-1)/2," : ")
nb_aretes = int(input(f"entrez un nombre d'aretes entre 0 et {n*(n-1)/2} : "))
while (nb_aretes<0 or nb_aretes > n*(n-1)/2):
    print("nombre non accepté\n")
    nb_aretes = int(input(f"entrez un nombre d'aretes entre 0 et {n*(n-1)/2} : "))

nb_couleurs = int(input(f"entrez un nombre de couleurs entre 0 et {n} : "))
while (nb_couleurs <0 or nb_couleurs > n):
    print("nombre non accepté\n")
    nb_couleurs = int(input(f"entrez un nombre de couleurs entre 0 et {n} : "))
#n = 5
#G = generer_graphe(n)
#G1 = generer_graphe_connu(n)
G = generer_graphe_avec_nb_aretes(n, nb_aretes)
A = trouver_ens_aretes(G, n)
#C = gen_ens_couleurs(n)
C = [i+1 for i in range(nb_couleurs)]
c = len(C)
V = len(A)
N = (n, V, c) # N for 'network' (= reseau), ce 3-uplet definie le graphe G en termes tres generaux
              # de n sommets, V aretes et C couleurs. on utiliesera ce 3-uplet pour la creation des fichiers.

r = 100              
dic = { i+1 : [[],0] for i in range(n) }
coords = coords_sur_circum(r, n)
d = remplir_dic(A, coords, dic,n) #dictionnaire des coordonnes des sommets

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

dic_var_enum = dic_vars_enumere(n, c) # dictionnaire des variables et leurs chiffres DIMACS

dimacs = fnc_en_dimacs(formule, n, c) # string de format DIMACS
formuleint = fnc_en_pycosat(formule, n, len(C)) # fnc en format convenable pour pycosat

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

print('dic de var en forme dimacs : ', dic_var_enum)
print('\n')
print('\n')
print('\n')

print('formule en fnc representee : ',formule)
print('\n')
print('\n')
print('\n')
#print(formuleint)

file = input(f"entrez un nom du fichier dimacs : ")

while Path(f"{file}.txt").is_file():
    file = input(f"Un fichier avec ce titre existe deja. Entrez un autre nom du fichier dimacs : ")

write_file_dimacs(dimacs, file)
PATH = os.path.abspath(f"{file}.txt")
l = len(file+'txt')
l2 = len(PATH) - l
PATH2 = PATH[:l2-2]

decide_solver = int(input("veuillez choisir un SAT solver. entrez 1 pour pycosat et 2 pour minisat : "))
while (decide_solver != 1) and (decide_solver != 2):
    decide_solver = int(input("veuillez entrer un soit 1 soit 2. entrez 1 pour pycosat et 2 pour minisat : "))
if decide_solver == 2:
    print(f"pour utiliser minisat il faut passer par le bash. veuillez copier et utiliser la commande : minisat {PATH} {PATH2}/{file}_solution.txt")
    pret = False
    while pret == False:
        pret = input("veuillez indiquer quand vous avez lance minisat : ")
    parse = parse_solution(file)
    print(interpret_parse(parse))
    parse2 = interpret_parse(parse)
    sols = [parse2]
elif decide_solver == 1:
    sol = solution(formuleint)
    sols = extraire_solutions(sol, n)
    print(sols)

#solution_convertie = [reconvertir_de_dimacs(sol, dic_var_enum) for sol in sols ]
#print(solution_convertie)


if len(sols) > 0:
  solution_convertie = reconvertir_de_dimacs(sols[0], dic_var_enum)
  print(solution_convertie)
  dic_sol = implement_dic_solution(solution_convertie)
  print(dic_sol)
  dessine_solution(d, couleurs, n, r, c, V, dic_sol)
else:
  dessine_echec(n, c, V)

##read_file_dimacs(*N)
##read_solution(*N)

##print(interpret_parse(parse))
##parse2 = interpret_parse(parse)
##solution_convertie = reconvertir_de_dimacs(parse2, dic_var_enum)
##print(solution_convertie)


