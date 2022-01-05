'''
@lanhuage: python
@Descripttion: mask2json.
@version: beta
@Author: zhaoliang
@Date: 2021-7-6
'''
import sys
sys.path.append('..')
import os
from pathlib import Path
from glob import glob
from convertmask.utils.methods import getMultiShapes

if __name__ == "__main__":
    """
    main process
    """

    base_path = Path('/Users/clustar/Desktop/项目/金盛兰数据_超长/精品废钢超长最新/train')
    data_augmentation = base_path / 'data_augmentation'
    VerticalFlip_image = data_augmentation / 'VerticalFlip' / 'image'
    VerticalFlip_mask = data_augmentation / 'VerticalFlip' / 'mask'
    VerticalFlip_save_json = data_augmentation / 'VerticalFlip' / 'json'
    VerticalFlip_save_json.mkdir(parents=True, exist_ok=True)
    VerticalFlip_image.mkdir(parents=True, exist_ok=True)
    VerticalFlip_mask.mkdir(parents=True, exist_ok=True)
    data_augmentation.mkdir(parents=True, exist_ok=True)

    HorizontalFlip_image = data_augmentation / 'HorizontalFlip' / 'image'
    HorizontalFlip_mask = data_augmentation / 'HorizontalFlip' / 'mask'
    HorizontalFlip_save_json = data_augmentation / 'HorizontalFlip' / 'json'
    HorizontalFlip_save_json.mkdir(parents=True, exist_ok=True)
    HorizontalFlip_image.mkdir(parents=True, exist_ok=True)
    HorizontalFlip_mask.mkdir(parents=True, exist_ok=True)
    data_augmentation.mkdir(parents=True, exist_ok=True)


    savePath = HorizontalFlip_save_json
    yamlPath = '/Users/clustar/PycharmProjects/mask2json_pr/info.yaml'
    imgPath = HorizontalFlip_image
    maskPath = HorizontalFlip_mask
    oriImgs = glob(f'{imgPath}/*')
    for i in oriImgs:
        maskname = i.replace('image', 'mask').replace('.jpg', '.png')
        if Path(maskname).exists():
            getMultiShapes.getMultiShapes(i, maskname, str(savePath), yamlPath)
        else:
            print('mask图片不存在')
    print("Processed successfully")




