import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="osbgen",
    version="1.0.0.dev1",
    author="stkjoe",
    author_email="joestephen1997@gmail.com",
    description="A python library to create osu! storyboards in an object-orientated way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stkjoe/osbgen",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.8",
)