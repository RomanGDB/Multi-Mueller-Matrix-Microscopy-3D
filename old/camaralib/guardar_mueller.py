import numpy as np
import cv2
from camaralib.digitalizar import digitalizar
from camaralib.guardar_img import guardar_img
from stokeslib.acoplar_matriz import acoplar_matriz

#Codigo de color
codigo=['R','G','B']

def guardar_mueller(M, path, name):

    #Mueller RGB
    M_RGB16 = np.zeros((M.shape[0]*M.shape[3], M.shape[1]*M.shape[4], 3), dtype = np.uint16)

    #Acoplar en una imagen la Matriz de Mueller en el canal
    M_acoplada = acoplar_matriz(M)
    
    for i in range(3):
            
        #Normalizar Mueller en 8 y 16 bits
        M_norm8 = digitalizar(M_acoplada[:,:,i], 'M8')
        M_RGB16[:,:,i] = digitalizar(M_acoplada[:,:,i], 'M8')

        #Colormap
        im = cv2.cvtColor(cv2.applyColorMap(M_norm8, cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
            
        #Guardar
        guardar_img(path, im, name + '_' + codigo[i], cmap = 'jet', clim = [-1,1])
    
    #Guardar Mueller color
    cv2.imwrite(path + '/' + name + '.jpg', M_RGB16)

    return True