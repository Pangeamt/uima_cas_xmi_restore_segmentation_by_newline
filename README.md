# UIMA CAS XMI. Restore segmentation by newline

When a text file (with one sentence per line) is uploaded to Inception as PLAIN/TEXT, 
the original segmentation is broken. This library helps to restore it.


## Install
Install the last version of dkpro-cassis from github:

```BASH
    pip install -U git+https://github.com/dkpro/dkpro-cassis
```

Install this library:

```BASH
    pip install git+https://github.com/Pangeamt/uima_cas_xmi_restore_segmentation_by_newline
```

## Usage
1) In Inception, export the file as UIMA CAS XMI.
2) With your preferred python editor:
```python
from uima_cas_xmi_restore_segmentation_by_newline import uima_cas_xmi_restore_segmentation_by_newline


uima_cas_xmi_restore_segmentation_by_newline(
    "uima_cas_xmi.zip",
    "uima_cas_xmi_resegmented.zip"
)


```
3) Unzip the uima_cas_xmi_resegmented.zip file and upload the xmi file to Inception.