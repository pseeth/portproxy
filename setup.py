# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='portproxy',
    version='0.6.1', 
    description='Automatically forward and manage ports from any remote machines.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pseeth/portproxy/',
    author='Prem Seetharaman',
    author_email='prem@descript.com', 
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
    ],
    keywords='command-line configuration yaml argument parsing',
    packages=find_packages(),  # Required
    python_requires='>=3.5, <4',
    install_requires=[
        'argbind>=0.3.1',
        'sshtunnel',
        'dominate',
        'Flask',
        'portpicker',
        'marko'
    ],
    extras_require={ 
        'tests': ['pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'portproxy = portproxy:main',
            'portproxy.forward = portproxy:forward' 
        ]
    },
    include_package_data=True
)