# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='wavplot',
    version='0.1.0',
    author='Fabian-Robert Stöter, Nils Werner',
    author_email='mail@faroit.com, nils@hey.com',
    url='https://github.com/nils-werner/wavplot',

    description='Generate waveform and spectrogram png images from a wav file',

    install_requires=[
        'scipy',
        'numpy',
        'matplotlib',
        'PySoundFile>=0.7.0',
    ],

    platforms='any',
    keywords=['audio'],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Sound/Audio'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wavplot = wavplot:main',
        ]
    },
)
