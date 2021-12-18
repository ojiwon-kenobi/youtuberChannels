import os
import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image
from pathlib import Path
import sys
from scipy.ndimage.filters import gaussian_filter
from torchvision import transforms
import cv2
import glob

def xdog(original, count, lineartPath, epsilon=0.5, phi=10, k=1.4, tau=1, sigma=0.5):
    image = cv2.imread(original, cv2.IMREAD_GRAYSCALE)
    image = gaussian_filter(image, 0.7)
    gauss1 = gaussian_filter(image, sigma)
    gauss2 = gaussian_filter(image, sigma*k)

    D = gauss1 - tau*gauss2

    U = D/255
    
    for i in range(0,len(U)):
        for j in range(0,len(U[0])):
            U[i][j] = abs(1-U[i][j])
    for i in range(0, len(U)):
        for j in range(0, len(U[0])):
            if U[i][j] >= epsilon:
                U[i][j] = 1
            else:
                ht = np.tanh(phi*(U[i][j] - epsilon))
                U[i][j] = 1 + ht

    lineart = U*255
    success = cv2.imwrite(lineartPath+"/%d.png" % count, lineart)
