import zipfile
import re
from pathlib import Path
from typing import Union
from cassis import load_typesystem, load_cas_from_xmi


def uima_cas_xmi_restore_segmentation_by_newline(
        source: Union[str, Path],
        target: Union[str, Path],
        sentence_ns: str = 'de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence'):
    archive = zipfile.ZipFile(source, 'r')

    xmi = None
    type_system = None

    for file in archive.namelist():
        if file.endswith('.xmi'):
            xmi = file
        if file.endswith('.xml'):
            type_system = file

    if not xmi:
        raise ValueError("Xmi file not found")
    if not type_system:
        raise ValueError("Type system file not found")

    with archive.open(type_system, 'r') as f:
        ts = load_typesystem(f)

    with archive.open(xmi, 'r') as f:
        cas = load_cas_from_xmi(f, typesystem=ts)

        # Remove sentence annotation
        for sentence in list(cas.select(sentence_ns)):
            cas.remove_annotation(sentence)

        # Create new sentence annotations
        for sofa in cas.sofas:
            idx = 0
            separator = re.compile('((?:\r?)\n)')
            for item in re.compile(separator).split(sofa.sofaString):
                start = idx
                if re.match(separator, item):
                    idx += len(item)
                elif len(item):
                    idx += len(item)
                    annotation = ts.get_type(sentence_ns)(begin=start, end=idx, sofa=sofa.sofaNum)
                    cas.add_annotation(annotation)

        zf = zipfile.ZipFile(target, "w")
        zf.writestr(type_system, ts.to_xml())
        zf.writestr(xmi, cas.to_xmi(pretty_print=True))
        zf.close()



