import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

# Guarda imagen con la barra

# Magnificacion
Mag = 11

def guardar_img(path, img, name, cmap = 'gray', color = 'white', clim = None):

    #Crea Figure
    fig = plt.figure()

    #Crea ejes
    ax = fig.add_subplot()

    #Muestra la imagen
    im = ax.imshow(img, cmap=cmap)

    #Titulo
    ax.set_title(name, fontsize = 20)

    #Barra
    scalebar = AnchoredSizeBar(ax.transData, 0.5*Mag*100/3.45 , '100 μm', 'lower right', pad=0.2, 
                                color=color, frameon=False, size_vertical=6,
                                fontproperties=fm.FontProperties(size=14))
    
    ax.add_artist(scalebar)

    #Limites de la barra
    if clim != None:
        cbar = plt.colorbar(im)
        im.set_clim(vmin=clim[0],vmax=clim[1])

    #Guarda Figura
    plt.savefig(path + '/' + name + '.png')

    #Cierra Figura
    plt.close()

    return None