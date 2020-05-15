import SimpleITK as sitk
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

kinds = ['emphysema', 'honeycomb', 'normal']
from scipy.signal import convolve2d
import numpy as np
import mhd
import tqdm
import matplotlib.pyplot as plt
import math
from PIL import Image
from pathlib import Path

out_dir = 'patches'
kernel = np.ones((20,20))
ps = 32
stride = 20
for kind in kinds:
    counts = 0
    for mask_fn in tqdm.tqdm(Path('volume/{}'.format(kind)).glob('mask*.nii.gz')):
        org_fn = mask_fn.parent / (str(mask_fn.name)[5:-7]+'.mha')
        s_mask = sitk.ReadImage(str(mask_fn))
        org = sitk.GetArrayFromImage(sitk.ReadImage(str(org_fn)))
        mask = sitk.GetArrayFromImage(s_mask)
        tm = np.array(s_mask.GetDirection()).reshape((3,3))
        h = {'TransformMatrix':tm}
        org, mask = mhd.reorient(org,h), mhd.reorient(mask,h)
        zs = np.nonzero(np.sum(mask,axis=(1,2)))[0]
        for z in zs:
            conved = convolve2d(mask[z], kernel, mode='same')
            s_org = org[z]
            conved = conved[::stride, ::stride]
            valid = conved > 200
            for coords in zip(*np.nonzero(valid)):
                ss = tuple(slice(c*stride-ps//2,c*stride+math.ceil(ps/2)) for c in coords)
                patch = s_org[ss]
                Image.fromarray(normalize(patch,wlww=wlww)).save('patches/{}/{:03d}.png'.format(kind,counts))
                counts += 1