import sys
import os
import numpy as np
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QLibraryInfo
from simple_pyspin import Camera
import cv2
from datetime import datetime
from opto import Opto

sys.path.append('../')
from stokeslib.polarization_full_dec_array import polarization_full_dec_array
from stokeslib.calcular_stokes import calcular_stokes
from camaralib.digitalizar import digitalizar
from camaralib.runcmd import runcmd
from raspberrylib.rpi_connection import RPiController
from stokeslib.calcular_propiedades import calcular_dolp, calcular_aolp

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

#Threading motores
class thread_motor(Thread):
    def __init__(self, motor, movimiento):
        super(thread_motor, self).__init__()
        self.motor = motor
        self.movimiento = movimiento
    def run(self):
        comando = self.motor + ' ' + self.movimiento + ' ' + '45'
        rpi.ejecutar("python3 /home/mwsi/Desktop/main/motor_control.py " + comando)

#Threading lente
class thread_lens(Thread):
    def __init__(self, o, current_value):
        super(thread_lens, self).__init__()
        self.current_value = current_value
        self.o = o
    def run(self):
        self.o.current(self.current_value)

# Configuración inicial cámara
exposure_time = 5000
interpolador = 'vecinos'
N = 1

# Configuración inicial OptoTune
current_value = 25.0
current_step = 2.5
max_current = 100 - current_step
min_current = current_step

#Decimador imagen
decimador = 4

# Contador 
counter = 1000

