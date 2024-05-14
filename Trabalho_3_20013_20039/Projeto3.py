
from PIL      import Image
from math     import*
import numpy as np

import os



def Parametrica_circunferencia(r,t):
    a = radians(t)
    return [r*cos(a),r*sin(a)]

def Parametrica_espiral(t):
    return [t*sin(t),t*cos(t)]

def Implicita_circunferencia(x,r):
    return sqrt(abs(pow(r,2) - pow(x,2)))


class desenho:
    # Construtor
    def __init__(self,quadro = None):
        # Cor dos pixels são brancos
        self.cor = (255,255,255);
        # Superficie que recebera o desenho
        self.quadro = quadro
    
    def setLayer(self,quadro):
        self.quadro = quadro
    
    def setColor(self,cor):
        self.cor = cor;

    def paint_pixel(self,i,j):
        self.quadro.putpixel((i,j),self.cor)
    
    # Translada um vertice de dx e dy
    def transladar(self,vertice,dx,dy):
        vertice[0] += dx 
        vertice[1] += dy
        return vertice


def projeto3(questao):
    # Dimensões da imagem
    IMG_WIDTH  = 200
    IMG_HEIGHT = 200

    # Raio unitario
    r = 1.0

    # Centro da imagem
    cx = 100
    cy = 100
    
    q1 = desenho()
    
    if questao == 1:
        questao1 = Image.new('RGB', (IMG_WIDTH+1, IMG_HEIGHT+1), (0, 0, 0))

        q1.setLayer(questao1)

        valores = np.arange(0.0, 360.0, 0.0001)
        for a in valores: 
            pi = Parametrica_circunferencia(r,a)
            
            pi[0] = 100*pi[0]
            pi[1] = 100*pi[1]

            
            ''' Transladando para [100,100] '''
            
            pi = [int(pi[0]),int(pi[1])]
            
            pi = q1.transladar(pi,cx,cy)
         
            q1.paint_pixel(pi[0],pi[1])
        
        questao1.save("questao1.png","png")

     
    
    if questao == 2:

        questao2a = Image.new('RGB', (IMG_WIDTH+1, IMG_HEIGHT+1), (0, 0, 0))

        q1.setLayer(questao2a)

        t  = 0.0
        passo = 0.1

        while t < 100:
            t += passo
            pi = Parametrica_espiral(t)
            
            pi = [int(pi[0]),int(pi[1])]
            
            pi = q1.transladar(pi,cx,cy)
            
            q1.paint_pixel(pi[0],pi[1])

        questao2a.save("questao2a.png","png")    
    
    if questao == 3:
        questao2b = Image.new('RGB', (IMG_WIDTH+1, IMG_HEIGHT+1), (0, 0, 0))

        q1.setLayer(questao2b)

        t  = 0.0

        while t < 100:
           
            dt = 1.0/sqrt(pow(cos(t) - t*sin(t),2)+pow(sin(t) + t*cos(t),2))
            t += dt
            
            pi = Parametrica_espiral(t)
            
            pi = [int(pi[0]),int(pi[1])]
            
            pi = q1.transladar(pi,cx,cy)

            q1.paint_pixel(pi[0],pi[1])
            

        questao2b.save("questao2b.png","png") 
        
    if questao == 4:   
        questao3 = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0))
        q1.setLayer(questao3)

        for i in range(IMG_WIDTH):
            for j in range(IMG_HEIGHT):

                x = i/float(IMG_WIDTH)
                y = j/float(IMG_HEIGHT)
                
                f1 = x + y - 1.0 # Primeira condição x+y>1
                f2 = pow(x,2) + pow(y-1.0,2) - 1.0 # Segunda condição x^2+(y-1)^2 = 1
                f3 = pow(x-1.0,2) + pow(y,2) - 1.0 # Terceira condição (x-1)^2+y^2 = 1
                
                if f1 > 0 and f2 < 0 and f3 < 0:
                    q1.paint_pixel(i,IMG_HEIGHT - (j+1))
    
        questao3.save("questao3.png","png") 
    
    if questao == 5:

        questao4 = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0))
        q1.setLayer(questao4)

        for i in range(IMG_WIDTH):
            for j in range(IMG_HEIGHT):

                x = 4*float(i)/IMG_WIDTH  - 2.0
                y = 4*float(j)/IMG_HEIGHT - 2.0   
                F1 = pow(y,2) - pow(x,3) + x
                
                x = 4*float(i+1)/IMG_WIDTH  - 2.0
                y = 4*float(j)/IMG_HEIGHT - 2.0 
                F2 = pow(y,2) - pow(x,3) + x
                
                x = 4*float(i)/IMG_WIDTH  - 2.0
                y = 4*float(j+1)/IMG_HEIGHT - 2.0 
                F3 = pow(y,2) - pow(x,3) + x

                count = 0
                T1 = [F1,F2,F3]
                for k in range(3):
                    if T1[k] < 0: count += 1
                #teoream de bozano (significa q passou pelo 0 em algum momento)
                if count == 1 or count == 2: 
                    if T1[0]*T1[1] <= 0:
                        if abs(T1[0]) < abs(T1[1]):
                            q1.paint_pixel(i,j)
                        else:
                            q1.paint_pixel(i+1,j)
                            
                    if T1[0]*T1[2] <= 0:
                        if abs(T1[0]) < abs(T1[2]):
                            q1.paint_pixel(i,j)
                        else:
                            q1.paint_pixel(i,j+1)
                            
                    if T1[1]*T1[2] <= 0:
                        if abs(T1[1]) < abs(T1[2]):
                            q1.paint_pixel(i+1,j)
                        else:
                            q1.paint_pixel(i,j+1)

        questao4.save("questao4.png","png")
    



def main():
    #imagens
    projeto3(1)
    projeto3(2)
    projeto3(3)
    projeto3(4)
    projeto3(5)
    



if __name__ == "__main__":
    main()