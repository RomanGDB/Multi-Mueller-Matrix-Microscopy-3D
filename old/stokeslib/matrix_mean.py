import numpy as np

def stokes_mean(A):
    M = A.shape[3]
    N = A.shape[4]
    A_mean = np.zeros((M, N))
    A_std = np.zeros((M, N))
    A_mean_show = np.zeros_like(A_mean)
    for i in range(M):
        for j in range(N):
            A_mean[i,j] = np.mean(A[:,:,:,i,j])
            A_std[i,j] = np.std(A[:,:,:,i,j])
    for j in range(N):
        A_mean_show[:,j] = A_mean[:,j]/A_mean[0,j]
    print('Mean: \n', np.round(A_mean_show,2))
    print('')
    print('STD: \n', np.round(A_std,2))
    print('')
    return A_mean

def mueller_mean(A):
    M = A.shape[3]
    N = A.shape[4]
    A_mean = np.zeros((M, N))
    A_std = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            A_mean[i,j] = np.mean(A[:,:,:,i,j])
            A_std[i,j] = np.std(A[:,:,:,i,j])
    print('Mean: \n', np.round(A_mean,2))
    print('')
    print('STD: \n', np.round(A_std,2))
    print('')
    return A_mean