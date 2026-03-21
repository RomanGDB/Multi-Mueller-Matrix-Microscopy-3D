import numpy as np

#Definiciones
MAX8 = 2**8-1
MAX16 = 2**16-1

#Digitalizadora de medidas físicas

def digitalizar(A, medida):

    #Intensidad
    if medida == 'S0':
        A_digital = (A // 2).astype(np.uint8)

    #Polarización
    elif (medida == 'S1') or (medida == 'S2'):
        A_digital = ((A + MAX8) // 2).astype(np.uint8)

    #Medida entre 0 y 1
    elif (medida == 'DoLP') or (medida == 'D') or (medida == 'PoD'):
        A_digital = A*MAX8
        A_digital[A_digital > MAX8] = MAX8
        A_digital[A_digital < 0] = 0
        A_digital = np.round(A_digital).astype(np.uint8)

    #Ángulo entre 0 y pi
    elif (medida == 'AoLP') or (medida == 'AoD') or (medida == 'OA') or (medida == 'LR'):
        A_digital = A/np.pi*MAX8
        A_digital[A_digital > MAX8] = MAX8
        A_digital[A_digital < 0] = 0
        A_digital = np.round(A_digital).astype(np.uint8)

    #Mueller en 8 bits
    elif medida == 'M8':
        A_digital = ((A + 1)/2 * MAX8)
        A_digital[A_digital > MAX8] = MAX8
        A_digital[A_digital < 0] = 0
        A_digital = np.round(A_digital).astype(np.uint8)
    
    #Mueller en 16 bits
    elif medida == 'M16':
        A_digital = ((A + 1)/2 * MAX16)
        A_digital[A_digital > MAX16] = MAX16
        A_digital[A_digital < 0] = 0
        A_digital = np.round(A_digital).astype(np.uint16)

    #Componentes Mueller
    elif medida == 'm00':
        A_digital = A/np.max(A) * MAX16
        A_digital = np.round(A_digital).astype(np.uint16)    
        
    #Cualquier otro caso:
    else:
        A_digital = A

    return A_digital
