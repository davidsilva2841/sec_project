import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sec_edgar",
    version="0.0.2",
    author="David Silva",
    author_email="david.silva2841+python@gmail.com",
    description="A package for automatically downloading & updating data from the SEC Edgar database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidsilva2841/sec_project",
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=[
        ('', ['LICENSE.txt']),
        ('', ['README.md']),
        ('', ['requirements.txt']),
        ('', ['MANIFEST.in'])
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment"
    ],
)