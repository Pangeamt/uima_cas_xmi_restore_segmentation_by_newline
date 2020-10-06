import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uima_cas_xmi_restore_segmentation_by_newline",
    version="0.0.1",
    author="Laurent Bié",
    author_email="l.bie@pangeanic.com",
    description="UIMA CAS XMI restore segmentation by newline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pangeamt/web_anno_tsv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)