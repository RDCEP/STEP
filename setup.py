import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="step",
    version="1.0.0",
    author="Alex Rittler",
    author_email="arittler@haverford.edu",
    description="Identifies, tracks, and computes physical characteristics of rainstorms given spatiotemporal precipitation data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RDCEP/STEP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['imageio','matplotlib','netCDF4','numpy','scikit-image','scipy'],
)
