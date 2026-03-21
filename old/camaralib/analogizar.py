import numpy as np

#Definiciones
MAX8 = 2**8-1
MAX16 = 2**16-1

#Analogizadora de medidas digitales

def analogizar(A, medida):

    #Evitar Overlfow
    A = A.astype(float)

    #Intensidad
    if medida == 'S0':
        A_analogo = (2*A).astype(np.uint16)

    #Polarización
    elif (medida == 'S1') or (medida == 'S2'):
        A_analogo = (2*A - MAX8).astype(np.uint16)

    #Medida entre 0 y 1
    elif (medida == 'DoLP') or (medida == 'D') or (medida == 'PoD'):
        A_analogo = A/MAX8

    #Ángulo entre 0 y pi
    elif (medida == 'AoLP') or (medida == 'AoD') or (medida == 'OA') or (medida == 'LR'):
        A_analogo = MAX8/np.pi*A-np.pi/2

    #Mueller en 8 bits
    elif medida == 'M8':
        A_analogo = 2/MAX8*A - 1
    
    #Mueller en 16 bits
    elif medida == 'M16':
        A_analogo = 2/MAX16*A - 1

    #Componentes Mueller
    elif medida == 'm00':
        A_analogo = A/MAX16

    return A_analogo
