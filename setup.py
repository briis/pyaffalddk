"""Package Setup."""

import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaffalddk",
    version="2.12.2",
    author="briis",
    author_email="bjarne@briis.com",
    description="Gets garbage collection data from danish Municipalities",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briis/pyaffalddk",
    packages=setuptools.find_packages(),
    package_data={
        'pyaffalddk': ['supported_items.json'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
