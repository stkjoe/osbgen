import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="osbgen",
    version="0.0.1",
    author="stkjoe",
    author_email="joestephen1997@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: tbc :: tbc",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)