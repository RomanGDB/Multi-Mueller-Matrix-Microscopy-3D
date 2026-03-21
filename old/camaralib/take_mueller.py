from camaralib.take_intensities import take_intensities 
from stokeslib.calcular_mueller_inv import calcular_mueller_inv
from stokeslib.normalizar_mueller import normalizar_mueller
from stokeslib.calcular_stokes import calcular_stokes
from stokeslib.calcular_s3 import calcular_s3
from stokeslib.matrix_mean import mueller_mean, stokes_mean
import numpy as np

#Calcula la matriz de Mueller. Sincroniza con los motores, toma las fotos, 
# carga la Sin invertida y entrega la matriz de mueller observada.

def take_mueller(I_in, exposure_time, N, thetas_list):

    # Dimension
    dim = (1024,1224)

    #Configuración del sistema
    DoP = 1
    beta = 45
    gamma = 1.44

    # Número de datos
    N_datos = len(thetas_list)

    # Matrices de Stokes
    S_in = np.zeros((dim[0],dim[1],3,4,N_datos))
    S_in_inv = np.zeros((dim[0],dim[1],3,N_datos,3)) #no sirve
    S_out = np.zeros((dim[0],dim[1],3,3,N_datos))

    print('Calculando Matrices de Stokes...')

    # Entrada
    S_in[:,:,:,0,:], S_in[:,:,:,1,:], S_in[:,:,:,2,:] = calcular_stokes(I_in[:,:,:,2,:], I_in[:,:,:,1,:], I_in[:,:,:,3,:], I_in[:,:,:,0,:])
    S_in = calcular_s3(S_in, DoP, gamma, thetas_list, beta)

    #Mide de intensidades de salida
    I_out = take_intensities(exposure_time, N, thetas_list)

    # Salida
    S_out[:,:,:,0,:], S_out[:,:,:,1,:], S_out[:,:,:,2,:] = calcular_stokes(I_out[:,:,:,2,:], I_out[:,:,:,1,:], I_out[:,:,:,3,:], I_out[:,:,:,0,:])

    # Stokes invertida media
    S_in_mean = stokes_mean(S_in)
    S_in_mean_inv = np.linalg.pinv(S_in_mean)

    # Numero de Condición
    print('Condición del Sistema:', np.linalg.cond(S_in_mean))
    
    S_in_inv = S_in_mean_inv[np.newaxis, np.newaxis, np.newaxis, :, :]

    #Calcula Mueller
    print('Calculando Matriz de Mueller...')

    #Calculo de Mueller
    M = calcular_mueller_inv(S_in_inv, S_out)
    m00, M_norm = normalizar_mueller(M)
    _ = mueller_mean(M_norm)

    return m00, M_norm
