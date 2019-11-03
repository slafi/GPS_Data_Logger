from setuptools import setup

with open("Readme.md", 'r') as f:
    long_description = f.read()

setup(
   name='Car_Data_logger',
   version='1.0',
   description='This project implements a data logger which connects to the car through an OBD reader (e.g., ELM327) and stores the retrieved data to a SQLite database. It also stores the car location whenever a GPS connection is available.',
   author='Sabeur Lafi',
   author_email='lafi.saber@gmail.com',
   url="https://github.com/slafi",
   license="MIT",
   long_description=long_description,
   packages=['car_data_logger'],
   keywords=["data logger", "car data logger", "ELM327", "GPS tracking"],
   classifiers=[
       "Programming Language :: Python",
       "Programming Language :: Python :: 3",
       "Development Status :: 4 - Beta",
       "Operating System :: POSIX :: Linux",
       "License :: OSI Approved :: MIT License"
   ],
)