import numpy as np
import sys

sys.path.append('../')
from camaralib.take_photo import take_photo
from stokeslib.calcular_stokes import calcular_stokes
from stokeslib.polarization_full_dec_array import polarization_full_dec_array


# Dimension sensor
dim = (2048,2448)  

def take_stokes(exposure_time, N):

    # Vector de Stokes
    S = np.zeros((dim[0]//2,dim[1]//2,3,3), dtype=float)
   
    #Toma la foto
    image_data = take_photo(exposure_time, N)
    
    # Decodifica
    I90, I45, I135, I0 = polarization_full_dec_array(image_data)
    
    # Calcula Stokes
    S[:,:,:,0], S[:,:,:,1], S[:,:,:,2] = calcular_stokes(I90, I45, I135, I0)

    return S