import setuptools
import os

basedir = os.path.dirname(os.path.realpath(__file__))
requirements = basedir + "/requirements.txt"
install_requires = []
if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gh2db",
    version="0.1.0",
    author="MichinaoShimizu",
    author_email="",
    description="Convert Github Data to Database.",
    long_description="Convert Github Data to Database.",
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/MichinaoShimizu/gh2db",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'mysumy = gh2db.gh2db.__main__:main',
        ]
    },
    python_requires='>=3.6',
)
