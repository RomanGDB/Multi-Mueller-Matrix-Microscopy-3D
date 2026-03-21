import paramiko
import subprocess
import os

# Parámetros Raspberry Pi
RPI_IP = '169.254.110.82'
RPI_PORT = 22
RPI_USER = 'mwsi'
RPI_PASS = 'mwsi'

class RPiController:
    def __init__(self, ip=RPI_IP, port=RPI_PORT, user=RPI_USER, password=RPI_PASS):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.ssh = None
        self.sftp = None

    def conectar(self):
        print("Conectando a Raspberry Pi...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, username=self.user, password=self.password)
        self.sftp = self.ssh.open_sftp()
        print("Conexión establecida.")

    def copiar_motor_control(self):
        if self.sftp is None:
            raise Exception("No hay conexión SFTP.")
        print("Copiando motor_control.py...")
        cwd = os.getcwd()
        self.sftp.put(os.path.join(cwd, 'raspberrylib', 'motor_control.py'), '/home/mwsi/Desktop/main/motor_control.py')
        print("Archivo copiado.")

    def ejecutar(self, comando):
        if self.ssh is None:
            raise Exception("No hay conexión SSH.")
        print(f"Ejecutando: {comando}")
        stdin, stdout, stderr = self.ssh.exec_command(comando)
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        if salida:
            print("Salida:\n", salida)
        if errores:
            print("Errores:\n", errores)
        return salida, errores
    
    def desconectar(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        print("Desconectado de la Raspberry Pi.")
