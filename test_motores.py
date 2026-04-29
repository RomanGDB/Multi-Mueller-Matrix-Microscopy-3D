import paramiko
import os
import sys

# Datos de acceso a la Raspberry
RPI_USER = 'estefany0134'                  # Cambialo si tu usuario es otro
RPI_PASS = 'estefany0134'
RPI_IP   = '169.254.151.60'
RPI_PORT = 22

angulo_motor1 = float(sys.argv[1])
angulo_motor2 = float(sys.argv[2])
dir1 = sys.argv[3].lower()
dir2 = sys.argv[4].lower()

# ---------- COPIAR SCRIPT ----------
def copiar_script(archivo_local, archivo_remoto):
    print("📤 Copiando script a la Raspberry...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RPI_IP, RPI_PORT, username=RPI_USER, password=RPI_PASS)

    sftp = ssh.open_sftp()
    sftp.put(archivo_local, archivo_remoto)
    sftp.close()
    ssh.close()

    print("✔ Archivo copiado correctamente.\n")


# ---------- EJECUTAR COMANDO ----------
def ejecutar_comando(comando):
    print("🔗 Conectando a la Raspberry...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RPI_IP, RPI_PORT, username=RPI_USER, password=RPI_PASS)

    print(f"▶ Ejecutando: {comando}\n")

    stdin, stdout, stderr = ssh.exec_command(comando)

    print(stdout.read().decode())
    print(stderr.read().decode())

    ssh.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    
    ruta_script_local = r"C:\Users\roman\OneDrive\Escritorio\MuellerMatrixMicroscope\programa_motores.py"
    ruta_script_remoto = f"/home/{RPI_USER}/programa_motores.py"

    # 1️⃣ Copiar
    #copiar_script(ruta_script_local, ruta_script_remoto)

    # 2️⃣ Dar permisos (por si acaso)
    ejecutar_comando(f"chmod +x {ruta_script_remoto}")

    # 3️⃣ Ejecutar con parámetros
    comando = (
        f"python3 {ruta_script_remoto} "
        f"{angulo_motor1} {angulo_motor2} {dir1} {dir2}"
    )

    ejecutar_comando(comando)