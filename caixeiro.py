# Trabalho para matéria de Modelagem e Otimização Algoritimica
# Alunos: João Augusto da Silva Gomes e Vitor Felipe de Souza Siqueira
# Professor: Mateus Filipe Tavares Carvalho

# implementação do algoritmo de caixeiro viajante

import sys, random
from collections import deque

x = 1
if len(sys.argv) > 2:
  x = int(sys.argv[2])

#------------------------------------------------------------------------------------------------------

class Grafo:     # Classe que representa um Grafo
  def __init__(self, n):                                                      # Para cada vértice i, guarda uma lista com 4 informações:
    self.vertices = [[deque([]),None,None,None,None,None] for i in range(n)]             # [lista de adjacências, cor, pai, distancia, tempo inicial, tempo final]
    self.c = {}                                                             # Alfabeto com os pesos/capacidades de cada aresta

  def add_aresta(self, u, v, c):     # Adiciona uma aresta (u,v) de peso/capacidade 'c' no grafo
    if u in range(len(self.vertices)) and v in range(len(self.vertices)) and (u,v) not in self.c :
      self.vertices[u][0].append(v)
      self.c[(u,v)] = c

#------------------------------------------------------------------------------------------------------

#Busca em profundidade em um grafo
def DFS_VISIT(g, u, tempo, visitados):
  g.vertices[u][1] = 'C'
  tempo = tempo + 1
  g.vertices[u][4] = tempo
  visitados.append(u)
  for v in g.vertices[u][0]:
    if g.vertices[v][1] == 'B':
      g.vertices[v][2] = u
      g.vertices[v][3] = g.vertices[u][3] + g.c[(u,v)]
      tempo = DFS_VISIT(g, v, tempo, visitados)
  g.vertices[u][1] = 'P'
  tempo = tempo + 1
  g.vertices[u][5] = tempo
  return tempo

def DFS(g):
  for u in range(len(g.vertices)):
    g.vertices[u][1] = 'B'
    g.vertices[u][2] = None
    g.vertices[u][3] = 0
    g.vertices[u][4] = None
    g.vertices[u][5] = None
  tempo = 0
  visitados = []
  for v in range(len(g.vertices)):
    if g.vertices[v][1] == 'B':
      tempo = DFS_VISIT(g, v, tempo, visitados)
  return visitados

#------------------------------------------------------------------------------------------------------

def mochileiro(arquivo):
  # ler o arquivo de entrada
  entrada = open(arquivo, 'r')
  texto = entrada.readlines()
  entrada.close()

  # extrair as informações do arquivo
  n = len(texto)
  g = Grafo(n)

  # montar o grafo
  if len(texto[0].split()) != n:
    lista = [0 for i in range(n)]
    for i in range(n):
      cidade, coordx, coordy = texto[i].split()
      lista[int(cidade)-1] = (int(coordx), int(coordy))
    for i in range(n):
      for j in range(n):
        if i != j and (i,j) not in g.c:
          g.add_aresta(i, j, ((lista[i][0] - lista[j][0])**2 + (lista[i][1] - lista[j][1])**2)**(1/2))
  else:
    for i in range(n):
      linha = texto[i].split()
      for j in range(n):
        if i != j and (i,j) not in g.c:
          g.add_aresta(i, j, int(linha[j]))

  # calcular caminhos
  # roda DFS n*x vezes para combinaçoes aleatórias de vértices
  caminhos = []
  for i in range(n*x):
    caminho = DFS(g)
    dist = g.vertices[caminho[-1]][3]+g.c[(caminho[-1],caminho[0])]
    add = True
    for dado in caminhos:
      if dado[0] == dist:
        random.shuffle(g.vertices[i%n][0])
        add = False
        break
    if add:
      caminho.append(caminho[0])
      caminhos.append([dist, caminho])
      random.shuffle(g.vertices[i%n][0])

  # pega o caminho de menor custo
  caminho_minimo = min(caminhos)
  custo = caminho_minimo[0]
  visitados = caminho_minimo[1]

  print('caminho: ')
  for i in visitados:
    print('->' + str(i), end='')
  print('\ncusto: '+ str(custo))

sys.setrecursionlimit(10000)
mochileiro(sys.argv[1])