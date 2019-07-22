#pip install termcolor
import numpy as np
from random import sample
from termcolor import colored

class MineSweeper(object):
    C_BOMBA = -2
    C_UKN = -1
    def __init__(self,alto=10,ancho=10,bomba=1,neverends=False):
        self.alto=alto
        self.ancho=ancho
        self.bomba=bomba                          
        self.matriz_juego = np.array(np.zeros(alto*ancho))
        self.matriz_usuario = np.array(np.ones(alto*ancho)*self.C_UKN)        
        for t in sample([i for i in range(alto*ancho)],bomba):
            self.matriz_juego[t]=self.C_BOMBA
        self.numerea()
        self.unclicked = alto*ancho-bomba
        self.gameover = False
        self.neverends = neverends
        
    def get_pos(self,i,j):
        return i*self.ancho+j
    def get_loc(self,n):
        return n//self.ancho,n%self.ancho

    def isBomb(self,i,j):
        if i<0 or j<0:
            return 0
        if i>=self.alto or j>=self.ancho:
            return 0
        if self.matriz_juego[self.get_pos(i,j)] == self.C_BOMBA:
            return 1
        return 0

    def numerea(self):
        for i in range(self.alto):
            for j in range(self.ancho):
                if self.matriz_juego[self.get_pos(i,j)] == self.C_BOMBA:
                    continue
                cont = 0
                cont += self.isBomb(i+1,j)
                cont += self.isBomb(i-1,j)
                cont += self.isBomb(i,j+1)
                cont += self.isBomb(i,j-1)
                cont += self.isBomb(i+1,j+1)
                cont += self.isBomb(i+1,j-1)
                cont += self.isBomb(i-1,j+1)
                cont += self.isBomb(i-1,j-1)
                self.matriz_juego[self.get_pos(i,j)]=cont    
        
    def colores(self,letra):
        if letra == self.C_BOMBA:
            return f"{colored('B', 'red')}"
        if letra == 0:
            return f"{colored(0, 'white')}"
        if letra == self.C_UKN:
            return f"{colored('#', 'green')}"
        return f"{int(letra)}"
   
    def pretty_print(self,player=False):            
        if player:
            matriz = self.matriz_usuario.reshape(self.alto,self.ancho)
        else:
            matriz = self.matriz_juego.reshape(self.alto,self.ancho)
        for row in matriz:
            fila = ""
            for space in row:
                fila+=f"{self.colores(space)} "
            print(fila)
            
             
    def colores_peso(self,letra):
        letra = int(letra*10)
        if letra>=8:
            return f"{colored(8, 'green')}"
        if letra>=6:
            return f"{colored(6, 'yellow')}"
        if letra>=4:
            return f"{colored(4, 'white')}"
        if letra>=2:
            return f"{colored(2, 'grey')}"            
        return f"{colored(0, 'red')}"
            
    def pretty_weight(self,weights):        
        matriz = weights.reshape(self.alto,self.ancho)
        a = np.min(weights)
        b = np.max(weights)
        for row in matriz:
            fila = ""
            for num in row:
                space = (num-a)/(b-a)
                fila+=f"{self.colores_peso(space)} "
            print(fila)
        
    def click(self,i,j):
        if i<0 or j<0:
            return 0
        if i>=self.ancho or j >= self.alto:
            return 0
        if self.matriz_usuario[self.get_pos(i,j)]!=self.C_UKN:
            return 0
        if self.matriz_juego[self.get_pos(i,j)]==self.C_BOMBA:
            self.matriz_usuario[self.get_pos(i,j)] = self.matriz_juego[self.get_pos(i,j)]
            if not self.neverends:
                self.gameover = True
            return -1 
        self.unclicked -= 1
        if self.unclicked == 0:
            self.gameover = True
        
        self.matriz_usuario[self.get_pos(i,j)] = self.matriz_juego[self.get_pos(i,j)]        
        cant = 1
        #if self.matriz_juego[self.get_pos(i,j)]==0:        
        #    cant += self.click(i+1,j)
        #    cant += self.click(i-1,j)
        #    cant += self.click(i,j+1)
        #    cant += self.click(i,j-1)
        #    cant += self.click(i+1,j+1)
        #    cant += self.click(i-1,j+1)
        #    cant += self.click(i+1,j-1)
        #    cant += self.click(i-1,j-1)
                
        return cant