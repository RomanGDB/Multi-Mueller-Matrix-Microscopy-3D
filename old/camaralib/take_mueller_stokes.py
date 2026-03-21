import numpy as np
import sys

sys.path.append('../')
from camaralib.take_stokes import take_stokes
from raspberrylib.ejecutar_comando_ssh import ejecutar_comando_ssh

# Dimension sensor
dim = (2048,2448)  

#Decimador 
decimador = 1

#Captura el vector de Stokes variando el ángulo de entrada
def take_mueller_stokes(exposure_time, N, thetas_list):

    #Numero de angulos    
    N_datos = len(thetas_list)

    #Matrices de estadísticas
    S_stat = np.zeros((dim[0]//2,dim[1]//2,3,3,N_datos), dtype=float)[::decimador,::decimador]
    
    for i, theta in enumerate(thetas_list):
        # Toma una captura de Stokes
        print("Tomando Stokes...") 
        S = take_stokes(exposure_time, N)
    
        #Almacena Stokes        
        for j in range(3):
            S_stat[:,:,:,j,i] = S[:,:,:,j] 

        # Mientras no sea el ultimo
        if theta != thetas_list[-1]:
            #Mueve el motor
            print("Moviendo T en direccion F...")
            comando = f"cd /home/mwsi/Desktop/main && python motor_control.py T F"
            ejecutar_comando_ssh(comando)

    # Volver a posicion original
    for _ in range(len(thetas_list)-1):
        print("Moviendo T en direccion B...")
        comando = f"cd /home/mwsi/Desktop/main && python motor_control.py T B"
        ejecutar_comando_ssh(comando)

    return S_stat