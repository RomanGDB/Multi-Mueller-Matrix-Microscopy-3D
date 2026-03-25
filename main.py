import paramiko
import sys
import time
import os
import cv2
import numpy as np
from datetime import datetime
from simple_pyspin import Camera
from opto import Opto

# ---------- CONFIG RPI ----------
RPI_USER = 'estefany0134'
RPI_PASS = 'estefany0134'
RPI_IP   = '169.254.151.60'
RPI_PORT = 22

RUTA_SCRIPT_REMOTO = f"/home/{RPI_USER}/programa_motores.py"

# ---------- CONFIG CAMARA ----------
output_path = 'output/'
os.makedirs(output_path, exist_ok=True)
exposure_time = 5000

# ---------- CONFIG LENTE ----------
LENS_PORT = 'COM3'  # cambiar si usas Linux
diop_list = [37,38,39,40,41,42,43]

# ---------- PREVIEW ----------

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

def preview_polarizado():

    o = Opto(port=LENS_PORT)
    o.connect()

    diop_central = diop_list[len(diop_list)//2]
    o.current(diop_central)
    print(f"Lente en preview: {diop_central} 1/m")

    cv2.namedWindow("Polarizacion", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Polarizacion", 700, 500)

    with Camera() as cam:
        cam.ExposureAuto = 'Off'
        cam.ExposureTime = exposure_time
        cam.PixelFormat = "BayerRG16"

        cam.start()

        while True:
            img = cam.get_array()

            I90, I45, I135, I0 = polarization_full_dec_array(img)

            I0_disp   = (I0[::4, ::4] // 256).astype(np.uint8)
            I45_disp  = (I45[::4, ::4] // 256).astype(np.uint8)
            I90_disp  = (I90[::4, ::4] // 256).astype(np.uint8)
            I135_disp = (I135[::4, ::4] // 256).astype(np.uint8)

            top    = np.hstack((I0_disp, I45_disp))
            bottom = np.hstack((I135_disp, I90_disp))
            grid   = np.vstack((top, bottom))

            cv2.imshow("Polarizacion", grid)

            key = cv2.waitKey(1) & 0xFF

            # Control de lente con teclas 1–7
            if key in [ord(str(i)) for i in range(1, len(diop_list) + 1)]:
                idx = int(chr(key)) - 1
                diop = diop_list[idx]
                o.current(diop)
                print(f"Lente cambiada a {diop} 1/m")

            # Salir
            if key == ord('q'):
                cam.stop()
                cv2.destroyAllWindows()
                o.close()
                sys.exit(0)

            # Capturar Mueller
            elif key == 13 or key == 10:
                cam.stop()
                cv2.destroyAllWindows()
                o.close()
                return True

# ---------- FOTO ----------
def tomar_foto(nombre):

    with Camera() as cam:
        cam.ExposureAuto = 'Off'
        cam.ExposureTime = exposure_time
        cam.PixelFormat = "BayerRG16"

        cam.start()
        img = cam.get_array()
        cam.stop()

    filename = f"{nombre}.png"

    cv2.imwrite(filename, img)
    print(f"Imagen guardada: {filename}")

# ---------- LENTE ----------
def set_lente(o, diop):
    o.current(diop)
    print(f"Lente en {diop:.2f} 1/m")
    time.sleep(0.3)

# ---------- SSH ----------
class SSHConnection:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = None

    def __enter__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, self.port, username=self.user, password=self.password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def ejecutar(self, comando):
        stdin, stdout, stderr = self.client.exec_command(comando)
        print(stdout.read().decode())
        print(stderr.read().decode())

# ---------- MOVER ----------
def mover(ssh_conn, m1, m2, d1, d2, delay=2):
    comando = f"python3 {RUTA_SCRIPT_REMOTO} {m1} {m2} {d1} {d2}"
    print(f"Moviendo: {comando}")
    ssh_conn.ejecutar(comando)
    time.sleep(delay)

# ---------- MAIN ----------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Uso: python script.py nombre_captura")
        sys.exit(1)

    folder = sys.argv[1]

    # PREVIEW
    preview_polarizado()

    # INICIALIZAR LENTE
    o = Opto(port=LENS_PORT)
    o.connect()

    with SSHConnection(RPI_IP, RPI_PORT, RPI_USER, RPI_PASS) as ssh:

        # Generar carpeta principal con fecha y hora
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        folder_timestamp = f"{folder}_{timestamp}"

        movimientos = [(45, 45),(45, 45),(45, 0),(45, 90)]
        polar_labels = ["0_0", "45_45", "90_90", "135_90"]

        for label, (m1, m2) in zip(polar_labels, movimientos):

            print(f"\n=== POSICION {label} ===")

            for diop in diop_list:
                # Configurar lente
                set_lente(o, diop)

                # Crear carpeta de salida por corriente
                folder_corriente = os.path.join(output_path, folder_timestamp, f"{diop}")
                os.makedirs(folder_corriente, exist_ok=True)

                # Tomar foto
                nombre_foto = os.path.join(folder_corriente, label)
                tomar_foto(nombre_foto)

            # Mover motores    
            mover(ssh, m1, m2, 'a', 'h')

    print("Secuencia completa.")
