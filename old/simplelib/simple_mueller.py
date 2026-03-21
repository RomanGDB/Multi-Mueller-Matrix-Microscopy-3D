import sys
import os
import numpy as np
import gzip
import cv2

sys.path.append('../')
from camaralib.guardar_mueller import guardar_mueller
from camaralib.take_mueller import take_mueller
from camaralib.digitalizar import digitalizar
from stokeslib.desacoplar_matriz import desacoplar_matriz

#Directorio de raíz
os.chdir('..')

#Rutas
IMG_LOAD_PATH = 'input/I_input.png'            
IMG_SAVE_PATH = 'mueller/'

# Exposiciona
exposure_time = 5000

# Numero de promedios
N = 1

#Decimador
decimador = 1

#Angulos de polarizacion de entrada
thetas_list = [0,45,90,135,180,225,270,315,360]

#Intensidades de Entrada
I_in = desacoplar_matriz(cv2.imread(IMG_LOAD_PATH))

def main():
    #Nombre
    name = sys.argv[1]  

    #Directorio
    IMG_SAVE_PATH = 'output/mueller/' + name
    if not os.path.exists(IMG_SAVE_PATH): 
        os.makedirs(IMG_SAVE_PATH)

    #Captura matriz de Mueller
    m00, M = take_mueller(I_in, exposure_time, N, thetas_list)

    #Digitaliza intensidad
    m00_dig = digitalizar(m00, 'm00')

    # Guarda imagen de intensidad
    cv2.imwrite(IMG_SAVE_PATH + '/' + 'm00.png', m00_dig)

    #Guardar matriz de Mueller
    guardar_mueller(M, IMG_SAVE_PATH, 'M')

    return True

if __name__ == '__main__':

    if main():
        sys.exit(0)
    else:
        sys.exit(1)
