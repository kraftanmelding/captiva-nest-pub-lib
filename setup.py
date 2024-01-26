from setuptools import find_packages
from setuptools import setup
import sys, os

VERSION = '0.0.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='tyde3pub',
  packages=find_packages(),
  version=VERSION,
  license='Broentech Solutions AS',
  author="Luca Petricca",
  author_email="lucap@broentech.no",
  description="library implementing tyde3 functionalities, authentication, timeseries etc",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/enestor-as/tyde3-pub-lib',
  download_url = 'https://github.com/enestor-as/tyde3-pub-lib/dist/tyde3pub-_%s.tar.gz' % VERSION,
  keywords = ['tyde', 'timeseries', 'auth', "tyde3"],
  install_requires=[
    'PyJWT',
    'cryptography',
    'requests',
    'rauth',
    'numpy',
    'pint'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: Broentech Proprietary',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
  python_requires='>=3.8',
)

