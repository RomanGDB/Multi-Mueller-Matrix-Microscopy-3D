import numpy as np

#Desacoplar imagen y recuperar array en RGB

def desacoplar_matriz(A_show, dim = (1024,1224)):

  #Numero de Vectores
  M = A_show.shape[0]//dim[0]

  #Numero de Vectores
  N = A_show.shape[1]//dim[1]

  #Matriz de Mueller
  A = np.zeros((dim[0],dim[1],3,M,N), dtype=float)

  #Desacoplado
  for i in range(M):
    for j in range(N):
      for k in range(3):
        A[:,:,k,i,j] = A_show[i*dim[0]:(i+1)*dim[0],j*dim[1]:(j+1)*dim[1],k]

  return A