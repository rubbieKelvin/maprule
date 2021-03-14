import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='maprule',  
    version='0.1.3',
    author="Rubbie Kelvin",
    author_email="dev.rubbie@gmail.com",
    description="package for validating values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rubbiekelvin/maprule",
    packages=["maprule"],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)