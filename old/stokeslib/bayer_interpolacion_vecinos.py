import numpy as np

# Interpolación por vecinos cercanos
#
# La codificación de colores se hace en BGR, tal como está especificado en OpenCV
#
# I[:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#

def bayer_interpolacion_vecinos(M):
  I = np.zeros((M.shape[0],M.shape[1],3), dtype=np.uint8)
  #Rojos R
  I[0::2,0::2,2] = M[0::2,0::2]
  I[0::2,1::2,2] = M[0::2,0::2]
  I[1::2,0::2,2] = M[0::2,0::2]
  I[1::2,1::2,2] = M[0::2,0::2]
  #Verdes G
  I[0::2,0::2,1] = M[1::2,0::2]
  I[1::2,1::2,1] = M[1::2,0::2]
  I[1::2,0::2,1] = M[1::2,0::2]
  I[0::2,1::2,1] = M[0::2,1::2]
  #Azules B
  I[0::2,0::2,0] = M[1::2,1::2]
  I[1::2,0::2,0] = M[1::2,1::2]
  I[0::2,1::2,0] = M[1::2,1::2]
  I[1::2,1::2,0] = M[1::2,1::2]
  return I
