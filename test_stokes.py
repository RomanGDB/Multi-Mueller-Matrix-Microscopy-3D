import sys
import numpy as np
import cv2
from simple_pyspin import Camera

# Calcular Stokes
def calcular_stokes (I90, I45, I135, I0, A = None, decimador = 1):

  #Decimador
  I0 = I0[::decimador,::decimador]
  I45 = I45[::decimador,::decimador]
  I90 = I90[::decimador,::decimador]
  I135 = I135[::decimador,::decimador]
  
  #Modo sin calibración
  if A == None:

    #Calculo
    S0 = I0.astype(np.int16)+I90.astype(np.int16)
    S1 = I0.astype(np.int16)-I90.astype(np.int16)
    S2 = I45.astype(np.int16)-I135.astype(np.int16)

  #Modo calibrado  
  else:

    #Decimador
    A = A[::decimador,::decimador]
    A = A[::decimador,::decimador]
    A = A[::decimador,::decimador]
    A = A[::decimador,::decimador]
    
    #Calculo
    S0 = A[:,:,:,0,0]*I0.astype(float)+A[:,:,:,0,1]*I45.astype(float)+A[:,:,:,0,2]*I90.astype(float)+A[:,:,:,0,3]*I135.astype(float)
    S1 = A[:,:,:,1,0]*I0.astype(float)+A[:,:,:,1,1]*I45.astype(float)+A[:,:,:,1,2]*I90.astype(float)+A[:,:,:,1,3]*I135.astype(float)
    S2 = A[:,:,:,2,0]*I0.astype(float)+A[:,:,:,2,1]*I45.astype(float)+A[:,:,:,2,2]*I90.astype(float)+A[:,:,:,2,3]*I135.astype(float)
  
  return S0, S1, S2

def bayer_interpolacion_vecinos(M):
    I = np.zeros((M.shape[0], M.shape[1], 3), dtype=np.uint16)

    I[0::2,0::2,2] = M[0::2,0::2]
    I[0::2,1::2,2] = M[0::2,0::2]
    I[1::2,0::2,2] = M[0::2,0::2]
    I[1::2,1::2,2] = M[0::2,0::2]

    I[0::2,0::2,1] = M[1::2,0::2]
    I[1::2,1::2,1] = M[1::2,0::2]
    I[1::2,0::2,1] = M[1::2,0::2]
    I[0::2,1::2,1] = M[0::2,1::2]

    I[0::2,0::2,0] = M[1::2,1::2]
    I[1::2,0::2,0] = M[1::2,1::2]
    I[0::2,1::2,0] = M[1::2,1::2]
    I[1::2,1::2,0] = M[1::2,1::2]

    return I

def polarization_full_dec_array(A):
    I0   = bayer_interpolacion_vecinos(A[1::2,1::2])
    I45  = bayer_interpolacion_vecinos(A[0::2,1::2])
    I90  = bayer_interpolacion_vecinos(A[0::2,0::2])
    I135 = bayer_interpolacion_vecinos(A[1::2,0::2])
    return I90, I45, I135, I0

# Configuración de la exposición
exposure_time = 5000

# Número máximo de puntos a mostrar
MAX_POINTS = 200

# Dimensiones de la ventana de la gráfica
width, height = 400, 300  # Ancho y alto de la ventana
center_x, center_y = width // 2, height // 2  # Centro de la ventana

# Colores
background_color = (255, 255, 255)  # Blanco
axis_color = (0, 0, 0)  # Negro
curve_color_1 = (255, 0, 0)  # Azul para S1/S0
curve_color_2 = (0, 255, 0)  # Verde para S2/S0
curve_color_3 = (255, 0, 255)  # Morado para S3/S0
text_color = (0, 0, 0)  # Negro

# Función para escalar valores
def scale(value, max_value, half_range):
    return int((value / max_value) * half_range)

