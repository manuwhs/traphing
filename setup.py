from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="traphing",
    version="0.0.1",
    author="Manuel Montoya",
    author_email="manuwhs@gmail.com",
    description="A package to make trading in python easier",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/manuwhs/traphing",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)