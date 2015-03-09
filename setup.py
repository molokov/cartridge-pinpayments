from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

version = "0.0.1"


setup(
    name='cartridge-pinpayments',
    version=version,

    description='PIN payment processor integration for mezzanine/cartridge',
    long_description=open("README.md", 'rb').read().decode('utf-8'),

    # The project's main homepage.
    url='https://github.com/molokov/cartridge-pinpayments',

    # Author details
    author='Danny Sag (molokov)',
    author_email='molokov@gmail.com',

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: "
                                        "Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords='django mezzanine cartridge payment',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['mezzanine', 'cartridge', 'django-pinpayments'],

)