def draw_axes(canvas):
    """Dibuja los ejes cartesianos y la numeración."""
    # Ejes
    cv2.line(canvas, (0, center_y), (width, center_y), axis_color, 1)  # Eje X
    cv2.line(canvas, (center_x, 0), (center_x, height), axis_color, 1)  # Eje Y

    # Etiquetas y ticks del eje Y
    for i in range(-5, 6):  # Rango de -1 a 1 en pasos de 0.2
        if i != 0:
            y_pos = center_y - scale(i / 5, 1, height // 2)
            cv2.line(canvas, (center_x - 5, y_pos), (center_x + 5, y_pos), axis_color, 1)  # Tick
            cv2.putText(canvas, f"{i / 5:.1f}", (center_x + 10, y_pos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)

    # Etiquetas y ticks del eje X
    for i in range(-5, 6):  # Rango de -1 a 1 en pasos de 0.2
        if i != 0:
            x_pos = center_x - scale(i / 5, 1, width // 2)
            cv2.line(canvas, (x_pos, center_y - 5), (x_pos, center_y + 5), axis_color, 1)  # Tick
            #cv2.putText(canvas, f"{i / 5:.1f}", (x_pos + 5, center_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)
            
def draw_legend(canvas):
    """Dibuja la leyenda para las curvas."""
    cv2.putText(canvas, "S1", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, curve_color_1, 2)  # Rojo
    cv2.putText(canvas, "S2", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, curve_color_2, 2)  # Verde
    cv2.putText(canvas, "S3", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, curve_color_3, 2)  # Morado

def main():

    # Almacenar valores
    values_1 = []
    values_2 = []

    # Continúa actualizando
    update = True
    
    # Almacena Stokes
    S = np.zeros((1,1,1,3,1))

    with Camera() as cam:  # Inicializar cámara
        cam.ExposureAuto = 'Off'
        cam.ExposureTime = exposure_time  # Configurar exposición

        cam.start()  # Comenzar captura

        while update:
            # Capturar imagen
            img = cam.get_array()

            # Calcular Stokes
            I90, I45, I135, I0 = polarization_full_dec_array(img)
            S0, S1, S2 = calcular_stokes(I90, I45, I135, I0)
            S[:,:,:,0,0], S[:,:,:,1,0], S[:,:,:,2,0] = S0[0,0,0], S1[0,0,0], S2[0,0,0]
            
            # Normalizar valores
            if S[0,0,0,0,0] != 0:
                value_1 = S[0,0,0,1,0] / S[0,0,0,0,0]
                value_2 = S[0,0,0,2,0] / S[0,0,0,0,0]
            else:
                value_1, value_2 = 0, 0

            # Imprimir Stokes 
            print(f"[ {int(S[0,0,0,0,0])} , {value_1:.2f} , {value_2:.2f}, AoP = {0.5*np.rad2deg(np.arctan2(value_2, value_1)):.1f}]")

            # Almacenar las nuevas medidas
            values_1.append(value_1)
            values_2.append(value_2)

            # Mantener el batch de medidas recientes
            if len(values_1) > MAX_POINTS:
                values_1.pop(0)
                values_2.pop(0)

            # Crear lienzo de fondo
            canvas = np.full((height, width, 3), background_color, dtype=np.uint8)

            # Dibujar ejes y leyenda
            draw_axes(canvas)
            draw_legend(canvas)

            # Dibujar ejes cartesianos
            cv2.line(canvas, (0, center_y), (width, center_y), axis_color, 1)  # Eje X
            cv2.line(canvas, (center_x, 0), (center_x, height), axis_color, 1)  # Eje Y

            # Dibujar las curvas desplazadas
            for i in range(1, len(values_1)):
                x1 = int(1.5 * center_x) + i - len(values_1)  # Posición X desplazada
                y1_1 = center_y - scale(values_1[i - 1], 1, height // 2)
                y2_1 = center_y - scale(values_2[i - 1], 1, height // 2)

                x2 = int(1.5 * center_x) + i + 1 - len(values_1)
                y1_2 = center_y - scale(values_1[i], 1, height // 2)
                y2_2 = center_y - scale(values_2[i], 1, height // 2)

                # Dibujar líneas para las curvas
                cv2.line(canvas, (x1, y1_1), (x2, y1_2), curve_color_1, 2)  # Curva roja (S1/S0)
                cv2.line(canvas, (x1, y2_1), (x2, y2_2), curve_color_2, 2)  # Curva verde (S2/S0)

            # Mostrar la ventana
            cv2.imshow("Curvas centradas y desplazadas", canvas)

            # Manejar teclado para salir
            key = cv2.waitKey(1)
            if key == ord('q'):
                update = False

        cam.stop()  # Detener captura

    return True

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
