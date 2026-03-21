import numpy as np

# Calcula la descomposición de Lu-Chipman de una matriz de Mueller
# Recibe como entrada una matriz de Mueller M no singular (det(M) != 0 para todo pixel (x,y))
# y devuelve tres matrices de mueller (MDelta, MR, MD) y la componente m00
# MDelta: Matriz de depolarizancia 
# MR: Matriz de retardancia
# MD: Matriz de diatenuación
#
# M[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)
#
# MR[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)
#
# MD[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)
#
# MDelta[:,:,:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#                Cuarta componente: Dimensión vertical de la matriz (0,1,2)
#                Quinta componente: Dimensión horizontal de la matriz (0,1,2)
#
# m00[:,:]: 
#               Primera componente: Dimensión vertical pixeles [0, dimy]
#               Segunda componente: Dimensión horizonal pixeles [0, dimx]
#

def lu_chipman(M):
  #Identidades
  I2 = np.stack([np.stack([np.identity(2)]*M.shape[1])]*M.shape[0])
  I3 = np.stack([np.stack([np.identity(3)]*M.shape[1])]*M.shape[0])

  #Normalización
  M_norm = M.copy()
  for i in range(3):
    for j in range(3):
      M_norm[:,:,i,j] = M[:,:,i,j]/M[:,:,0,0]
  
  #M Diatenuación
  MD = np.ones_like(M)
  D = M_norm[:,:,0,1:]
  D2 = np.einsum('ijk,ijk->ij',D, D)
  a = np.sqrt(1-D2,out=np.zeros_like(D2),where=D2<=1)
  b = np.divide(1-a,D2,out=np.zeros_like(D2),where=D2!=0)
  MD[:,:,0,1:] = D
  MD[:,:,1:,0] = D
  for i in range(2):
    for j in range(2):
      MD[:,:,1+i,1+j] = a*I2[:,:,i,j] + b*np.einsum('ijk,ijl->ijkl',D,D)[:,:,i,j]

  #M Prima
  Mprima = np.einsum('ijkl,ijlm->ijkm',M_norm[:,:,:,:],np.linalg.pinv(MD))
  mprima = Mprima[:,:,1:,1:]

  #M Delta
  mdr = np.einsum('ijkl,ijlm->ijkm',mprima,mprima.transpose(0,1,3,2))
  L , V = np.linalg.eig(mdr)

  #Depolarizancia
  delta = np.sqrt(np.abs(L[:,:,0])) * (L[:,:,0] >= L[:,:,1]) + np.sqrt(np.abs(L[:,:,1])) * (L[:,:,0] < L[:,:,1])
  MDelta = np.zeros_like(M)
  MDelta[:,:,0,0] = np.ones(M[:,:,0,0].shape)
  MDelta[:,:,1,1] = delta
  MDelta[:,:,2,2] = delta

  #Polarizancia:
  PDelta = np.zeros((M.shape[0],M.shape[1],2))
  for i in range(2):
    PDelta[:,:,i] = (M_norm[:,:,1+i,0] - np.einsum('ijkl,ijl->ijk',M_norm[:,:,1:,1:],D)[:,:,i])/(1-D2)
  MDelta[:,:,1:,0] = PDelta
  
  #M Retardancia
  MR = np.einsum('ijkl,ijlm->ijkm', np.linalg.pinv(MDelta), Mprima)

  return MDelta, MR, MD, M[:,:,0,0]
