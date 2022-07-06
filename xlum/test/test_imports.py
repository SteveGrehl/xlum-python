import pytest
import os
import urllib
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
    for fn in ["xlum_prototype.xlum"]:
        assert isinstance(importer.from_xlum(
            os.path.join(
                DIRNAME,
                "..",
                "..",
                "assets",
                fn
            )
        ), XlumMeta)


def test_gh_import() -> None:
    # Download example file
    url = 'https://raw.githubusercontent.com/R-Lum/xlum_specification/master/examples/xlum_example.xlum'
    local_dir = os.path.join(os.getcwd(), "tmp")
    local_path = os.path.join(local_dir, "example.xlum")
    os.mkdir(local_dir)
    urllib.request.urlretrieve(url, local_path)

    try:
        assert isinstance(importer.from_xlum(
            local_path
        ), XlumMeta)
    finally:
        os.remove(local_path)
        os.rmdir(local_dir)


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