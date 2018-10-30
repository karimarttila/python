from setuptools import find_packages, setup


setup(
    name='simpleserver',
    version='0.0',
    description='A Python implementation of Simple Server',
    author='Kari Marttila',
    author_email='kari.marttila@ikif.i',
    keywords='Python Flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage'
        ],
    },
)
