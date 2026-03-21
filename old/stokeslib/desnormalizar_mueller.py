import numpy as np
from camaralib.analogizar import analogizar
from camaralib.digitalizar import digitalizar
# Desnormaliza matriz de mueller M

def desnormalizar(M, m00):

  #Máscara
  mask_ = np.append(m00,np.append(m00,m00,axis=0), axis=0)
  mask = np.append(mask_, np.append(mask_, mask_, axis=1), axis=1)

  #Analogizar medidas
  M_norm = analogizar(M, 'M16')
  mask_norm = analogizar(mask, 'm00')

  #Normalizar Mueller
  M = M_norm*mask_norm

  #Digitalizar Mueller
  M_show = digitalizar(M, 'M16')

  return M_show
