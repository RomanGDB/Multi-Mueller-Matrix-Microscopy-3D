# Normaliza matriz de mueller M

def normalizar_mueller(M):

  M_norm = M.copy()
  for i in range(3):
    for j in range(3):
      for k in range(3):
        M_norm[:,:,k,i,j] = M_norm[:,:,k,i,j]/M[:,:,k,0,0]

  return M[:,:,k,0,0], M_norm
