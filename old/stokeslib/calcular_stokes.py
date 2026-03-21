import numpy as np

# Calcula los parámetros de Stokes
#
# Toma como entrada en vector de observables I = (I90, I45, I135, I0),
# la matriz de instrumentación A (S = AI) y la bandera calibrar (si o no)
# Devuelve el vector de Stokes S = (S0, S1, S2) calibrado o no
#
# A[:,:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#               Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)
#
# S0[:,:,:],S1[:,:,:],S2[:,:,:]: 
#                                 Primera componente: Dimensión vertical pixeles [0, dimy]
#                                 Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                                 Tercera componente: Canales de colores Blue (B), Green (G) y Red (R) 
#
def calcular_stokes (I90, I45, I135, I0, A = None, decimador = 1):

  #Decimador
  I0 = I0[::decimador,::decimador]
  I45 = I45[::decimador,::decimador]
  I90 = I90[::decimador,::decimador]
  I135 = I135[::decimador,::decimador]
  
  #Modo sin calibración
  if A == None:

    #Calculo
    S0 = I0.astype(np.int16)+I90.astype(np.int16)
    S1 = I0.astype(np.int16)-I90.astype(np.int16)
    S2 = I45.astype(np.int16)-I135.astype(np.int16)

  #Modo calibrado  
  else:

    #Decimador
    A = A[::decimador,::decimador]
    A = A[::decimador,::decimador]
    A = A[::decimador,::decimador]
    A = A[::decimador,::decimador]
    
    #Calculo
    S0 = A[:,:,:,0,0]*I0.astype(float)+A[:,:,:,0,1]*I45.astype(float)+A[:,:,:,0,2]*I90.astype(float)+A[:,:,:,0,3]*I135.astype(float)
    S1 = A[:,:,:,1,0]*I0.astype(float)+A[:,:,:,1,1]*I45.astype(float)+A[:,:,:,1,2]*I90.astype(float)+A[:,:,:,1,3]*I135.astype(float)
    S2 = A[:,:,:,2,0]*I0.astype(float)+A[:,:,:,2,1]*I45.astype(float)+A[:,:,:,2,2]*I90.astype(float)+A[:,:,:,2,3]*I135.astype(float)
  
  return S0, S1, S2
