import cv2
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import splu


class Projection():
    def __init__(self,verticesProjecao,largura,altura):
        verticesTextura = np.array([[altura,0.0],[altura,largura],[0.0,largura],[0.0,0.0]])
        self.vertices = verticesProjecao
        self.textura = verticesTextura
        self.larguraT = largura
        self.alturaT = altura
        self.resolve_linear()
    
    def resolve_linear(self):
        # Sistema linear esparso
        vertice_expandido = np.empty((4, 3))
        textura_expandido = np.empty((4, 3))
        for i in range(0,4):
            vertice_expandido[i] = np.append(self.vertices[i],1)
            textura_expandido[i] = np.append(self.textura[i],1)

        P = textura_expandido
        Q = vertice_expandido
        #Para resolver o sistema linear usaremos Y0 = 1
               #a b c d e f g h i 0 1 2 3
        line = [0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,0.,0]
        matriz = np.array([line])
        for j in range(0,4):
            for i in range (0,3):
                line = np.zeros(13)
                line[3*i] = P[j][0]
                line[3*i+1] = P[j][1]
                line[3*i+2] = P[j][2]
                line[9+j] = -Q[j][i]
                matriz = np.concatenate((matriz, line[np.newaxis, :]), axis=0)
        A = csr_matrix(matriz)
        A = A.tocsc()
        b = np.zeros(13)
        b[0] = 1.0
        # Resolução usando `spsolve`
        #X= [a b c d e f g h i y0 y1 y2 y3]
        X = splu(A).solve(b)
        
        self.solution = X

        self.H = np.array([ 
            [X[0],X[1],X[2]],
            [X[3],X[4],X[5]],
            [X[6],X[7],X[8]]
            ])
        self.inversaDeH = np.linalg.inv(self.H)
    
    def isTextura(self,ponto):
        if ponto[0] >=  self.alturaT or ponto[1] >= self.larguraT or ponto[0]<0.0 or ponto[1]<0.0:
            return False
        return True
    


class Image():
    def __init__(self,textura,entrada):
        self.textura = textura
        self.entrada = entrada
        self.contagem = 0
        self.vertices = np.empty((4, 2))
        self.altura = textura.shape[0]
        self.largura = textura.shape[1]
        

    def mouse_callback(self,evento, x, y, flags, param):
        # Verifique se o botão esquerdo do mouse foi clicado
        
        if evento == cv2.EVENT_LBUTTONDOWN:
            # Imprima as coordenadas do ponto clicado
            self.vertices[self.contagem]= np.array([y,x])
            self.contagem+=1
            if self.contagem>=4:
                cv2.destroyAllWindows()
                self.projecao = Projection(self.vertices,largura= self.largura,altura= self.altura)
                self.projetar()

    def start(self,nome):

        cv2.imshow(nome, self.entrada)
        cv2.setMouseCallback(nome, self.mouse_callback)
        cv2.waitKey(0)
        

    def projetar(self):
        output = self.entrada
        for alt in range(self.entrada.shape[0]):
            for larg in range(self.entrada.shape[1]):
                    
                    ponto_textura = self.projecao.inversaDeH @ np.array([alt,larg,1]).T
                    x = round(ponto_textura[1]/ponto_textura[2])
                    y = round(ponto_textura[0]/ponto_textura[2])
                    # print(ponto_textura,self.textura.shape[0],self.textura.shape[1])
                    if self.projecao.isTextura(np.array([y,x])):

                        # print(ponto_textura)
                        #Projeção ortogonal
                        #Mudar a cor
                        output[alt, larg, 0] = self.textura[y,x,0] #red
                        output[alt, larg, 1] = self.textura[y,x,1] #green
                        output[alt, larg, 2] = self.textura[y,x,2] #blue


        cv2.imwrite('output.png', output)

def main():
    #imagens
    textura = cv2.imread('textura.png')
    entrada = cv2.imread('entrada.png')
    
    imagem = Image(textura=textura,entrada=entrada)
    nome = "Imagem"
    imagem.start(nome)



if __name__ == "__main__":
    main()