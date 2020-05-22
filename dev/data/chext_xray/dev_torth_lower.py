import torch
import numpy as np
from skimage import transform
import SimpleITK as sitk

from logging import basicConfig, getLogger, INFO
basicConfig(level=INFO, format='%(asctime)s %(levelname)s :%(message)s')
logger = getLogger(__name__)

MU_WATER = 0.268
MU_BONE = 0.521
MU_AIR = 0
MU_WATER_10, MU_BONE_10 = 5.33, 19.9
MU_WATER_20, MU_BONE_20 = 0.81, 2.83
MU_WATER_25, MU_BONE_25 = 0.508, 1.56
MU_WATER_30, MU_BONE_30 = 0.376, 0.982
MU_WATER_40, MU_BONE_40 = 0.268, 0.521
MU_WATER_60, MU_WATER_120 = 0.206, 0.161
MU_BONE_60, MU_BONE_120 = 0.275, 0.164

t_air = -1000
t_water = 0
t_bone = 1000

def compose(volume, t1,t2,w1,w2):
    volume = volume.clone()
    volume.sub_(t1).div_(t2-t1)
    volume.mul_(w2-w1).add_(w1)
    return volume

def resize(proj, spacings):
    proj = proj.cpu().numpy().astype(np.float64)
    return transform.rescale(proj, (spacings[2]/spacings[0],1), clip=False, preserve_range=True, multichannel=False)

def project(volume, spacings):
    proj = torch.sum(volume, dim=1)
    return resize(proj, spacings)

def compose3(volume, t1,t2,t3, w1,w2,w3):
    a = compose(volume, t1,t2,w1,w2)
    a.clamp_(w1,w2)
    b = compose(volume, t2,t3,w2,w3)
    b.clamp_(w2,w3*2)
    cond = a < w2
    a.mul_(cond)
    b.mul_(~cond)
    return a.add_(b)
#    return cond * a + ~cond * b#a.add_(b)

def hu2mu(volume, mu_water):
    volume = volume.clone()
    volume.add_(1000)
    volume.div_(1000/mu_water)
    volume.clamp_(0, 4*mu_water)
    return volume

def rescale(arr):
    return np.round(10*arr).astype(np.int16)


def do(t_volume, mu_water, mu_bone):
    mu_vol = compose3(t_volume, t_air, t_water, t_bone, MU_AIR, mu_water, mu_bone)
    proj = project(mu_vol, spacings)
    return rescale(proj)

def normalize(x, wlww=None, minmax=None, percentile=None):
    if wlww is None and minmax is None and percentile is None:
        raise RuntimeError('Either wlww or minmax is required')

    if wlww is not None:
        wl, ww = wlww
        minmax = (wl-ww/2, wl+ww/2)

    if percentile is not None:
        min_z, max_z = int(x.shape[0]*.1), int(x.shape[0]*.5)
        minmax = np.percentile(x[min_z:max_z],[percentile,100-percentile])

    x = np.clip(x, minmax[0], minmax[1]).astype(np.float)
    return np.round(255*(x - minmax[0])/(minmax[1]-minmax[0])).astype(np.uint8)


def percent(img, mask, p):
    return np.percentile(img[mask],[p,100-p])

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logger.info('using ' + device.type)

from PIL import Image
from pathlib import Path
from lung_extract import extract_lung
import mhd
import tqdm

mhd_dir = r'E:\dataset\LIDC\mhd'
outdir = Path('output')
taiou = []
count = 0
paths = []
for p in Path(mhd_dir).glob('*.mha'):
    input_fn = str(p)
    h = mhd.read_header(input_fn)
    if h['ElementSpacing'][2] > 1:
        continue
    
    taiou.append((count, p.stem))
    paths.append(p)
    count += 1
#import pandas as pd
#df_taiou = pd.DataFrame(taiou, columns=['fn','id'])
#df_taiou.to_excel('taiou.xlsx')
count = 0
#for p in tqdm.tqdm(Path(mhd_dir).glob('*.mha'),total=len(taiou)):
for p in tqdm.tqdm(paths):
    input_fn = str(p)
    h = mhd.read_header(input_fn)
#    if h['ElementSpacing'][2] > 1:
#        continue
    sitk_volume = sitk.ReadImage(input_fn)
    volume = sitk.GetArrayFromImage(sitk_volume)[::-1].copy()
#    lung = extract_lung(volume)
    t_volume = torch.from_numpy(volume).float().to(device)
    spacings = sitk_volume.GetSpacing()
    
#    mu_volume = hu2mu(t_volume, MU_WATER)
    proj_lower = do(t_volume, MU_WATER_25, MU_BONE_25)
    proj_low = do(t_volume, MU_WATER_60, MU_BONE_60)
    proj_high = do(t_volume, MU_WATER_120, MU_BONE_120)
#    mhd.write('proj_low.mha',proj_low)
#    mhd.write('proj_high.mha',proj_high)
#    mhd.write('proj_mu.mha',proj_mu)
#    mhd.write('proj_lung.mha',proj_lung)
#    break
#    mhd.write(outdir/'{:03d}.mha'.format(count), proj_mu)
    mhd.write(outdir/'{:03d}_lower.mha'.format(count), proj_lower)
    mhd.write(outdir/'{:03d}_low.mha'.format(count), proj_low)
    mhd.write(outdir/'{:03d}_high.mha'.format(count), proj_high)
#    mhd.write(outdir/'{:03d}_lung.mha'.format(count), proj_lung.astype(np.int16))
#    perc = 1
#    Image.fromarray(normalize(proj_mu, minmax=percent(proj_mu, proj_lung,3))).save(Path('png')/'{:03d}.png'.format(count))
#    Image.fromarray(normalize(proj_high,minmax=percent(proj_high, proj_lung,2))).save(Path('png')/'{:03d}_high.png'.format(count))
#    Image.fromarray(normalize(proj_low,minmax=percent(proj_low, proj_lung,5))).save(Path('png')/'{:03d}_low.png'.format(count))
#    Image.fromarray(255*proj_lung.astype(np.uint8)).save(outdir/'{:03d}_lung.png'.format(count))
    count += 1
#    if count > 3:
#        break
