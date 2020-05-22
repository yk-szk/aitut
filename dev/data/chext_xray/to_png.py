import mhd
from PIL import Image
from matplotlib.pyplot import rcParams
rcParams['figure.figsize'] = 10,10
import matplotlib.pyplot as plt
import numpy as np

def normalize(x, wlww=None, minmax=None, percentile=None):
    if wlww is None and minmax is None and percentile is None:
        raise RuntimeError('Either wlww or minmax is required')

    if wlww is not None:
        wl, ww = wlww
        minmax = (wl-ww/2, wl+ww/2)

    if percentile is not None:
        minmax = np.percentile(x,[percentile,100-percentile])

    x = np.clip(x, minmax[0], minmax[1]).astype(np.float)
    return np.round(255*(x - minmax[0])/(minmax[1]-minmax[0])).astype(np.uint8)

def percent(img, mask, p):
    return np.percentile(img[mask],[p,100-p])

from scipy import ndimage
def dilation(img, k=16):
    return ndimage.binary_dilation(img,structure=np.ones((k,k)))

m0 = 0.268
m1 = 0.161
for i in range(285):
    print(i)
    img, h = mhd.read('output/{:03d}.mha'.format(i))
    lung,_ = mhd.read('output/{:03d}_lung.mha'.format(i))
    
    lung_bin = dilation(lung > 100)

    normed = normalize(img, percentile=3)
    Image.fromarray(normed).save('png/regular/{:03d}.png'.format(i))
    plt.imshow(normed, cmap='gray')
    plt.show()

    img_h,h = mhd.read('output/{:03d}_high.mha'.format(i))
    normed = normalize(img_h, percentile=3)
    plt.imshow(normed, cmap='gray')
    plt.show()
    Image.fromarray(normed).save('png/bone_suppression/{:03d}.png'.format(i))

    img_h,h = mhd.read('output/{:03d}_lower.mha'.format(i))
    normed = normalize(img_h, percentile=3)
    plt.imshow(normed, cmap='gray')
    plt.show()
    Image.fromarray(normed).save('png/bone_enhancement/{:03d}.png'.format(i))

    # lung_bin = lung > 50
    # Image.fromarray((lung_bin*255).astype(np.uint8)).save('png/lung/{:03d}.png'.format(i))
#    if i >= 10:
#        break
