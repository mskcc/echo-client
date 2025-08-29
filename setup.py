from setuptools import setup, find_packages


def read_requirements():
    """
    Read requirements from requirements.txt
    :return: list of dependency packages
    """
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()


# Read the README file for the long description
def read_readme():

    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="echo_client",
    version="0.1.0",
    author="MSK CMO",
    author_email="ivkovics@mskcc.org",
    description="Python Library for Echo Service (Copy Service)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mskcc/echo-client",
    packages=find_packages(),
    install_requires=read_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
