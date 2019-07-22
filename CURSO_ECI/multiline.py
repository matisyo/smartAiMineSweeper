import random
import numpy as np
class MultiLine():
    def __init__(self,alto,ancho,largo,new_game=True):
        self.player1=1
        self.player2=2
        self.unclear=0
        self.outside=-1
        
        self.end = False
        self.winner = 0
        
        self.current_player = self.player1
        
        self.alto = alto
        self.ancho = ancho
        self.largo = largo
        if new_game:
            self.moves = set([(i,j) for i in range(self.alto) for j in range(self.ancho)])
            self.init_map()
        
    def init_map(self):
        tx = (self.alto+2*(self.largo-1))
        ty = (self.ancho+2*(self.largo-1))
        
        self.mapa = np.zeros(
            tx*ty
            ).reshape(tx,ty) + self.outside
        
        for i in range(self.alto):
            for j in range(self.ancho):
                self.mapa[i+self.largo-1][j+self.largo-1]= self.unclear
                                
    def check_col(self,x,y):
        mask_x = np.array([i for i in range(self.largo)])+x
        mask_y = (np.zeros(self.largo).astype(int)+self.largo-1+y)

        for i in range(self.largo):            
            if (self.mapa[mask_x+i,mask_y]==self.current_player).sum() == self.largo:
                return True
        return False     
       
    def check_row(self,x,y):
        mask_x = (np.zeros(self.largo).astype(int)+self.largo-1+x)
        mask_y = np.array([i for i in range(self.largo)])+y

        for i in range(self.largo):            
            if (self.mapa[mask_x,mask_y+i]==self.current_player).sum() == self.largo:
                return True
        return False  
    
    def check_diag_1(self,x,y):        
        mask_x = np.array([i for i in range(self.largo)])+x
        mask_y = np.array([i for i in range(self.largo)])+y

        for i in range(self.largo):            
            if (self.mapa[mask_x+i,mask_y+i]==self.current_player).sum() == self.largo:
                return True
        return False  
    def check_diag_2(self,x,y):        
        mask_x = np.array([i for i in range(self.largo)])+x
        mask_y = np.array([self.largo-1-i for i in range(self.largo)])+y        

        for i in range(self.largo):            
            if (self.mapa[mask_x+i,mask_y+i]==self.current_player).sum() == self.largo:
                return True
        return False  
    def move(self,x,y):
        if self.end:
            return
        if (x,y) in self.moves:
            self.moves.remove((x,y))
            self.mapa[x+self.largo-1][y+self.largo-1]=self.current_player
            if self.check_row(x,y) or \
                self.check_col(x,y) or \
                self.check_diag_1 (x,y) or \
                self.check_diag_2(x,y):
                self.end = True
                self.winner = self.current_player
            else:
                self.current_player = self.player1 if self.current_player==self.player2 else self.player2
        if len(self.moves)==0:
            self.end=True
            
            
    def copy(self):
        clon = MultiLine(self.alto,self.ancho,self.largo,new_game=False)        
        clon.end = self.end
        clon.winner = self.winner    
        clon.current_player = self.current_player
        clon.mapa = self.mapa.copy()
        clon.moves = self.moves.copy()
        
        return clon
    
    def autoplay(self):
        while not self.end:
            self.move(*random.sample(self.moves,1)[0])
        return self.winner
    
    def show(self):
        k=self.largo-1
        kk=-1*k
        print(self.mapa[k:kk,k:kk])