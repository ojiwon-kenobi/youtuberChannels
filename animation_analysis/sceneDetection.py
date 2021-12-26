from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
HEIGHT  = 720
WIDTH = 1280
DIFF= 1

def getFeatureVectorOfImage (imagePath):
    image = cv2.imread(imagePath)
    vectors = []
    for i, col in enumerate(['b', 'g', 'r']):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        vectors.append(hist)
        plt.plot(hist, color = col)
        plt.xlim([0, 256])
    plt.show()
    vectors = np.vstack(vectors)
    return vectors

