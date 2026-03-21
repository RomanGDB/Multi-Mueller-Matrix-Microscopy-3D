import numpy as np

# Calcula la matriz de instrumentación A (S = AI) del sistema 
#
# Toma como entrada una estadística de parámetros de Stokes (S_stat) y observables (I_stat)
# Devuelve la matriz de instrumentaición A
#
# S[:,:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#                Cuarta componente: Dimensión vertical del vector (S0, S1, S2)
#                Quinta componente: Dimensión horizontal de estadísticas (dato1, dato2, ... datoN)
#
# I[:,:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#                Cuarta componente: Dimensión vertical del vector (I90, I45, I135, I0)
#                Quinta componente: Dimensión horizontal de estadísticas (dato1, dato2, ... datoN)
#
# A[:,:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)

def calcular_instrumentacion(I_stat,S_stat):
  A = np.einsum('ijklm,ijkmn->ijkln',S_stat,np.linalg.pinv(I_stat))
  return A     
