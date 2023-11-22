# Autores: Daniel Ortega de Carvalho          - Ra:170088
#          Gabriel Hiroaki da Silva Kanezaki  - Ra:179292

# Atividade Avaliativa: Google Maps

# Neste código é criada ou carregada uma imagem onde o 
# usuário escolhe os vértices e traça caminhos (arestas)
# sobre eles, indicando o peso de cada aresta.
# O algoritmo mostrará o caminho de menor custo e 
# mostrará o seu valor.

# Teclas de comando (segure a tecla por 1s para ativá-la):

# (v)   =    Vértices: clique com o botão esquerdo 
#            do mouse sobre o local. 
#            (ativado por padrão)

# (a)   =    Arestas: clique com o botão esquerdo 
#            dentro de um vértice e arraste o mouse
#            até o vértice e em seguida digite o
#            peso do vértice no pop-up que aparecer.

# (Espaço) = Resultado: digite o ponto inicial
#            e o ponto final do mapa no formato
#            'XY'. Exemplo: Vértices (A,B,C,D), 
#            para ir de A até C, digite 'AC'.


import numpy as np
import cv2
import networkx as nx
from tkinter import *
from scipy.spatial import distance
from math import atan, sin, cos, pi
from os import system

system('cls')

esp = 3
letra = 65
raio = 30

corV = (255,0,0)
corVc = (255,255,255)
corLV = (255,255,255)
corA = corV

# Imagem vazia
img = np.zeros((720,1280,3), np.uint8)

# Caso queria colocar a imagem de um mapa ou qualquer outra coisa
#img = cv2.imread('caminho/da/imagem.extensão',1)

res = img.shape

# listas das coordenadas dos vértices
Lvertices = []
# listas das coordenadas do início e do final
# de uma aresta
Larestas = []


def janela(texto, str):

    ar = []
    # a função valor, é uma função modular que
    # pode retornar número ou string, conforme
    # o argumento 'str' da função for 0 para float
    # e 1 para string
    def valor():
        if not str:
            try:
                f = float(a.get())
                valido = 1
            except:
                valido = 0
        
            if not valido:
                return
        else:
            f = a.get().upper()
        ar.append(f)
        main.destroy()

    # criação das tabelas (interface gráfica) utilizando a biblioteca Tkinter  
    main = Tk()
    main.title('')
    
    # criação de um texto na interface
    txt = Label(main, text=texto)
    txt.config(font=('Calibri', 20,'bold'),justify='center')
    txt.place(relx= 0.3, rely = 0.2)
    
    # criação de uma janela para que possamos digitar o valor
    a = Entry(main, font = ('Courier',20),width=10)
    a.place(relx=0.26,rely= 0.5)
    
    # criação do botão para executar, no caso ele executa a função 'valor'
    valorBotao = Button(main, text='  OK  ', command=valor, height = 1, width = 5, fg = '#303030', bg = '#888888')
    valorBotao.place(relx = 0.37, rely = 0.7)
    valorBotao.config(font=('Calibri', 15))
    
    # resulução da janela
    main.geometry('300x300')
    main.resizable(False, False)
    main.mainloop()
    
    # retorna um float ou uma string
    # conforme a função é chamada
    return ar[0]

def arestas(event,x,y,flags,param):
    global x0,y0, img
    
    # verifica e salva as coordenadas do clique do mouse
    if event==cv2.EVENT_LBUTTONDOWN:
        x0,y0 = x,y
    # ao soltar o clique do mouse são salva as novas
    # coordenadas e traça uma linha entre a primeira
    # e a segunda coordenada
    elif event==cv2.EVENT_LBUTTONUP:
        n0 = (0,0)
        n1 = (0,0)
        n0m = distance.euclidean((0,0),res[0],res[1])+10
        n1m = n0m
        ar0,ar1 = '-','-'
        
        # nesse laço é comparado a distância de cada vértice 
        # existente em relação as duas coordenadas obtidas
        # anteriormente e salva os vértices com as menores
        # distâncias, ou seja, salva os vértices mais próximos
        # do local onde foi clicado e solto o mouse, respectivamente,
        # e salva os nomes dos vértices (letras)
        for i, coord in enumerate(Lvertices):
            if distance.euclidean(coord, (x0,y0)) < n0m:
                n0m = distance.euclidean(coord, (x0,y0))
                n0 = coord
                ar0 = chr(i+65)

            if distance.euclidean(coord, (x,y)) < n1m:
                n1m = distance.euclidean(coord, (x,y))
                n1 = coord
                ar1 = chr(i+65)

        # valida o novo vértice que foi criado, com as seguintes
        # condições: o vértice liga arestas diferentes; a distância
        # entre a coordenada da aresta e o vértice não é maior que
        # o raio do vértice; não há arestas repetidas
        rep = True
        for k in Larestas:
            if k[0]+k[1] == ar0+ar1:
                rep = False
        cond = (n1!=n0) and (n1m<raio+esp) and (n0m<raio+esp) and rep

        # se o vétice está dentro das condições, ele será criado
        if cond:
            # toda essa parte abaixo se refere a um cálculo
            # trigonométrico desenvolvido para a linha (aresta) 
            # se conectar apenas às extremidades dos círculos (vértices)
            s = 1 if n0[0]<n1[0] else -1
            r = raio+esp
            try:
                alfa = atan((n0[1]-n1[1])/(n0[0]-n1[0]))
            except:
                sa = -1 if n0[1]<n1[1] else 1
                alfa = sa*1.5610878939607877

            x0y0 = int(s*r*cos(alfa)+n0[0]), int(s*r*sin(alfa)+n0[1]) 
            x1y1 = int(-s*r*cos(alfa)+n1[0]), int(-s*r*sin(alfa)+n1[1])

            # criação da linha do vértice
            cv2.line(img, x0y0, x1y1,(255,255,255),esp*3)
            cv2.line(img, x0y0, x1y1,corA,esp)

            # chama a função janela, que retornará o peso da aresta
            # e salva o ponto inicial, final e o peso do vértice
            Larestas.append((ar0,ar1,{'weight':janela('Peso da\naresta '+ar0+ar1,0)}))

