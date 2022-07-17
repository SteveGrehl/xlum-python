import pytest
import os
import urllib
from xlum.data.classes import XlumMeta
import xlum.importer as importer


def get_assets_dir() -> os.PathLike:
    """return path to assets folder

    Returns:
        os.PathLike: path to assets folder
    """
    assets_dir = os.path.dirname(__file__).split("/")[:-2]
    assets_dir = os.path.join("/", *assets_dir, "assets")
    assert os.path.isdir(assets_dir), f"{assets_dir=} not found"
    return assets_dir


@pytest.mark.parametrize("fn", [("xlum_prototype.xlum"), ("xlum_prototype_b64.xlum")])
def test_import(fn: os.PathLike) -> None:
    """test if a file can be imported

    Args:
        fn (str): path to file
    """
    full_path = os.path.join(get_assets_dir(), fn)
    assert os.path.isfile(full_path), f"{full_path=} is not a file"
    assert isinstance(importer.from_xlum(full_path), XlumMeta)


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


@pytest.mark.parametrize("fn", [("xlum_invalid.xlum")])
@pytest.mark.xfail
def test_import_fails(fn: os.PathLike) -> None:
    full_path = os.path.join(get_assets_dir(), fn)
    assert os.path.isfile(full_path), f"{full_path=} is not a file"
    importer.from_xlum(full_path)
