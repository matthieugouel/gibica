"""Setup for gibica package."""

from setuptools import setup, find_packages


setup(
    name="gibica",
    version="0.8.2",
    author="Matthieu Gouel",
    author_email="matthieu.gouel@gmail.com",
    url="https://github.com/matthieugouel/gibica",
    description="Interprète ? Interprète ? Cuillère !",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    packages=find_packages(),
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        gibica=gibica.entrypoint:main
    """,
)
