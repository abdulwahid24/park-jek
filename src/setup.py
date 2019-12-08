import os
import setuptools
import random

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="park-jek",
    version="0.0.1",
    author="Abdulwahid Barguzar",
    author_email="abdulwahid24@gmail.com",
    description="A Parking Lot Management Software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LICENSE',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['LICENCE', 'README.md', '*.ini', "*.txt"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "configparser == 3.7.4", "pip == 19.1.1", "pycodestyle == 2.5.0"
    ],
    entry_points={
        'console_scripts': [
            'park-jek=src.app.__main__:main',
            'park-jek-test=src.app.__test__:main',
        ],
    },
)
