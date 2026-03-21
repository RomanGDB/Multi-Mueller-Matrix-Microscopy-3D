import numpy as np

# Devuelve la matriz de Mueller 4x4 del polarizador lineal con transmitancia T, tasa de extinción e y 
# ángulo de polarización theta_d (en grados)
def mueller_polarizador(T,D,theta_d):
  theta_d = theta_d*np.pi/180 #Radianes
  MR = np.array([[1,0,0,0],[0,np.cos(2*theta_d),np.sin(2*theta_d),0],[0,-np.sin(2*theta_d),np.cos(2*theta_d),0],[0,0,0,1]])
  M = MR.T @ np.array([[1,D,0,0],[D,1,0,0],[0,0,np.sqrt(1-D**2),0],[0,0,0,np.sqrt(1-D**2)]]) @ MR
  return M

# Devuelve la matriz de Mueller 4x4 del retardador lineal con birrefringencia phi (en grados) y 
# ángulo de rotación theta (en grados)
def mueller_retardador(phi,theta):
  theta = theta*np.pi/180   #Radianes
  phi = phi*np.pi/180       #Radianes
  MR = np.array([[1,0,0,0],[0,np.cos(2*theta),np.sin(2*theta),0],[0,-np.sin(2*theta),np.cos(2*theta),0],[0,0,0,1]])
  M =  MR.T @ np.array([[1,0,0,0],[0,1,0,0],[0,0,np.cos(phi),np.sin(phi)],[0,0,-np.sin(phi),np.cos(phi)]]) @ MR
  return M

# Devuelve la matriz de Mueller 4x4 del rotador con ángulo de rotación theta (en grados)
def mueller_rotador(theta):
  theta = theta*np.pi/180 #Radianes
  M = np.array([[1,0,0,0],[0,np.cos(2*theta),-np.sin(2*theta),0],[0,np.sin(2*theta),np.cos(2*theta),0],[0,0,0,1]])
  return M
