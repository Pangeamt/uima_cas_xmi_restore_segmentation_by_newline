import zipfile
import re
from pathlib import Path
from cassis import load_typesystem, load_cas_from_xmi
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SOURCE_DIR = Path('001_source')
TARGET_DIR = Path('002_target')

SENTENCE_NS = 'de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence'
TOKEN_NS = 'de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token'


def uima_cas_xmi_segment_by_new_line(source, target=None):

            segment_by_newline(source, target)


def segment_by_newline(source: Path, target: Path):
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
        for sentence in list(cas.select(SENTENCE_NS)):
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
                    annotation = ts.get_type(SENTENCE_NS)(begin=start, end=idx, sofa=sofa.sofaNum)
                    cas.add_annotation(annotation)

        zf = zipfile.ZipFile(target, "w")
        zf.writestr(type_system, ts.to_xml())
        zf.writestr(xmi, cas.to_xmi(pretty_print=True))
        zf.close()


if __name__ == '__main__':
    main()
