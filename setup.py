#!/usr/bin/env python3

from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['engagement_detector'],
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'pillow',
        'tensorflow-cpu==2.13.0',  # Or match your TF version
        'keras==2.13.0',
        'keras-applications',  # Required for ResNeXt
        'opencv-python',
        'rospkg'
    ]
)

setup(**d)
