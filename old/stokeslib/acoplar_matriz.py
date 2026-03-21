import numpy as np

def acoplar_matriz(M):
    # Número de filas de la matriz M
    filas = M.shape[3]  # M[:,:,:,i,j] -> i va hasta shape[3]
    N = M.shape[4]      # Número de columnas -> shape[4]

    # Crear una lista para almacenar las matrices acopladas horizontalmente
    matrices_acopladas = []

    # Acoplar horizontalmente cada matriz individual
    for i in range(filas):
        matriz_i = M[:,:,:,i,0].copy()
        for j in range(1, N):
            matriz_i = np.append(matriz_i, M[:,:,:,i,j], axis=1)
        matrices_acopladas.append(matriz_i)

    # Acoplar verticalmente todas las matrices acopladas horizontalmente
    M_show = np.concatenate(matrices_acopladas, axis=0)

    return M_show
