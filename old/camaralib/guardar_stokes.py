import cv2
import sys

sys.path.append('../')
from camaralib.digitalizar import digitalizar
from camaralib.guardar_img import guardar_img

#Colores R G B
color = ['650', '550', '450']

def guardar_stokes(S, path, name):

    #Digitaliza S0
    S0_norm = digitalizar(S[:,:,:,0], 'S0')

    #Color S0
    S0_RGB = cv2.cvtColor(S0_norm, cv2.COLOR_BGR2RGB)

    #Guarda imagen en color
    guardar_img(path, S0_RGB, name + ' S0')

    #S0 en grises con colorbar
    for i in range(3):

        #Colormap canal
        im = cv2.cvtColor(cv2.applyColorMap(S0_RGB[:,:,i], cv2.COLORMAP_BONE), cv2.COLOR_BGR2RGB)

        #Guarda imagen
        guardar_img(path, im, name + ' S0 ('+color[i]+' nm)', color = 'red', clim=[0,2])

    #S1 y S2 en grises con colorbar
    for i in range(3):
        for j in range(1,3):
            
            #Digitaliza S1 o S2
            S_norm = digitalizar(S[:,:,i,j], 'S1')

            #Colormap
            im = cv2.cvtColor(cv2.applyColorMap(S_norm, cv2.COLORMAP_BONE), cv2.COLOR_BGR2RGB)
            guardar_img(path, im, name + ' S' + str(j) + ' ('+color[i]+' nm)', color = 'red', clim=[-1,1])

    return True    
