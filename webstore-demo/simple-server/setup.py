from setuptools import setup, find_packages

requires = [
    'flask',
]

setup(
    name='simpleserver',
    version='0.0',
    description='A Python implementation of Simple Server',
    author='Kari Marttila',
    author_email='kari.marttila@ikif.i',
    keywords='Python Flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
