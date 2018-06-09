"""Setup for gibica package."""
import uuid

from setuptools import setup, find_packages
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

INSTALL_REQS = parse_requirements('requirements.txt', session=uuid.uuid1())
REQS = [str(ir.req) for ir in INSTALL_REQS]

setup(
    name="gibica",
    version="0.1.0",
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
    install_requires=REQS,
    py_modules=['gibica'],
    entry_points='''
        [console_scripts]
        gibica=gibica.gibica:main
    ''',
)
