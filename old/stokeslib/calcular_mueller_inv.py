import numpy as np

# Calcula matriz de Mueller en tres canales
# Recibe como entrada los vectores de stokes de entrada invertidos (Sin_inv) y los vectores de Stokes de salida (Sout)
# en codificación de colores BGR 
# Devuelve la matriz de Mueller M del sistema 
#
# S_out_stat[:,:,:,:,:]:
#                       Primera componente: Dimensión vertical pixeles [0, dimy]
#                       Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                       Tercer componente:  Canales de colores Blue (B), Green (G) y Red (R) 
#                       Cuarta componente:  Componente del vector (S0,S1,S2) 
#                       Quinta componente:  Datos (1,...,N) (entradas)
#
# S_in_stat_inv[:,:,:,:,:]:
#                       Primera componente: Dimensión vertical pixeles [0, dimy]
#                       Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                       Tercer componente:  Canales de colores Blue (B), Green (G) y Red (R) 
#                       Cuarta componente:   
#                       Quinta componente:  
#
# M[:,:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)

def calcular_mueller_inv(S_in_inv,S_out):
  M = np.einsum('ijklm,ijkmn->ijkln', S_out, S_in_inv)
  return M
