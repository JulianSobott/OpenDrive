from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='OpenDrive',
      version='0.1a1',
      description='Open source, self hosting alternative to GoogleDrive',
      long_description=long_description,
      url='https://github.com/JulianSobott/OpenDrive',
      author='Julian Sobott',
      author_email='julian.sobott@gmx.de',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
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
      zip_safe=False
      )
