from setuptools import setup, find_packages


setup(
    name='datatype',
    version='0.2',
    description='Anonymous datatype validation',
    packages=find_packages(),
    install_requires=['pytest', 'pytest-cov'],
    author = 'Adam Wagner',
    author_email = 'awagner83@gmail.com',
    url = 'https://github.com/LearningStation/datatype',
    license = 'BSD3'
)

