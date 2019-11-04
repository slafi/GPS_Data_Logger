from setuptools import setup

with open("Readme.md", 'r') as f:
    long_description = f.read()

setup(
   name='Car_Data_logger',
   version='1.0',
   description='This project implements a data logger which connects to a GPS device and stores the real-time location info to a SQLite database. It also allows to export saved data as GPX and KML files.',
   author='Sabeur Lafi',
   author_email='lafi.saber@gmail.com',
   url="https://github.com/slafi",
   license="MIT",
   long_description=long_description,
   packages=['car_data_logger'],
   keywords=["data logger", "GPS data logger", "vk-162", "GPS tracking", "GPX", "KML"],
   classifiers=[
       "Programming Language :: Python",
       "Programming Language :: Python :: 3",
       "Development Status :: 4 - Beta",
       "Operating System :: POSIX :: Linux",
       "License :: OSI Approved :: MIT License"
   ],
)