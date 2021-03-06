from setuptools import setup, find_packages


setup(
    name='datatype',
    version='0.9a3',
    description='Anonymous datatype validation and coercion',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=['pytest', 'pytest-cov', 'doctools', 'mock'],
    author = 'Adam Wagner',
    author_email = 'awagner83@gmail.com',
    url = 'https://github.com/awagner83/datatype',
    license = 'BSD3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Libraries'
    ]
)

