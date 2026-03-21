import numpy as np

#Devuelve matriz promediada y matriz de desviación de la matriz de instrumentación
#
# A[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2,3)
#
# A_mean[:,:,:]: 
#                Primera componente: Dimensión vertical de la matriz (0,1,2)
#                Segunda componente: Dimensión horizontal de la matriz (0,1,2,3)
#
def instrumentacion_media_std(A):
  A_mean = np.zeros((3,4,3))
  A_std = np.zeros((3,4,3))
  for k in range(3):
    for i in range(3):
      for j in range(4):
        A_mean[i,j,k] = np.mean(A[:,:,k,i,j])
        A_std[i,j,k] = np.std(A[:,:,k,i,j])
  return A_mean, A_std
