import mhd
from scipy.ndimage import morphology
import numpy as np
import boundingbox as bb

def label_cc(img, connectivity):
    from skimage import measure
    bbox = bb.bbox(img>0)
    cropped = bb.crop(img, bbox)
    return bb.uncrop(measure.label(cropped, connectivity=connectivity, background=0), img.shape, bbox)

def largest(img, n=1):
    labels = label_cc(img, connectivity=3)
    area = np.bincount(labels.flat)
    new_image = np.zeros_like(labels)
    indices = np.argsort(area)[::-1]
    for i in range(n):
        new_image[labels==indices[i+1]] = 1
    return new_image.astype(np.uint8)

def extract_lung(volume, t_air=-500):
    air = volume < t_air
    body = 1 - air
    filled = morphology.binary_fill_holes(body, np.ones((1,3,3)))
    air_inbody = filled - body
    lung = largest(air_inbody)
    return lung