class Ui(QMainWindow):
    def __init__(self, rpi, cam):
        super(Ui, self).__init__()

        #Objeto Raspberry Pi
        self.rpi = rpi

        #Objeto cámara
        self.cam = cam
        
        # Contador
        self.counter = counter

        # Carga GUI diseñado
        loadUi('gui/gui.ui', self)      
            
        #Inicializa Cámara
        self.start_cam(self)

        #Inicializa Lente
        self.start_lens(self)

        #Configura Lente
        self.config_lens(self)

        #Configura Cámara
        self.config_cam(self)

        #Configura Lente
        self.config_lens(self)
        
        #Muestra imagen
        self.start_recording(self) 

        #Espera boton motor
        self.motor_listen(self)

        #Espera boton captura
        self.capture_listen(self)

        #Espera cambios en la configuración
        self.config_listen(self)

        #Muestra GUI
        self.show()

    def start_cam(self, label):

        #Modo de Exposición
        self.cam.ExposureAuto = 'Off'
    	
        #Tiempo de exposición
        self.exposure_time = exposure_time

        #Número de promedios
        self.N = N

        #Formato
        self.cam.PixelFormat = "BayerRG8"

        #Inicia cámara
        self.cam.start()

    def config_cam(self, label):
        #Cambia tiempo de exposición
        self.cam.ExposureTime = self.exposure_time
        print(f'Exposición actual: {self.exposure_time}')

    def start_lens(self, label):
        # Iincializa lente
        self.o = Opto(port = 'COM3')
        self.o.connect()

    def config_lens(self, label):
        #Cambia tiempo de exposición
        self.current_value = current_value    
        self.current_step = current_step
        self.max_current = max_current
        self.min_current = min_current    
        thread = thread_lens(self.o, self.current_value)
        thread.start()
        print(f'Corriente actual: {self.current_value}')

    def config_program(self, label):
        #Cambia número de promedio
        self.N = self.new_N

    def start_recording(self, label):  
        #Timer 	
        timer = QtCore.QTimer(self)
        
        #Conexión
        timer.timeout.connect(self.update_image)
        timer.start(33)
        self.update_image()    

    def update_image(self):
        #Actualiza configuración
        self.interpolador = 'vecinos' if self.vecinos_btn.isChecked() else 'bilineal'
        self.exposure_time = int(self.exposicion_edit.text())
        self.new_N = int(self.N_edit.text())

        #Captura imagen
        raws = [np.uint16(self.cam.get_array()) for n in range(self.N)]
        raw = (1/self.N*sum(raws)).astype(np.uint8)
        
        #Medibles
        I90, I45, I135, I0 = polarization_full_dec_array(raw, interpolacion = self.interpolador)
        I90 = I90[::decimador,::decimador,:]
        I45 = I45[::decimador,::decimador,:]
        I135 = I135[::decimador,::decimador,:]
        I0 = I0[::decimador,::decimador,:]
        
        #Stokes
        S0, S1, S2 = calcular_stokes(I90, I45, I135, I0)

        #Medida a mostrar
        medida_str = self.medida_box.currentText()

        if medida_str == 'DoLP':
            medida = digitalizar(calcular_dolp(S0, S1, S2), 'DoLP')
        elif medida_str == 'AoLP':
            medida = digitalizar(calcular_aolp(S1, S2), 'AoLP')
        else:
            medida = digitalizar(locals()[medida_str], medida_str)
        
        #Imagen de la medida elegida
        img = medida.astype(np.uint8)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        #Formato Array to PixMap
        h, w, _ = img.shape
        bytes_per_line = 3 * w  # 3 canales (RGB) * ancho
        S0QIMG = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(S0QIMG)

        # Alerta píxeles saturados
        max_intensity = np.max(np.array([I0, I45, I90, I135]))
        if max_intensity == 255:
            print(str(self.counter) + ': Advertencia: Píxeles saturados') 
            self.counter = self.counter + 1

        #Plot
        self.img.setPixmap(pixmap)

    def copiar_motor_control(self, label):
        # Copiar archivos (update)
        self.rpi.copiar_motor_control()

    def move_up(self):
        thread = thread_motor("Y","B")
        thread.start()

    def move_down(self):
        thread = thread_motor("Y","F")
        thread.start()

    def move_left(self):
        thread = thread_motor("X","B")
        thread.start()

    def move_right(self):
        thread = thread_motor("X","F")
        thread.start()  

    def rotate_left(self):
        thread = thread_motor("T","B")
        thread.start()  

    def rotate_right(self):
        thread = thread_motor("T","F")
        thread.start()  
        
    def focus_minus_optolens(self):
        if self.current_value >= self.min_current:
            self.current_value -= self.current_step
            print(f'Corriente actual: {self.current_value}')
        else:
            print("Corriente mínima alcanzada.")
        thread = thread_lens(self.o, self.current_value)
        thread.start()  

    def focus_plus_optolens(self):
        if self.current_value <= self.max_current:
            self.current_value += self.current_step
            print(f'Corriente actual: {self.current_value}')
        else:
            print("Corriente máxima alcanzada.")
        thread = thread_lens(self.o, self.current_value)
        thread.start()  

    def auto_capture(self):
        #Detiene la cámara
        self.cam.stop()

        # Ejecuta comando
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.current_value}_mA_" + f"{timestamp}"
        runcmd("cd simplelib/ && python simple_intensities.py " + filename, verbose=True)
        
        #Vuelve a iniciar la cámara
        self.cam.start()
   
    def motor_listen(self, label):
        #Arriba
        up_btn = self.up_btn
        up_btn.clicked.connect(self.move_up)
        
        #Abajo
        dwn_btn = self.dwn_btn
        dwn_btn.clicked.connect(self.move_down)
        
        #Izquierda
        left_btn = self.left_btn
        left_btn.clicked.connect(self.move_left)
        
        #Derecha
        right_btn = self.right_btn
        right_btn.clicked.connect(self.move_right)

        #Girar izquierda
        rotate_left_btn = self.rotate_left_btn
        rotate_left_btn.clicked.connect(self.rotate_left)

        #Girar derecha
        rotate_right_btn = self.rotate_right_btn
        rotate_right_btn.clicked.connect(self.rotate_right)
    
    def capture_listen(self, label):
        capture_btn = self.capture_btn
        capture_btn.clicked.connect(self.auto_capture)

    def config_listen(self, label):
        config_btn = self.config_btn
        
        #Camara
        config_btn.clicked.connect(self.config_cam)

        #Programa
        config_btn.clicked.connect(self.config_program)
        
        #OptoTune
        focus_plus_btn = self.focus_plus_btn
        focus_plus_btn.clicked.connect(self.focus_plus_optolens)
        
        focus_minus_btn = self.focus_minus_btn
        focus_minus_btn.clicked.connect(self.focus_minus_optolens)

def main(rpi, cam):
    app = QApplication(sys.argv)
    instance = Ui(rpi, cam)
    app.exec_()

if __name__ == "__main__":

    # Conectar Raspberry Pi
    rpi = RPiController()
    rpi.conectar()

    try:
        # Inicia GUI con contexto de cámara
        with Camera() as cam:
            main(rpi, cam)  

    except Exception as e:
        print(f"Error durante la ejecución: {e}")

    finally:
        # Asegura la detención de la cámara y desconexión
        try:
            cam.stop()
        except Exception:
            pass  # Puede que la cámara ya esté detenida

        # Desconectar Raspberry Pi
        rpi.desconectar()

        # Salir del programa
        sys.exit()