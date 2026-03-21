from stokeslib.bayer_interpolacion_vecinos import bayer_interpolacion_vecinos
from stokeslib.bayer_interpolacion_bilineal import bayer_interpolacion_bilineal

# Decodificación completa de la cámara polarizada
#
# Por defecto se utiliza la interpolación por vecinos cercanos
# Devuelve el vector de observables I = (I90, I45, I135, I0) en codificación de color BGR
#
# I90[:,:,:], I45[:,:,:], I135[:,:,:], I0[:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#

def polarization_full_dec_array(A, interpolacion = 'vecinos'):

  if interpolacion == 'vecinos':

    # Interpolación vecinos y descomposición de Bayer
    I0 = bayer_interpolacion_vecinos(A[1::2,1::2])
    I45 = bayer_interpolacion_vecinos(A[0::2,1::2])
    I90 = bayer_interpolacion_vecinos(A[0::2,0::2])
    I135 = bayer_interpolacion_vecinos(A[1::2,0::2])

  elif interpolacion == 'bilineal':

    # Interpolación vecinos y descomposición de Bayer
    I0 = bayer_interpolacion_bilineal(A[1::2,1::2])
    I45 = bayer_interpolacion_bilineal(A[0::2,1::2])
    I90 = bayer_interpolacion_bilineal(A[0::2,0::2])
    I135 = bayer_interpolacion_bilineal(A[1::2,0::2])
    
  return I90, I45, I135, I0