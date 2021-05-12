from random import *
import math
import pycosat
import subprocess
from generer import *

def produit_cartesien(E):  # fonction qui genere un produit cartesien d'un ensemble,
    ExE = []               # sans couples de la forme (a, a), ou a est un elem. de l'ens.
    for e1 in E:
      for e2 in E:
        if e1 != e2:
          couple = (e1, e2)
          if not ((e2, e1) in ExE):
              ExE.append(couple)
    return ExE

def formule_depuis_graphe(G, n, C):
    aretes = trouver_ens_aretes(G, n)
    CxC = produit_cartesien(C)
    fnc = []

    for s in range(1, n+1):
        clause1 = [''.join((str(s), str(j))) for j in C] 
        fnc.append(clause1)
        for pair in CxC:
          c1 = pair[0]
          c2 = pair[1]
          clause3 = [''.join((str(-s), str(c1))), ''.join((str(-s), str(c2)))]
          fnc.append(clause3)
    
    for j in C:
        for couple in aretes:
            l = couple[0]
            k = couple[1]
            clause2 = [''.join((str(-l), str(j))), ''.join((str(-k), str(j)))] 
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
          

def write_file_dimacs(formule, file):
    
    f = open(f"{file}.txt", "x")
    f.write(formule)
    f.close()
    print(f"fichier ecrit : graphe_{file}.txt")

def read_file_dimacs(file):
    
    f = open(f"{file}.txt", "r")
    print(f.read())
    f.close()

def read_solution(file):
    
    f = open(f"{file}_sol.txt", "r")
    print(f.read())
    f.close()
    
def parse_solution(file):
    
    f = open(f"{file}_solution.txt", "r")
    l = f.read()
    f.close()
    m = l[4:-3]
    parse = m.split(' ')
    return parse

def extraire_solutions(sol, n):
    sols = []
    for s in sol:
      inter = []
      for var in s:
        if var > 0:
          #print(var)
          inter.append(var)
      if len(inter) == n:
        sols.append(inter)
    return sols

def interpret_parse(liste):
    pos_vari = []
    for var in liste:
        if var[0] != '-':
          pos_vari.append(var)
    return pos_vari
  
def trouver_cle(v, dic):
    for var, vardim in dic.items():
      if type(v) == int:
        if vardim == v:
          return var
      elif vardim == int(v):
          return var
        
def reconvertir_de_dimacs(liste, dic):
    solution_convertie = []
    for var in liste:
      
      v = trouver_cle(var, dic)
      print((var, v))
      solution_convertie.append(v)
    return solution_convertie
    
    
def solution(formule):
    sols = []
    for sol in pycosat.itersolve(formule):
      sols.append(sol)
      #print(sol)
    return sols
