import sys

# Definir la cantidad de pasos en cada direccion
X_STEPS = 4
Y_STEPS = 5

def capturar_muestra(X, Y):
    # comienza en esquina sup izq
    x = 0
    y = 0
    dx = 1
    dy = 0

    for i in range(X*Y):
        
        #Imprime posicion actual
        print (x, y)

        # En alguno de los limites laterales, baja
        if (x in [0, X - 1]) and (x + y != 0):

            if dy == 0:
                dx_ = dx
                dx, dy = 0, 1 

            else:
                dx, dy = -dx_, 0
    
        print('dx', dx)
        print('dy', dy)

        x, y = x + dx, y + dy

        if dx != 0:
            direccion_x = "F" if dx > 0 else "B"
            print("X " + direccion_x)
            
        if dy != 0:
            direccion_y = "F" if dy > 0 else "B"
            print("Y " + direccion_y)

        print(i)
        print(' ')
def main():

    #Captura muestra, calcula tiempo
    capturar_muestra(X_STEPS, Y_STEPS)        

    return True

if __name__ == '__main__':

    if main():
        sys.exit(0)
    else:
        sys.exit(1)
