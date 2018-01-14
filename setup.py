"""A basic setup.py.
"""

from setuptools import setup, find_packages

setup(
    name='scroll_background',
    version='1.0.5',
    author='AarnoT',
    url='https://github.com/aarnot/scroll_background',
    packages=find_packages('src', exclude=['docs', 'tests', 'env']),
    package_dir={'': 'src'},
    install_requires=['pygame == 1.9.3'],
    extras_require={
        'test': ['pytest'],
        'docs': ['sphinx', 'numpydoc']
    }
)
