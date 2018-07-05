"""Setup for gibica package."""

from setuptools import setup, find_packages


setup(
    name="gibica",
    version="0.5.0",
    author="Matthieu Gouel",
    author_email="matthieu.gouel@gmail.com",
    url="https://github.com/matthieugouel/gibica",
    description="Interprète ? Interprète ? Cuillère !",
    long_description=open('README.md').read(),
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'click'
    ],
    entry_points='''
        [console_scripts]
        gibica=gibica.gibica:main
    ''',
)
