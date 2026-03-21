import os
import sys
import time
import numpy as np
import cv2
import gzip

sys.path.append('../')
from stokeslib.acoplar_mueller import acoplar_mueller
from stokeslib.calcular_propiedades import calcular_diatenuacion
from camaralib.digitalizar import digitalizar
from camaralib.take_mueller import take_mueller
from raspberrylib.ejecutar_comando_ssh import ejecutar_comando_ssh

# Ruta Stokes de entrada
IMG_LOAD_PATH = 'stokes/Sin_inv.npy.gz'    

#Exposicion
exposure_time = 5000

# Numero de promedios
N = 1

# Definir la cantidad de pasos en cada dirección
X_STEPS = 10
Y_STEPS = 10

# Calcular la posición del centro en términos de pasos
centro_x = X_STEPS // 2
centro_y = Y_STEPS // 2

# Definir el rango de índices para las fotos en la grilla
INDICE_INICIAL = 1
INDICE_FINAL = X_STEPS * Y_STEPS

# Definir el tiempo de espera entre movimientos (en segundos)
TIEMPO_ESPERA = 0.5

#Angulos de polarizacion de entrada
thetas_list = [0,30,60,90,120,150]  

#Matrices de estadísticas	
f = gzip.GzipFile(IMG_LOAD_PATH, 'rb')
S_in_stat_inv = np.load(f)          

def mover_motor(motor, direccion, pasos=1):
    for _ in range(pasos):
        print(f"Mover {motor} en direccion ", direccion)
        comando = f"cd /home/mwsi/Desktop/main && python motor_control.py {motor} {direccion}"
        ejecutar_comando_ssh(comando)

def capturar_muestra(X, Y):
    # comienza en centro x, extremo y
    x = 0
    y = -centro_y + 1
    dx = -1
    dy = 0

    # Pide directorio donde guardar las imagenes
    img_sub = input("Ingresa el directorio destino: ")
    IMG_SAVE_PATH = 'img/' + img_sub
    if not os.path.exists(IMG_SAVE_PATH): 
        os.makedirs(IMG_SAVE_PATH)

    for i in range(max(X, Y)**2):
        
        # Si estamos dentro de los límites, capturamos
        if (-X/2 <= x <= X/2) and (-Y/2 <= y <= Y/2):    
            
            #Imprime posición actual
            print (x, y)

            #Calcula Matriz de Mueller
            m00, M = take_mueller(S_in_stat_inv, exposure_time, N, IMG_LOAD_PATH, thetas_list)

            #Salida
            M_dig_color = np.zeros((M.shape[0]*3,M.shape[1]*3,3),dtype=np.uint16)

            for j in range(3):
                #Guarda Mueller img
                M_acoplada = acoplar_mueller(M[:,:,j,:,:])
                
                #Digitaliza Mueller
                M_dig = digitalizar(M_acoplada, 'M16')

                #Arma matriz de mueller en colores
                M_dig_color[:,:,j] = M_dig

            #Digitaliza intensidad
            I_dig = digitalizar(m00, 'm00')

            #Diatenuacion
            D = calcular_diatenuacion(M[:,:,1,:,:])
            print(np.min(D),np.max(D))
            cv2.imwrite(IMG_SAVE_PATH + "/" + str(i).zfill(2) + '_diatenuacion.png', (D*255).astype(np.uint8))

            # Guarda imagen de intensidad
            cv2.imwrite(IMG_SAVE_PATH + "/" + str(i).zfill(2) + '_intensidad.png', I_dig)

            # Guarda Matriz de Mueller
            cv2.imwrite(IMG_SAVE_PATH + "/" + str(i).zfill(2) + '.png', M_dig_color)

        #if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
        if x in [-X/2, X/2]:
            if dy == 0:
                dx, dy = 0, 1
            else:
                dx, dy = -np.sign(x), 0
    
        x, y = x+dx, y+dy
        
        if dx != 0:
            direccion_x = "F" if dx > 0 else "B"
            mover_motor('X',"F" if dx > 0 else "B")
            
        if dy != 0:
            direccion_y = "F" if dy > 0 else "B"
            mover_motor('Y',direccion_y)
            
    # volver a posicion inicial
    print('Volviendo a posición inicial...')
    mover_motor('Y', 'B', Y_STEPS)
    mover_motor('X', 'B', X_STEPS//2)

def main():

    #Captura muestra, calcula tiempo
    tic = time.time()
    capturar_muestra(X_STEPS, Y_STEPS)        
    toc = time.time()

    print("Muestra completa capturada en "+str(int((toc-tic)//60))+" minutos y "+str(int((toc-tic) % 60))+' segundos.')

    return True

if __name__ == '__main__':

    if main():
        sys.exit(0)
    else:
        sys.exit(1)
