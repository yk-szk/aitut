import SimpleITK as sitk
data = {
    1:[100,128],
    2:[94,153],
    3:[97,65],
    4:[130],
    5:[127],
    6:[69],
    7:[110],
    8:[93,145],
    9:[128],
    10:[113,186],
}
wlww = (-700,1200)
minmax = (wlww[0]-wlww[1]//2,wlww[0]+wlww[1]//2)
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
from scipy.signal import convolve2d
import numpy as np
import mhd
import tqdm
import matplotlib.pyplot as plt
import math
from PIL import Image

org_dir = 'volume/corona'
mask_dir = 'volume/Lung_and_Infection_Mask'
out_dir = 'patches'
kernel = np.ones((20,20))
counts = 0
ps = 32
stride = 20
for i in tqdm.trange(1,11):
    org = org_dir + '/coronacases_org_{:03d}.nii.gz'.format(i)
    mask = mask_dir + '/coronacases_{:03d}.nii.gz'.format(i)
    s_img = sitk.ReadImage(mask)
    s_org = sitk.ReadImage(org)
    org = sitk.GetArrayFromImage(s_org)
    ggo = sitk.GetArrayFromImage(s_img) == 3
    tm = np.array(s_img.GetDirection()).reshape((3,3))
    h = {'TransformMatrix':tm}
    org, ggo = mhd.reorient(org,h), mhd.reorient(ggo,h)
    for z in data[i]:
        conved = convolve2d(ggo[z], kernel, mode='same')
        s_org = org[z]
        conved = conved[::stride, ::stride]
        valid = conved > 200
        for coords in zip(*np.nonzero(valid)):
            ss = tuple(slice(c*stride-ps//2,c*stride+math.ceil(ps/2)) for c in coords)
            patch = s_org[ss]
            Image.fromarray(normalize(patch,wlww=wlww)).save('patches/GGO/{:03d}.png'.format(counts))
            counts += 1