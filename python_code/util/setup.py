from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Python package containing wrappers for common utilities'
LONG_DESCRIPTION = 'Python package containing wrappers for common utilities for ease of use'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="utils", 
        version=VERSION,
        author="KKV",
        author_email="kuld.kkv@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'utils'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: cross platform",
        ]
)
