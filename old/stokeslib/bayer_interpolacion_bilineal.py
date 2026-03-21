import numpy as np
  
# Interpolación por bilineal
#
# La codificación de colores se hace en BGR, tal como está especificado en OpenCV
#
# I[:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#

def bayer_interpolacion_bilineal(M):
  M = M.astype(np.uint16)
  I = np.zeros((M.shape[0],M.shape[1],3), dtype=np.uint8)
  #Rojos
  I[0::2,0::2,2] = M[0::2,0::2]
  I[0::2,1::2,2][:,:-1] = 0.5*(M[0::2,0::2][:,:-1]+M[0::2,2::2])
  I[1::2,0::2,2][:-1,:] = 0.5*(M[0::2,0::2][:-1,:]+M[2::2,0::2])
  I[1::2,1::2,2][:-1,:-1] = 0.25*(M[0::2,0::2][:-1,:-1]+M[2::2,0::2][:,:-1]+M[0::2,2::2][:-1,:]+M[2::2,2::2])
  #Verdes 
  I[2::2,2::2,1] = 0.25*(M[1::2,2::2][:-1,:]+M[2::2,1::2][:,:-1]+M[3::2,2::2]+M[2::2,3::2])
  I[1::2,1::2,1][:-1,:-1] = 0.25*(M[0::2,1::2][:-1,:-1]+M[1::2,0::2][:-1,:-1]+M[1::2,2::2][:-1,:]+M[2::2,1::2][:,:-1])
  I[1::2,0::2,1] = M[1::2,0::2]
  I[0::2,1::2,1] = M[0::2,1::2]
  #Azules
  I[2::2,2::2,0] = 0.25*(M[1::2,1::2][:-1,:-1]+M[1::2,3::2][:-1,:]+M[3::2,1::2][:,:-1]+M[3::2,3::2])
  I[2::2,1::2,0] = 0.5*(M[1::2,1::2][:-1,:]+M[3::2,1::2])
  I[1::2,2::2,0] = 0.5*(M[1::2,1::2][:,:-1]+M[1::2,3::2])
  I[1::2,1::2,0] = M[1::2,1::2]
  return I
