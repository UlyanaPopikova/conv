

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='time_converter',

    version='1.2.5',

    packages=find_packages(),
    install_requires=['numpy', 'python-dateutil', 'tqdm', 'requests', 'pandas'],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'numpydoc', 'Sphinx'],
        'spice': ['spiceypy']
    },
    package_data={
        'time_converter.converters': [
            'msl/msl.tsc',
            'change4/change4_localtime.dat'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
