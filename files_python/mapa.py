from pylab import *

from PIL import Image

import matplotlib.cbook as cbook


def graficar(x,y):
    datafile = cbook.get_sample_data("C:\\Users\\michluna\\OneDrive - Cisco\\Desktop\\VSC PYTHON\\SmartSpaces\\files_python\\mapa.png")
    h = Image.open(datafile)
    #dpi = rcParams['figure.dpi']
    #print(dpi)
    dpi= 50
    figsize = h.size[0]/dpi, h.size[1]/dpi

    figure(figsize=figsize)
    ax = axes([0,0,1,1], frameon=False)
    ax.set_axis_off()
    ax.set_xlim(0,6)
    ax.set_ylim(0,7)
    #im = imshow(h, origin='upper',extent=[-2,4,-2,4])  # axes zoom in on portion of image
    #im2 = imshow(h, origin='lower',extent=[0,6,0,7]) # image is a small inset on axes
    plt.plot(x,y,marker='*',color = 'blue')
    plt.plot(3.854,2.887,marker='$3$',color = 'red')
    plt.plot(1.611,2.274,marker='$4$',color = 'red')
    plt.plot(4.366,4.144,marker='$7$',color = 'red')
    plt.imshow(h, origin='lower',extent=[0,6,0,7])
    plt.show()