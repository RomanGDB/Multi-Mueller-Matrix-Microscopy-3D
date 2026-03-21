import numpy as np

# Nuevo arcotangente entre 0 y 2pi
def arctan3(y,x):
  return np.mod(np.arctan2(y,x),2*np.pi)

#Grado de polarización
def calcular_dolp(S0,S1,S2):
  dolp = np.divide(np.sqrt(np.power(S1.astype(float),2) + np.power(S2.astype(float),2)),S0, out = np.zeros_like(S0.astype(float)), where = S0!= 0) 
  return dolp

#Ángulo de polarización
def calcular_aolp(S1,S2):
  aolp = 0.5*arctan3(S2.astype(float),S1.astype(float))
  return aolp

# Grado de polarización
def calcular_dolp_mueller(M):
  S0 = M[:,:,0,0];   S1 = M[:,:,1,0];   S2 = M[:,:,2,0]
  return calcular_dolp(S0,S1,S2)

# Ángulo de polarización
def calcular_aolp_mueller(M):
  S1 = M[:,:,1,0];   S2 = M[:,:,2,0]
  return calcular_aolp(S1,S2)

# Diatenuación
def calcular_diatenuacion(M):
  D = np.sqrt(M[:,:,0,1]**2+M[:,:,0,2]**2)/M[:,:,0,0]
  return D

# Angulo de diatenuación  
def calcular_aod(M):
  S1 = M[:,:,0,1];   S2 = M[:,:,0,2]
  return calcular_aolp(S1,S2)

# Poder de polarizancia
def power_of_depolarization(M_delta):
  delta = np.ones((1024,1224))-M_delta[:,:,1,1]
  return delta

# Actividad optica
def optical_activity(M_R):
  psi = 1/2 * arctan3(M_R[:,:,2,1]-M_R[:,:,1,2],M_R[:,:,1,1]+M_R[:,:,2,2])
  return psi

# Retardancia lineal
def linear_retardance(M_R):
  delta = np.arccos(np.sqrt((M_R[:,:,1,1]+M_R[:,:,2,2])**2+(M_R[:,:,2,1]-M_R[:,:,1,2])**2)-1)
  return delta
