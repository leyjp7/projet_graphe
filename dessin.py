import random
import math
import turtle
import pycosat
import subprocess

from fnc import *
from generer import *

s = turtle.getscreen()
turtle.hideturtle()
tu = turtle.Turtle(visible=False)
to = turtle.Turtle(visible=False)
wr = turtle.Turtle(visible = False)

wr.speed(0)
tu.speed(0)
to.speed(0)

pi = math.pi

def coords_sur_circum(r,n): #calcule les coordonnes des sommets sur un plan
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n)]
  
def remplir_dic(A, coords, dic, n):
  for (l, k) in A:
      dic[l][0].append(k)
      dic[k][0].append(l)
        
  for i in range(n):
      dic[i+1][1] = coords[i]
  return dic

def implement_dic_solution(sol):
    dic = {}
    for var in sol:
      if len(var) == 2:
          dic[int(var[0])] = int(var[1])
      elif len(var) == 3:
          dic[int(var[:2])] = int(var[2])
      elif len(var) == 4:
          dic[int(var[:2])] = int(var[2:])
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

def dessine_sommets_col(dic1, dic2, n, r1, sol):
      r = (r1+20) / (n+1)
      tu.penup()
      tu.width(4)
      for i in range(n):
          chf = sol[i+1]
          col = dic2[chf]
          tu.fillcolor(col)
          (x, y) = dic1[i+1][1]
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

def dessine_echec(n, c, V):
    wr.clear()
    wr.penup()
    wr.setposition(0,200)
    wr.pendown()
    wr.write(f"{c}-coloration d'un graphe G a {n} sommets et {V} aretes : pas de solution", False, align ="center", font=("Consolas", 20, "normal"))
    wr.penup()

def dessine_solution(dic1, dic2, n, r, c, V, sol):
   # dessine_sommets(dic, n)
    tu.clear()
    to.clear()
    wr.clear()
    wr.penup()
    wr.setposition(0,200)
    wr.pendown()
    wr.write(f"{c}-coloration d'un graphe G a {n} sommets et {V} aretes : solution", False, align ="center", font=("Consolas", 20, "normal"))
    wr.penup()
    dessine_aretes(dic1, n, r)
    dessine_sommets_col(dic1, dic2, n, r, sol)
