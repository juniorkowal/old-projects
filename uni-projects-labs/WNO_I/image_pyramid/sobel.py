import numpy as np
from PIL import Image, ImageFilter,ImageOps

img = Image.open('Alice_apple.jpg')
obraz2=np.asarray(img)

def kernel(size,sigma):
    a=np.zeros((size,size))
    k=int(size/2)
    for i in range(size):
        for j in range(size):
            a[i][j]=(1/(2*3.14*sigma**2))*2.7**(-(((i-(k+1))**2+(j-(k+1))**2)/2*sigma**2))
    return a


def grayscale(red, green, blue):
    gray = 0.2126*red+0.7152*green+0.0722*blue
    return gray.astype(int)

def filtr_gaussa(szary_obraz):
    gauss = kernel(7,1)
    filtered = np.zeros(szary_obraz.shape)
    for i in range(szary_obraz.shape[0]-6):
        for j in range(szary_obraz.shape[1]-6):
            filtered[i+3][j+3] = np.sum(np.multiply(gauss, szary_obraz[i:i+7, j:j+7]))
    return filtered

szary=grayscale(obraz2[:,:,0],obraz2[:,:,1],obraz2[:,:,2])
gaussowski=filtr_gaussa(szary)


wys2=Image.fromarray(gaussowski)
wys=Image.fromarray(szary)
wys3_0=img.filter(ImageFilter.GaussianBlur(radius = 1))
wys3=ImageOps.grayscale(wys3_0)



wys.show()
wys2.show()
wys3.show()


