from setuptools import setup, find_packages
import os
import sys

with open("README.rst", "r") as fh:
    long_description = fh.read()


def my_test_suite():
    import unittest
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py', top_level_dir="src")
    return test_suite


if __name__ == '__main__':
    try:
        os.makedirs("local/server_side/ROOT/", exist_ok=True)
    except FileExistsError:
        pass

    setup(name='OpenDrive',
          version='0.1a1',
          description='Open source, self hosting alternative to GoogleDrive',
          long_description=long_description,
          url='https://github.com/JulianSobott/OpenDrive',
          author='Julian Sobott',
          author_email='julian.sobott@gmx.de',
          #packages=find_packages("src", ["tests", "tests.*"]), # excludes tests
          packages=find_packages("src"),
          package_dir={'': 'src'},
          test_suite='setup.my_test_suite',
          include_package_data=True,
          keywords='synchronisation backup share cloud',
          project_urls={
            "Bug Tracker": "https://github.com/JulianSobott/OpenDrive/issues",
            "Documentation": "https://github.com/JulianSobott/OpenDrive/wiki",
            "Source Code": "https://github.com/JulianSobott/OpenDrive",
          },
          classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            ],
          zip_safe=False,
          install_requires=['pynetworking', 'watchdog', 'passlib']
          )
