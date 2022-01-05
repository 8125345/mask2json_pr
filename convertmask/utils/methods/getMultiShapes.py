'''
lanhuage: python
Descripttion:
'''
try:
    from labelme import __version__ as labelme_version
except:
    labelme_version = '4.5.6'
import sys

sys.path.append("..")

import copy
import json
import os

import cv2
import numpy as np
import skimage.io as io
import yaml

from convertmask.utils.methods import rmQ
from convertmask.utils.methods.getShape import *
from convertmask.utils.methods.img2base64 import imgEncode



def rs(st:str):
    s = st.replace('\n','').strip()
    return s


def readYmal(filepath, labeledImg=None):
    if os.path.exists(filepath):
        if filepath.endswith('.yaml'):
            f = open(filepath)
            y = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
            tmp = y['label_names']
            objs = zip(tmp.keys(), tmp.values())
            return sorted(objs)
        elif filepath.endswith('.txt'):
            f = open(filepath,'r',encoding='utf-8')
            classList = f.readlines()
            f.close()
            l3 = [rs(i) for i in classList]
            l = list(range(1,len(classList)+1))
            objs = zip(l3,l)
            return sorted(objs)
    elif labeledImg is not None and filepath == "":
        """
        should make sure your label is correct!!!
        """
        labeledImg = np.array(labeledImg, dtype=np.uint8)

        labeledImg[labeledImg > 0] = 255
        labeledImg[labeledImg != 255] = 0

        _, labels, stats, centroids = cv2.connectedComponentsWithStats(
            labeledImg)

        labels = np.max(labels) + 1
        labels = [x for x in range(1, labels)]

        classes = []
        for i in range(0, len(labels)):
            classes.append("class{}".format(i))

        return zip(classes, labels)
    else:
        raise FileExistsError('file not found')

def getMultiShapes(oriImgPath,
                   labelPath,
                   savePath='',
                   labelYamlPath='',
                   flag=False,
                   areaThresh=500):
    """
    oriImgPath : for change img to base64  \n
    labelPath : mask file \n
    savePath : json file save path  \n
    labelYamlPath : labelmap  \n

    """
    # print('-==================')
    # print(oriImgPath)
    # print(labelPath)
    # print(savePath)
    # print(labelYamlPath)
    # print('-==================')
    if isinstance(labelPath, str):
        if os.path.exists(labelPath):
            label_img = io.imread(labelPath)
        else:
            raise FileNotFoundError('mask/labeled image not found')
    else:
        # img = oriImg
        label_img = labelPath
    
    # print(np.max(label_img))

    if np.max(label_img) > 127:
        # print('too many classes! \n maybe binary?')
        label_img[label_img > 127] = 255
        label_img[label_img != 255] = 0
        label_img = label_img / 255

    labelShape = label_img.shape

    labels = readYmal(labelYamlPath, label_img)
    # print(list(labels))
    shapes = []
    obj = dict()
    obj['version'] = labelme_version
    obj['flags'] = {}
    for la in list(labels):

        if la[1] > 0:
            # print(la[0])
            img = copy.deepcopy(label_img)   # img = label_img.copy()
            img = img.astype(np.uint8)

            img[img == la[1]] = 255

            img[img != 255] = 0

            region = process(img.astype(np.uint8))

            if isinstance(region, np.ndarray):
                points = []
                for i in range(0, region.shape[0]):
                    # print(region[i][0])
                    points.append(region[i][0].tolist())
                shape = dict()
                shape['label'] = la[0]
                shape['points'] = points
                shape['group_id'] = 'null'
                shape['shape_type'] = 'polygon'
                shape['flags'] = {}
                shapes.append(shape)

            elif isinstance(region, list):
                # print(len(region))
                for subregion in region:
                    points = []
                    for i in range(0, subregion.shape[0]):
                        points.append(subregion[i][0].tolist())
                    shape = dict()
                    shape['label'] = la[0]
                    shape['points'] = points
                    shape['group_id'] = 'null'
                    shape['shape_type'] = 'polygon'
                    shape['flags'] = {}
                    shapes.append(shape)

    # print(len(shapes))
    obj['shapes'] = shapes
    # print(shapes)
    (_, imgname) = os.path.split(oriImgPath)
    obj['imagePath'] = imgname
    # print(obj['imagePath'])
    obj['imageData'] = str(imgEncode(oriImgPath))

    obj['imageHeight'] = labelShape[0]
    obj['imageWidth'] = labelShape[1]

    j = json.dumps(obj, sort_keys=True, indent=4)

    

    # print(j)

    if not flag:
        saveJsonPath = savePath + os.sep + obj['imagePath'][:-4] + '.json'
        # print(saveJsonPath)
        with open(saveJsonPath, 'w') as f:
            f.write(j)

        rmQ.rm(saveJsonPath)

    else:
        return j



