'''
lanhuage: python
Descripttion:
'''

import glob
import os

from tqdm import tqdm

from convertmask.utils.methods import getMultiShapes
from convertmask.utils.methods.logger import logger


def getJsons(imgPath, maskPath, savePath, yamlPath=''):
    """
    imgPath: origin image path \n
    maskPath : mask image path \n
    savePath : json file save path \n
    
    >>> getJsons(path-to-your-imgs,path-to-your-maskimgs,path-to-your-jsonfiles) 

    """
    logger.info("currently, only *.jpg supported")

    if os.path.isfile(imgPath):
        getMultiShapes.getMultiShapes(imgPath, maskPath, savePath, yamlPath)

    elif os.path.isdir(imgPath):
        oriImgs = glob.glob(imgPath + os.sep + '*.jpg')
        maskImgs = glob.glob(maskPath + os.sep + '*.jpg')
        for i in tqdm(oriImgs):
            i_mask = i.replace(imgPath, maskPath)
            if os.path.exists(i_mask):
                # print(i)
                getMultiShapes.getMultiShapes(i, i_mask, savePath, yamlPath)
            else:
                logger.warning('corresponding mask image not found!')
                continue
    else:
        logger.error('input error. got [{},{},{},{}]. file maybe missing.'.format(
            imgPath, maskPath, savePath, yamlPath))
    logger.info('Done! See here. {}'.format(savePath))


def getXmls(imgPath, maskPath, savePath):
    logger.info("currently, only *.jpg supported")

    if os.path.isfile(imgPath):
        getMultiShapes.getMultiObjs_voc(imgPath, maskPath, savePath)
    elif os.path.isdir(imgPath):
        oriImgs = glob.glob(imgPath + os.sep + '*.jpg')
        maskImgs = glob.glob(maskPath + os.sep + '*.jpg')

        for i in tqdm(oriImgs):
            i_mask = i.replace(imgPath, maskPath)
            # print(i)
            if os.path.exists(i_mask):
                getMultiShapes.getMultiObjs_voc(i, i_mask, savePath)
            else:
                logger.warning('corresponding mask image not found!')
                continue
    else:
        logger.error('input error. got [{},{},{}]. file maybe missing.'.format(
            imgPath, maskPath, savePath))
    logger.info('Done! See here. {}'.format(savePath))
