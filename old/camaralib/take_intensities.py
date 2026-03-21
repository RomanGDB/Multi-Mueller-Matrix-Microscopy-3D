import numpy as np
import sys

sys.path.append('../')
from camaralib.take_photo import take_photo
from stokeslib.polarization_full_dec_array import polarization_full_dec_array
from raspberrylib.rpi_connection import RPiController

# Conectar Raspberry Pi
rpi = RPiController()
rpi.conectar()

# Dimension sensor
dim = (2048,2448)  

# Decimador 
decimador = 1

# Captura el vector de Stokes variando el ángulo de entrada
def take_intensities(exposure_time, N, thetas_list):

    # Numero de angulos y angle backward
    N_datos = len(thetas_list)
    angle_backward = str(thetas_list[-1])
    print('Angulos: ', thetas_list)

    # Matrices de estadísticas
    I_stat = np.zeros((dim[0]//2,dim[1]//2,3,4,N_datos), dtype=np.uint8)[::decimador,::decimador]
    
    for i, theta in enumerate(thetas_list):

        # Angle forward
        if (theta != thetas_list[-1]):
            angle_forward = str(thetas_list[i+1] - thetas_list[i])

        # Toma una captura de intensidades
        print(f"Tomando Intensidades para ángulo de medida {theta}º") 

        # Toma la foto
        image_data = take_photo(exposure_time, N)
    
        # Decodifica
        I90, I45, I135, I0 = polarization_full_dec_array(image_data)

        # Vector de intensidades
        I_list = [I0, I45, I90, I135]
    
        # Almacena intensidades        
        for j in range(4):
            I_stat[:,:,:,j,i] = I_list[j]

        # Mientras no sea el ultimo
        if (theta != thetas_list[-1]):
            # Mueve el motor
            print(f"Moviendo T unos {angle_forward}º en direccion F ...")
            comando = 'T F ' + angle_forward
            rpi.ejecutar("python3 /home/mwsi/Desktop/main/motor_control.py " + comando)

    # Volver a posicion original
    print(f"Moviendo T unos {angle_backward}º en direccion B ...")
    comando = 'T B ' + angle_backward
    rpi.ejecutar("python3 /home/mwsi/Desktop/main/motor_control.py " + comando)

    # Desconectar Raspberry Pi
    rpi.desconectar()

    return I_stat