def vertices(event,x,y,flags,param):
    global x0,y0, img, letra
    cond = 0

    # verifica se um vértice está em cima do outro
    for coord in Lvertices:
        if distance.euclidean(coord,(x,y)) < raio*2 + 1:
            cond += 1

    # se a condição acima for falsa, entra no if
    # e efetuará a inserção de um novo vértice
    # com a próxima letra do alfabeto
    if event==cv2.EVENT_LBUTTONDOWN and not cond:
        x0,y0 = x,y
        cv2.circle(img, (x,y), raio, corV, cv2.FILLED, esp)
        cv2.circle(img, (x,y), raio, corVc, esp)
        cv2.putText(img, chr(letra), (x-8,y+8), cv2.FONT_HERSHEY_SIMPLEX,  
                   1, corLV, 2, cv2.LINE_AA) 
        Lvertices.append((x,y))
        letra += 1


def resultado():
    # esta função basciamente faz o papel da função aresta,
    # mas pinta de verde os vértice e as arestas que seguem
    # o caminho de custo mínimo
    global img
    cv2.circle(img, Lvertices[ord(ccm[0])-65], raio, (0,255,0), esp*3)
    for i in range(1,len(ccm)):
        n0 = Lvertices[ord(ccm[i-1])-65]
        n1 = Lvertices[ord(ccm[i])-65]
        # toda essa parte abaixo se refere a um cálculo
        # trigonométrico desenvolvido para a linha (aresta) 
        # se conectar apenas às extremidades dos círculos (vértices)
        s = 1 if n0[0]<n1[0] else -1
        r = raio+esp
        try:
            alfa = atan((n0[1]-n1[1])/(n0[0]-n1[0]))
        except:
            sa = -1 if n0[1]<n1[1] else 1
            alfa = sa*1.5610878939607877
        x0y0 = int(s*r*cos(alfa)+n0[0]), int(s*r*sin(alfa)+n0[1])
        x1y1 = int(-s*r*cos(alfa)+n1[0]), int(-s*r*sin(alfa)+n1[1])

        cv2.line(img, x0y0, x1y1,(0,255,0),esp*4)
        cv2.circle(img, Lvertices[ord(ccm[i])-65], raio, (0,255,0), esp*3)

# criação de uma janela do OpenCV
cv2.namedWindow('Mapas', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Mapas',res[1],res[0])

# pega dados do mouse e os envia para função vértices
cv2.setMouseCallback('Mapas',vertices)

# fica recebendo dados do teclado
# e do mouse para inserir vértices
# ou arestas e exibe os grafos até
# que a tecla espaço seja pressionada
# (termina o loop)
while(1):
    if cv2.waitKey(1) & 0xFF == ord('a'):
        imgBCKP = img
        cv2.setMouseCallback('Mapas',arestas)
    if cv2.waitKey(1) & 0xFF == ord('v'):
        cv2.setMouseCallback('Mapas',vertices)
    if cv2.waitKey(1) & 0xFF == 32:
        break
    cv2.imshow('Mapas',img)

# gerando um grafo
G = nx.Graph()
# insere o nome dos vértices 
G.add_nodes_from([chr(65+i) for i in range(len(Lvertices))])
# insere todas as arestas no formato: (1º aresta, 2º aresta, peso)
G.add_edges_from(Larestas)

# recebe o caminho a ser seguido
c = janela('Direção:',1)
cv2.destroyAllWindows()

# pega a aresta inicial (source) e a aresta final (target)
# da variável criada a cima 'c' e coloca na função
# do caminho mínimo de dijkstra e salva no vetor 'ccm',
# que estará no formato ['c[0]',...,'c[1]']
ccm = nx.dijkstra_path(G,source = c[0], target = c[1])

# armazena o tamanho do caminho mínimo 
tccm = nx.dijkstra_path_length(G,c[0],c[1])

# mostra o grafo final com o caminho mínimo e seu tamanho
resultado()

# mostra o resultado em forma de imagem
cv2.namedWindow('Mapas', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Mapas',res[1],res[0])
while(1):
    texto = 'Tamanho total de ' + c[0] + ' para ' + c[1] + ': ' + str(round(tccm,2))

    cv2.putText(img, texto, (int(res[1]*0.03),int(res[0]*0.95)), 
    cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), esp//2, cv2.LINE_AA)

    cv2.imshow('Mapas',img)
    if cv2.waitKey(1) & 0xFF == 32:
        break

cv2.destroyAllWindows()

               
