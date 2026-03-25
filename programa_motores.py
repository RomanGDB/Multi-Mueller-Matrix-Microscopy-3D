import RPi.GPIO as GPIO
import time
import threading
import sys

# --- CONFIGURACIÓN DE PINES ---
motor1_pins = [22, 24, 26, 32]   # Motor 1
motor2_pins = [29, 31, 33, 35]   # Motor 2

# --- SECUENCIA FASE COMPLETA ---
seq_full = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
]

# --- CONFIGURACIÓN GPIO ---
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

for pin in motor1_pins + motor2_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# --- PARÁMETROS DEL MOTOR ---
PASOS_POR_VUELTA = 512  
GRADOS_POR_PASO = 360 / PASOS_POR_VUELTA

# --- FUNCIONES ---
def angulo_a_pasos(angulo):
    """Convierte un ángulo en grados a cantidad de pasos."""
    return int(abs(angulo) / GRADOS_POR_PASO)

def mover_motor(pines, angulo, delay=0, sentido=1):
    """Mueve el motor cierta cantidad de grados."""
    pasos = angulo_a_pasos(angulo)
    secuencia = seq_full if sentido == 1 else list(reversed(seq_full))
    
    for _ in range(pasos):
        for paso in secuencia:
            for pin, val in zip(pines, paso):
                GPIO.output(pin, val)
            time.sleep(delay)

# --- BLOQUE PRINCIPAL ---
try:
    print("=== Control de motores paso a paso (enfrentados) ===")
    
    # # --- ENTRADAS DESDE TERMINAL ---

    ang1 = float(sys.argv[1])
    ang2 = float(sys.argv[2])
    dir1 = sys.argv[3].lower()
    dir2 = sys.argv[4].lower()

    # angulo_motor1 = 45 #float(input("Ingrese ángulo para Motor 1 (°): "))
    # angulo_motor2 = 45#float(input("Ingrese ángulo para Motor 2 (°): "))
    
    # dir1 = 'h' #input("Dirección Motor 1 (h=horario / a=antihorario): ").strip().lower()
    # dir2 = 'a' #input("Dirección Motor 2 (h=horario / a=antihorario): ").strip().lower()
    
    sentido1 = 1 if dir1 == "h" else -1
    sentido2 = 1 if dir2 == "h" else -1

    # --- MOVER AMBOS MOTORES AL MISMO TIEMPO ---
    t1 = threading.Thread(target=mover_motor, args=(motor1_pins, ang1, 0.003, sentido1))
    t2 = threading.Thread(target=mover_motor, args=(motor2_pins, ang2, 0.003, sentido2))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"\n Motor 1 giró {ang1}° en sentido {'horario' if sentido1 == 1 else 'antihorario'}")
    print(f" Motor 2 giró {ang2}° en sentido {'horario' if sentido2 == 1 else 'antihorario'}")

finally:
    GPIO.cleanup()
    print("\nGPIO liberado correctamente.")

