'''
lanhuage: python
Descripttion:
'''

__support_img_types__ = ['*.jpg', '*.jpeg', '*.bmp', '*.png']

__support_anno_types__ = ['*.txt', '*.json', '*.xml']

__support_classfiles_types__ = ['*.txt', '*.yaml']

__support_aug_methods__ = ['flip', 'noise', 'rotation', 'translation', 'zoom']

__support_aug_optional_methods__ = [
    'crop', 'distort', 'inpaint', 'perspective', 'resize'
]

__version__ = '1.0'
__appname__ = 'convertmask'
__support_methods__ = [
    'mask2json',
]


import multiprocessing

__CPUS__ = multiprocessing.cpu_count()
del multiprocessing

import argparse
from functools import wraps

import platform

__current_platform__ = platform.system()

del platform

def do_nothing():
    pass


def baseDecorate(message: str = ''):
    def dep_decorator(func):
        @wraps(func)
        def dep(*args, **kwargs):
            if message == '':
                print(func.__name__ +
                      ' is deprecated under {}.'.format(__version__))
            else:
                print(message)
            return func(*args, **kwargs)

        return dep

    return dep_decorator


