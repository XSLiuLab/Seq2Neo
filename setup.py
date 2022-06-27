import os

from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 7):
    print("This python version is not supported:")
    print(sys.version)
    print("Seq2Neo requires python 3.7 or greater")
    sys.exit(1)

data_files = []
for dirpath, dirnames, filenames in os.walk("seq2neo/function/immuno_Prediction/data"):
    for filename in filenames:
        data_files.append(os.path.join(os.path.relpath(dirpath, 'seq2neo/function/immuno_Prediction'), filename))

setup(
    name="Seq2Neo",
    version="v1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'seq2neo.function.immuno_Prediction': data_files
    },
    entry_points={
        "console_scripts": [
            "seq2neo = seq2neo.main:main",
        ]
    },
    install_requires=[
        'protobuf<3.20',
        'biopython==1.77',
        'keras==2.4.3',
        'tensorflow==2.3.0',
        'agfusion==1.252',

    ],
    author=" Kaixuan Diao",
    author_email="diaokx@shanghaitech.edu.cn",
    description="Seq2Neo: a comprehensive pipeline for cancer neoantigen immunogenicity prediction",
    keywords="neoantigen fusion immunogenicity prediction sequencing cancer",
    long_description_content_type="text/markdown",
    url="https://github.com/XSLiuLab/Seq2Neo",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Academic Free License v. 3.0",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires='>=3'
)
