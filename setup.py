import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="img2ascii",
    version="1.2.3",
    author="Gopalji Gaur",
    author_email="gopaljigaur@gmail.com",
    description="Image/Video to ASCII conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gopaljigaur/img2ascii",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=['numpy','opencv-python','filetype','comtypes'],
)
