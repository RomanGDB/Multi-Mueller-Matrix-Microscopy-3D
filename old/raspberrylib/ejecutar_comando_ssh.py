
import paramiko
import os

#Definiciones
RPI_USER = 'mwsi'
RPI_PASS = 'mwsi'
RPI_IP = '169.254.110.82'
RPI_PORT = 22

#Control de motores

def ejecutar_comando_ssh(comando):

    print('Conectando a raspberry...')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RPI_IP,RPI_PORT, username=RPI_USER, password=RPI_PASS)

    print('Ejecutando comando... ')

    # Realizar la copia segura utilizando SCP
    sftp = ssh.open_sftp()
    os.chdir('raspberrylib')
    sftp.put('motor_control.py', '/home/mwsi/Desktop/main/motor_control.py')
    os.chdir('..')
    sftp.close()

    #Ejecuta comando
    stdin, stdout, stderr = ssh.exec_command(comando)

    print(stdout.read().decode())
    print(stderr.read().decode())

    ssh.close()
    
    return stdout.readlines()
