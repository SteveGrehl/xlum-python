import pytest
import os
DIRNAME = os.path.dirname(__file__)
import sys
sys.path.append(
    os.path.join(
        DIRNAME,
        '../')
)
from data.classes import XlumMeta
import importer


def test_import() -> None:
    """test if a file can be imported

    Args:
        fn (str): path to file
    """
    for fn in ["xlum_example.xlum", "xlum_prototype.xlum"]:
        assert isinstance(importer.from_xlum(
            os.path.join(
                DIRNAME,
                "..",
                "..",
                "assets",
                fn
            )
        ), XlumMeta)


@pytest.mark.xfail
def test_import_fails() -> None:
    importer.from_xlum(
        os.path.join(
            DIRNAME,
            "..",
            "..",
            "assets",
            "xlum_invalid.xlum"
        )
    )