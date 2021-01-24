from os import path
import setuptools

VERSION = "v0.0.0"
DIST_FMT = "https://github.com/DoctorU/rpi-inky-layout/dist/{VERSION}.tar.gz"
DIST_URL = DIST_FMT.format(VERSION=VERSION)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(
  name='rpi-inky-layout',
  version='0.0.0',
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
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Multimedia :: Graphics :: Presentation',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    "License :: OSI Approved :: MIT License",
    "Operating System :: Other OS"
  ]
)
