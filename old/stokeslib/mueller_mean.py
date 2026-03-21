import numpy as np

# Promedia matriz de Mueller
#
# M[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)
#
# M_mean[:,:]: 
#                Primera componente: Dimensión vertical de la matriz (0,1,2)
#                Segunda componente: Dimensión horizontal de la matriz (0,1,2)
#

def mueller_mean(M):
    M_mean = np.zeros((3,3))
    for i in range(3):
      for j in range(3):
        M_mean[i,j] = np.round(np.mean(M[:,:,i,j]),1)
    return M_mean
  