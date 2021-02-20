from os import path
import setuptools

VERSION = "v0.2.0"
DIST_FMT = "https://github.com/DoctorU/rpi-inky-layout/dist/{VERSION}.tar.gz"
DIST_URL = DIST_FMT.format(VERSION=VERSION)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(
  name='rpi-inky-layout',
  version='0.2.0',
  license='MIT',
  description="A layout companion library for Pimoroni's Inky HATs",
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Stephen Hobdell',
  author_email='doctoruseful@gmail.com',
  url='https://github.com/DoctorU/rpi-inky-layout',
  download_url=DIST_URL,
  packages=setuptools.find_packages(),
  keywords=['Layout', 'Framework', 'Image', 'Inky', 'Pimoroni'],
  install_requires=[
    'numpy>=1.19.5',
    'Pillow>=8.1.0'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Multimedia :: Graphics :: Presentation',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    "License :: OSI Approved :: MIT License",
    "Operating System :: Other OS"
  ]
)
