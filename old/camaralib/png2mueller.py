sys.path.append('../')
from camaralib.analogizar import analogizar
from stokeslib.desacoplar_mueller import desacoplar_mueller

def png2mueller(M_show, medida):
    
    #Analogiza Matriz de Mueller
    M_analogo = analogizar(M_show, medida)

    # Desacopla imagen en matriz
    M = desacoplar_mueller(M_analogo)

    return M
