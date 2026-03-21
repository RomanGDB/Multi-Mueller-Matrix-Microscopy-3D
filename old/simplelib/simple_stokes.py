import sys
import numpy as np
import gzip
import os
import cv2

sys.path.append('../')
from camaralib.take_mueller_stokes import take_mueller_stokes
from camaralib.guardar_stokes import guardar_stokes
from camaralib.digitalizar import digitalizar
from stokeslib.acoplar_matriz import acoplar_matriz

#Directorio Raíz
os.chdir('..')

# Ruta carpeta en dónde guardar
IMG_SAVE_PATH = 'output/stokes/'  

if not os.path.exists(IMG_SAVE_PATH): 
    os.makedirs(IMG_SAVE_PATH)

# Exposicion
exposure_time = 5000

# Numero de promedios
N = 1

#Decimador 
decimador = 1

#Angulos de polarizacion de entrada
#thetas_list = [0,30,60,90,120,150]
thetas_list = [0,60,120]  

def main():
    #Nombre
    name = sys.argv[1]  

    #Toma vectores de Stokes
    S_in_stat = take_mueller_stokes(exposure_time, N, thetas_list)

    #Guarda numpy stokes comprimido
    print("Guardando imagen...")
    S_in_stat_img = acoplar_matriz(digitalizar(S_in_stat, 'S1'))
    cv2.imwrite(IMG_SAVE_PATH + 'S_' + name + '.png', S_in_stat_img)
    
    if name == 'in':
        print("Guardando array invertido...")
        f = gzip.GzipFile(IMG_SAVE_PATH + 'Sin_inv.npy.gz', 'wb')
        np.save(f, np.linalg.pinv(S_in_stat))

    return True

if __name__ == '__main__':

    if main():
        sys.exit(0)
    else:
        sys.exit(1)
