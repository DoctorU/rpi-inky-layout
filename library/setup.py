from distutils.core import setup
dist = 'https://github.com/DoctorU/rpi-inky-layout/dist/v0.0.0.tar.gz'
setup(
  name='rpi-inky-layout',
  packages=['rpi_inky_layout'],
  version='0.0.0',
  license='MIT',
  description="A layout companion library for Pimoroni's Inky HATs",
  author='Stephen Hobdell',
  author_email='doctoruseful@gmail.com',
  url='https://github.com/DoctorU/rpi-inky-layout',
  download_url=dist,
  keywords=['Layout', 'Framework', 'Image', 'Inky', 'Pimoroni'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Application Development',
    'Topic :: Multimedia :: Graphics :: Presentation',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    "License :: OSI Approved :: MIT License",
    "Operating System :: Other OS"
  ]
)
