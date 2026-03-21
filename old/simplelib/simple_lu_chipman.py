import sys
import numpy as np
import cv2
import os
import glob

sys.path.append('../')
from stokeslib.lu_chipman import lu_chipman
from stokeslib.calcular_propiedades import calcular_dolp_mueller, calcular_aolp_mueller, calcular_diatenuacion, calcular_aod, power_of_depolarization, optical_activity, linear_retardance
from camaralib.guardar_img import guardar_img
from camaralib.guardar_mueller import guardar_mueller
from camaralib.png2mueller import png2mueller
from camaralib.digitalizar import digitalizar

IMG_LOAD_PATH = 'C:\\Users\\roman\\Desktop\\LUCHIPMAN\\_mueller\\'
IMG_SAVE_PATH = 'C:\\Users\\roman\\Desktop\\LUCHIPMAN\\'

def extractor(path):

    # Nombre imagen
    name = os.path.splitext(os.path.basename(path))[0]
    print('Extrayendo Datos:', name)

    # Abrir imagen de Mueller en el formato que sea
    M_show = cv2.imread(path, -1)

    # Convertir imagen en Matriz
    M = png2mueller(M_show, 'M16')

    # Lu-Chipman
    lu_name = ['M','MDelta','MR','MD']
    MDelta = np.zeros_like(M)
    MR = np.zeros_like(M)
    MD = np.zeros_like(M)
    m00 = np.zeros_like(M[:,:,:,0,0])
    lu_list = [M, MDelta, MR, MD]

    #Descomposición por canal de color
    for i in range(3):
        MDelta[:,:,i,:,:], MR[:,:,i,:,:], MD[:,:,i,:,:], m00[:,:,i] = lu_chipman(M[:,:,i,:,:])

    #Guarda cada Matriz
    for i, mueller in enumerate(lu_list):
        path = IMG_SAVE_PATH + lu_name[i] + "\\"
        if not os.path.exists(path): 
            os.makedirs(path)
        guardar_mueller(mueller, path, name)
    
    #Color
    color = ['R','G','B']
    
    #Componentes matriciales
    comp_index = [(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    
    for i in range(3):
        for j, comp in enumerate(comp_index):
        
            #Extrae componente
            m = M[:,:,i,comp[0],comp[1]]
            
            #Digitaliza componente
            img = digitalizar(m, 'M8')

            #Guarda imagen
            path = IMG_SAVE_PATH + 'm' + str(comp[0]) + str(comp[1]) + "\\" + color[i] + "\\"
            if not os.path.exists(path): 
                os.makedirs(path)
            cv2.imwrite(path + name + '.png', img)

    #Características físicas
    prop_name = ['DoLP','AoLP','D','AoD','PoD','OA','LR']
    
    for i in range(3):

        #Calcula medida
        dolp = calcular_dolp_mueller(M[:,:,i,:,:])
        aolp = calcular_aolp_mueller(M[:,:,i,:,:])
        D = calcular_diatenuacion(M[:,:,i,:,:])
        aod = calcular_aod(M[:,:,i,:,:])
        delta = power_of_depolarization(MDelta[:,:,i,:,:])
        oa = optical_activity(MR[:,:,i,:,:])
        lr = linear_retardance(MR[:,:,i,:,:])
        prop_list = [dolp, aolp, D, aod, delta, oa, lr]
        
        #Por cada propiedad polarimétrica
        for j, prop in enumerate(prop_list):

            #Digitaliza
            img = digitalizar(prop, prop_name[j])
            
            print(prop_name[j], np.min(prop),np.max(prop),np.mean(prop),np.std(prop),np.min(img),np.max(img))
            
            #Guardar imagen
            path = IMG_SAVE_PATH + prop_name[j] + "\\" + color[i] + "\\"
            if not os.path.exists(path): 
                os.makedirs(path)
            cv2.imwrite(path + name + '.png', img)

    return True
    
def main():

    # Crea lista de imágenes
    img_list = [archivo for archivo in glob.glob(f'{IMG_LOAD_PATH}{"*.png"}')]

    #Extrae características de cada imagen
    for path in img_list:
        extractor(path)


if __name__ == '__main__':

    if main():
        sys.exit(0)
    else:
        sys.exit(1)
